from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QPen

class RegionSelector(QDialog):
    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Select Region")

        # Set transparency attributes BEFORE showing the window
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        # Initialize variables
        self.start = None
        self.end = None
        self.selected_rect = None

        # Set cursor
        self.setCursor(Qt.CrossCursor)

        # Make the dialog cover the whole screen
        self.showFullScreen()

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
        self.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.selected_rect = None
            self.reject()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # IMPORTANT: Create a semitransparent overlay (light enough to see through)
        overlay = QColor(0, 0, 0, 50)  # 50 is the opacity (0-255)
        painter.fillRect(self.rect(), overlay)

        if self.start and self.end:
            rect = QRect(self.start, self.end).normalized()

            # Clear the selection area (make it fully transparent)
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(rect, Qt.transparent)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            # Draw white outer border
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.drawRect(rect)

            # Draw black inner border for better visibility
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(rect.adjusted(1, 1, -1, -1))

            # Show dimensions
            text = f"{rect.width()} × {rect.height()}"
            text_rect = QRect(rect.right() - 80, rect.bottom() + 5, 80, 20)
            painter.fillRect(text_rect, QColor(0, 0, 0, 180))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(text_rect, Qt.AlignCenter, text)
