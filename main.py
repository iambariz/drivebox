from screenshot import take_screenshot
from upload import upload_file_to_drivebox
import os

def main():
    filename = take_screenshot()
    if filename and os.path.exists(filename):
        link = upload_file_to_drivebox(filename)
        print(f"Shareable link: {link}")
    else:
        print("Screenshot failed, nothing to upload.")

if __name__ == "__main__":
    main()