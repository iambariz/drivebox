import os
import sys
import types

# Force PyQt5 to run headless in CI
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Only mock pynput in CI (headless GitHub Actions)
if os.environ.get("CI") == "true":
    print(">>> Using fake pynput for CI <<<")

    # Remove real pynput if already imported
    sys.modules.pop("pynput", None)
    sys.modules.pop("pynput.keyboard", None)

    # Create fake pynput module
    sys.modules['pynput'] = types.ModuleType("pynput")
    sys.modules['pynput.keyboard'] = types.ModuleType("pynput.keyboard")

    class FakeKey:
        ctrl_l = "ctrl_l"
        alt_l = "alt_l"
        shift_l = "shift_l"

    class FakeKeyCode:
        def __init__(self, char=None):
            self.char = char

        @staticmethod
        def from_char(char):
            return FakeKeyCode(char)

    class FakeListener:
        def __init__(self, on_press=None, on_release=None):
            self.on_press = on_press
            self.on_release = on_release
            self.running = False

        def start(self):
            self.running = True
            return self

        def stop(self):
            self.running = False

    # Attach fakes
    sys.modules['pynput.keyboard'].Key = FakeKey
    sys.modules['pynput.keyboard'].KeyCode = FakeKeyCode
    sys.modules['pynput.keyboard'].Listener = FakeListener