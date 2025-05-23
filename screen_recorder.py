import sys
import subprocess
import tempfile
import os
from datetime import datetime
from utils import resource_path

class ScreenRecorder:
    def __init__(self):
        self.process = None
        self.output_file = None

    def _get_output_filename(self):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir, f"screen_record_{timestamp}.mp4")
        
    def _get_ffmpeg_path(self):
        """Get path to bundled FFmpeg binary"""
        # Try resources folder first
        ffmpeg_path = resource_path(os.path.join("resources", "ffmpeg", "ffmpeg"))
        if os.path.exists(ffmpeg_path):
            # Make it executable on Linux/Mac
            if not sys.platform.startswith("win"):
                import stat
                os.chmod(ffmpeg_path, os.stat(ffmpeg_path).st_mode | stat.S_IXUSR)
            return ffmpeg_path
            
        # Try the extracted folder in project root
        project_dir = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_path = os.path.join(project_dir, "ffmpeg-7.0.2-amd64-static", "ffmpeg")
        if os.path.exists(ffmpeg_path):
            if not sys.platform.startswith("win"):
                import stat
                os.chmod(ffmpeg_path, os.stat(ffmpeg_path).st_mode | stat.S_IXUSR)
            return ffmpeg_path
            
        # Fall back to system command
        return "ffmpeg"

    def start_recording(self):
        self.output_file = self._get_output_filename()
        ffmpeg_path = self._get_ffmpeg_path()
        
        if sys.platform.startswith("win"):
            cmd = [
                ffmpeg_path,
                "-y",
                "-f", "gdigrab",
                "-framerate", "30",
                "-i", "desktop",
                "-f", "dshow",
                "-i", "audio=Microphone (Realtek Audio)",
                "-vcodec", "libx264",
                "-preset", "ultrafast",
                self.output_file
            ]
        elif sys.platform.startswith("darwin"):
            cmd = [
                ffmpeg_path,
                "-y",
                "-f", "avfoundation",
                "-framerate", "30",
                "-i", "1:0",  # 1:0 = screen:audio
                self.output_file
            ]
        elif sys.platform.startswith("linux"):
            cmd = [
                ffmpeg_path,
                "-y",
                "-f", "x11grab",
                "-framerate", "30",
                "-i", ":0.0",
                "-f", "pulse",
                "-i", "default",
                self.output_file
            ]
        else:
            raise Exception("Unsupported OS")

        try:
            self.process = subprocess.Popen(cmd)
            print(f"Recording started: {self.output_file}")
        except Exception as e:
            print(f"Failed to start recording: {e}")
            raise

    def stop_recording(self):
        if self.process:
            try:
                self.process.terminate()
                try:
                    stdout, stderr = self.process.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    print("ffmpeg did not terminate in time, killing process.")
                    self.process.kill()
                    stdout, stderr = self.process.communicate()
                print("ffmpeg stderr:\n", stderr.decode() if stderr else "")
                print(f"Recording stopped: {self.output_file}")
                # Wait for file to appear
                import time
                for _ in range(10):
                    if os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0:
                        return self.output_file
                    time.sleep(0.5)
                print(f"Warning: Recording file not found after stopping: {self.output_file}")
                return None
            except Exception as e:
                print(f"Error stopping recording: {e}")
                return None
        else:
            print("No recording in progress.")
            return None
