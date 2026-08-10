from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QDialog


class RegionSelector(QDialog):
    def __init__(self, background: QPixmap) -> None:
        super().__init__(
            None,
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint,  # type: ignore[attr-defined]
        )
        self._background = background
        self._origin: QRect | None = None
        self.selected_rect: QRect | None = None

        self.setGeometry(0, 0, background.width(), background.height())
        self.setCursor(Qt.CrossCursor)  # type: ignore[attr-defined]

    def paintEvent(self, event) -> None:  # noqa: N802, ARG002
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._background)

        if self.selected_rect is not None and not self.selected_rect.isEmpty():
            painter.fillRect(self.rect(), QColor(0, 0, 0, 120))
            painter.drawPixmap(self.selected_rect, self._background, self.selected_rect)
            painter.setPen(QPen(Qt.red, 2))  # type: ignore[attr-defined]
            painter.drawRect(self.selected_rect)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        self._origin = event.pos()
        self.selected_rect = QRect(self._origin, self._origin)
        self.update()

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self._origin is not None:
            self.selected_rect = QRect(self._origin, event.pos()).normalized()
            self.update()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802, ARG002
        if self.selected_rect is not None and not self.selected_rect.isEmpty():
            self.accept()
        else:
            self.reject()

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() == Qt.Key_Escape:  # type: ignore[attr-defined]
            self.reject()
