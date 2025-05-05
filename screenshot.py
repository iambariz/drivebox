import platform
import os
import shutil

def take_screenshot(filename='screenshot.png'):
    system = platform.system()
    # Try mss first (works on Windows, macOS, Linux/X11)
    try:
        import mss
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
            print("screencapture not found. Please use Command+Shift+4 to take a screenshot.")
            return None
    elif system == "Linux":
        # Try gnome-screenshot
        if shutil.which("gnome-screenshot"):
            os.system(f"gnome-screenshot -f {filename}")
            print(f"Screenshot saved as {filename} (via gnome-screenshot)")
            return filename
        # Try grim (Wayland)
        elif shutil.which("grim"):
            os.system(f"grim {filename}")
            print(f"Screenshot saved as {filename} (via grim)")
            return filename
        # Try spectacle (KDE)
        elif shutil.which("spectacle"):
            os.system(f"spectacle -b -o {filename}")
            print(f"Screenshot saved as {filename} (via spectacle)")
            return filename
        else:
            print("No supported screenshot tool found. Please install gnome-screenshot, grim, or spectacle.")
            return None
    else:
        print("Unsupported OS.")
        return None

if __name__ == "__main__":
    take_screenshot()
