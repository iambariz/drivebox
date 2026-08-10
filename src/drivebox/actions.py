from dataclasses import dataclass


@dataclass(frozen=True)
class CaptureAction:
    id: str
    label: str
    hotkey: str


CAPTURE_ACTIONS = [
    CaptureAction(id="screenshot", label="Take Screenshot", hotkey="<ctrl>+<shift>+s"),
    CaptureAction(id="region", label="Capture Region", hotkey="<ctrl>+<shift>+r"),
]
