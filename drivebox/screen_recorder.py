import os
import sys
import subprocess
import datetime
from drivebox.utils import resource_path


class ScreenRecorder:
    def __init__(self):
        self.process = None
        self.output_file = None
        self.ffmpeg_path = self._get_ffmpeg_path()

    def _get_ffmpeg_path(self):
        """Get path to bundled or system ffmpeg binary"""
        exe_name = "ffmpeg.exe" if sys.platform.startswith("win") else "ffmpeg"
        ffmpeg_path = resource_path(os.path.join("resources", "ffmpeg", exe_name))

        if os.path.exists(ffmpeg_path):
            # Make it executable on Linux/Mac
            if not sys.platform.startswith("win"):
                os.chmod(ffmpeg_path, os.stat(ffmpeg_path).st_mode | 0o111)
            return ffmpeg_path

        # Fallback to system ffmpeg
        return exe_name

    def _list_pulse_devices(self):
        """List available PulseAudio devices (Linux only)"""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-sources", "pulse"],
                capture_output=True,
                text=True,
                check=True,
            )
            devices = []
            for line in result.stdout.splitlines():
                if "alsa_" in line:
                    devices.append(line.strip().split()[0])
            return devices
        except Exception:
            return []

    def _get_default_audio_args(self):
        """Return ffmpeg args for audio input depending on platform"""
        if sys.platform.startswith("linux"):
            devices = self._list_pulse_devices()
            if devices:
                # Prefer monitor (system audio) if available
                for d in devices:
                    if "monitor" in d:
                        return ["-f", "pulse", "-i", d]
                # Otherwise use first device (likely mic)
                return ["-f", "pulse", "-i", devices[0]]
            # fallback: no audio
            return []

        elif sys.platform == "darwin":  # macOS
            # avfoundation: 0 = screen, :0 = default audio
            return ["-f", "avfoundation", "-i", ":0"]

        elif sys.platform == "win32":
            # DirectShow on Windows (example device name)
            return ["-f", "dshow", "-i", "audio=Microphone (Realtek Audio)"]

        return []

    def start_recording(self):
        """Start screen recording"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        self.output_file = f"/tmp/screen_record_{timestamp}.mp4"

        # Base ffmpeg command
        cmd = [
            self.ffmpeg_path,
            "-y",
        ]

        # Video input
        if sys.platform.startswith("linux"):
            cmd += ["-f", "x11grab", "-i", ":0.0"]
        elif sys.platform == "darwin":
            cmd += ["-f", "avfoundation", "-i", "1:none"]  # screen only
        elif sys.platform == "win32":
            cmd += ["-f", "gdigrab", "-i", "desktop"]

        # Add audio input if available
        cmd += self._get_default_audio_args()

        # Output settings
        cmd += [
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            self.output_file,
        ]

        print("Starting ffmpeg with command:", " ".join(cmd))

        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Recording started: {self.output_file}")
        except Exception as e:
            print(f"Failed to start recording: {e}")
            self.process = None

    def stop_recording(self):
        """Stop recording and return output file path"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

            if os.path.exists(self.output_file):
                print(f"Recording stopped: {self.output_file}")
                return self.output_file
            else:
                print("⚠️ Recording file not found after stopping")
                return None
        return None