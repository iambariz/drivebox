import mss
import mss.tools
import os
import tempfile
from datetime import datetime
from drivebox.region_selector import RegionSelector

class Screenshotter:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def _get_formatted_filename(self, prefix=""):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        return os.path.join(self.temp_dir, f"{prefix}{timestamp}_screenshot.png")

    def select_region(self):
        selector = RegionSelector()
        if selector.exec_() == selector.Accepted and selector.selected_rect:
            rect = selector.selected_rect
            return rect.left(), rect.top(), rect.width(), rect.height()
        return None

    def take_fullscreen(self):
        """Take a screenshot of the primary monitor using mss."""
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # 1 = primary monitor
            output = self._get_formatted_filename("fullscreen_")
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            print(f"Screenshot saved as {output}")
            return output

    def take_region(self):
        """Take a screenshot of a user-selected region using mss."""
        region = self.select_region()
        if region:
            left, top, width, height = region
            monitor = {
                "left": left,
                "top": top,
                "width": width,
                "height": height
            }
            output = self._get_formatted_filename("region_")
            with mss.mss() as sct:
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
                print(f"Screenshot saved as {output}")
                return output
        else:
            print("No region selected")
            return None

if __name__ == "__main__":
    ss = Screenshotter()
    ss.take_region_with_mss()
