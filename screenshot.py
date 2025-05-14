import platform
import os
import shutil
import subprocess

def is_wayland():
    """Check if running on Wayland"""
    return os.environ.get('XDG_SESSION_TYPE') == 'wayland'

def take_screenshot(filename='screenshot.png'):
    system = platform.system()

    # On Linux, check for Wayland first and use appropriate tools
    if system == "Linux" and is_wayland():
        print("Detected Wayland session, using native tools...")

        # Try wl-screenshot (a Wayland-native screenshot tool)
        if shutil.which("grim"):
            os.system(f"grim {filename}")
            print(f"Screenshot saved as {filename} (via grim)")
            return filename
        # Try gnome-screenshot (works on GNOME/Wayland via portal)
        elif shutil.which("gnome-screenshot"):
            os.system(f"gnome-screenshot -f {filename}")
            print(f"Screenshot saved as {filename} (via gnome-screenshot)")
            return filename
        else:
            print("No supported Wayland screenshot tool found.")
            return None

    # For non-Wayland systems, try mss first
    try:
        # Only import mss if we're going to use it
        import mss
        import mss.tools

        print("Taking screenshot using mss...")
        with mss.mss() as sct:
            sct.shot(output=filename)
        print(f"Screenshot saved as {filename} (via mss)")
        return filename
    except Exception as e:
        print(f"mss failed: {e}")

    # Fallbacks for each OS
    if system == "Windows":
        print("Automatic screenshot failed..")
        # os.system("start snippingtool")
        return None
    elif system == "Darwin":  # macOS
        if shutil.which("screencapture"):
            os.system(f"screencapture {filename}")
            print(f"Screenshot saved as {filename} (via screencapture)")
            return filename
        else:
            print("screencapture not found.")
            return None
    elif system == "Linux":
            print("No supported screenshot tool found.")
            return None
    else:
        print("Unsupported OS.")
        return None

if __name__ == "__main__":
    take_screenshot()