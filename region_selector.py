from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor

class RegionSelector(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Region")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.start = None
        self.end = None
        self.selected_rect = None

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.end = self.start
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.selected_rect = QRect(self.start, self.end).normalized()
        self.accept()  # Close the dialog and return

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.selected_rect = None
            self.reject()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Draw a semi-transparent gray overlay
        painter.fillRect(self.rect(), QColor(0, 0, 0, 80))
        # Draw the selection rectangle if dragging
        if self.start and self.end:
            rect = QRect(self.start, self.end).normalized()
            # Draw a more transparent gray inside the rectangle
            painter.fillRect(rect, QColor(200, 200, 200, 40))
            # Draw a black border
            painter.setPen(QColor(0, 0, 0, 200))
            painter.drawRect(rect)
