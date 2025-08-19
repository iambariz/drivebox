import os, sys, types

if os.environ.get("CI") == "true":
    # Remove real pynput if already imported
    sys.modules.pop("pynput", None)
    sys.modules.pop("pynput.keyboard", None)

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

    sys.modules['pynput.keyboard'].Key = FakeKey
    sys.modules['pynput.keyboard'].KeyCode = FakeKeyCode
    sys.modules['pynput.keyboard'].Listener = FakeListener