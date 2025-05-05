from screenshot import take_screenshot
from upload import upload_file_to_drivebox
import os
import pyperclip

def main():
    filename = take_screenshot()
    if filename and os.path.exists(filename):
        link = upload_file_to_drivebox(filename)
        print(f"Shareable link: {link}")
        pyperclip.copy(link)
        print("Shareable link copied to clipboard!")
        # Delete the screenshot file
        try:
            os.remove(filename)
            print(f"Deleted local file: {filename}")
        except Exception as e:
            print(f"Could not delete file: {e}")
    else:
        print("Screenshot failed, nothing to upload.")

if __name__ == "__main__":
    main()
