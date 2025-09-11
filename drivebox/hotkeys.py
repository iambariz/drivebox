class HotkeyManager:
    def __init__(self, bridge):
        self.registered_hotkeys = {}
        self.listener = None
        self.bridge = bridge

    def parse_hotkey(self, hotkey_str):
        from pynput import keyboard
        keys = set()
        for part in hotkey_str.lower().split('+'):
            part = part.strip()
            mapping = {
                "ctrl": keyboard.Key.ctrl_l,
                "alt": keyboard.Key.alt_l,
                "shift": keyboard.Key.shift_l,
            }
            if part in mapping:
                keys.add(mapping[part])
            elif len(part) == 1:
                keys.add(keyboard.KeyCode(char=part))
        return frozenset(keys)

    def register_hotkey(self, hotkey_str, callback_name, hotkey_name):
        keys = self.parse_hotkey(hotkey_str)
        self.registered_hotkeys[keys] = (callback_name, hotkey_name)
        print(f"Registered hotkey '{hotkey_name}': {hotkey_str}")
        self.start_listener()

    def start_listener(self):
        from pynput import keyboard
        if not self.registered_hotkeys:
            return

        if self.listener:
            try:
                self.listener.stop()
            except:
                pass

        current_keys = set()

        def on_press(key):
            current_keys.add(key)
            for keys_combo, (callback_name, _) in self.registered_hotkeys.items():
                if all(k in current_keys for k in keys_combo):
                    self.bridge.hotkey_activated.emit(callback_name)
                    break

        def on_release(key):
            current_keys.discard(key)

        self.listener = keyboard.Listener(
            on_press=on_press, on_release=on_release
        )
        self.listener.daemon = True
        self.listener.start()
        print(
            f"Started global keyboard listener with {len(self.registered_hotkeys)} hotkeys"
        )