import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import time
from screenshot import take_screenshot
from upload import upload_file_to_drivebox
import pyperclip
import os

def create_image():
    # Create a simple icon (a blue circle)
    image = Image.new('RGB', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill='blue')
    return image

def on_take_screenshot(icon, item):
    filename = take_screenshot()
    if filename and os.path.exists(filename):
        link = upload_file_to_drivebox(filename)
        pyperclip.copy(link)
        os.remove(filename)
        print(f"Screenshot uploaded! Link copied to clipboard: {link}")
    else:
        print("Screenshot failed.")

def on_exit(icon, item):
    icon.stop()

def run_tray():
    icon = pystray.Icon(
        "DriveBox",
        create_image(),
        "DriveBox",
        menu=pystray.Menu(
            item('Take Screenshot', on_take_screenshot),
            item('Exit', on_exit)
        )
    )
    icon.run()

if __name__ == "__main__":
    # Run the tray icon in the main thread
    run_tray()
