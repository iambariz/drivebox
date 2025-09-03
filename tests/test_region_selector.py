import pytest
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QMouseEvent, QKeyEvent
from drivebox.region_selector import RegionSelector


def test_mouse_press_and_move_and_release(qtbot):
    selector = RegionSelector()
    qtbot.addWidget(selector)

    # Simulate mouse press at (10, 10)
    press_event = QMouseEvent(QMouseEvent.MouseButtonPress, QPoint(10, 10),
                              Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
    selector.mousePressEvent(press_event)
    assert selector.start == QPoint(10, 10)
    assert selector.end == QPoint(10, 10)

    # Simulate mouse move to (50, 50)
    move_event = QMouseEvent(QMouseEvent.MouseMove, QPoint(50, 50),
                             Qt.NoButton, Qt.LeftButton, Qt.NoModifier)
    selector.mouseMoveEvent(move_event)
    assert selector.end == QPoint(50, 50)

    # Simulate mouse release at (100, 100)
    release_event = QMouseEvent(QMouseEvent.MouseButtonRelease, QPoint(100, 100),
                                Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
    selector.mouseReleaseEvent(release_event)

    assert isinstance(selector.selected_rect, QRect)
    assert selector.selected_rect.topLeft() == QPoint(10, 10)
    assert selector.selected_rect.bottomRight() == QPoint(100, 100)


def test_key_press_escape(qtbot):
    selector = RegionSelector()
    qtbot.addWidget(selector)

    # Simulate pressing Escape
    key_event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Escape, Qt.NoModifier)
    selector.keyPressEvent(key_event)

    assert selector.selected_rect is None
    # Dialog should be rejected
    assert selector.result() == selector.Rejected


def test_paint_event_runs(qtbot):
    selector = RegionSelector()
    qtbot.addWidget(selector)

    # Set start and end so paintEvent draws a rect
    selector.start = QPoint(10, 10)
    selector.end = QPoint(50, 50)

    # Call paintEvent manually with a fake event
    class DummyEvent:
        pass

    selector.paintEvent(DummyEvent())
