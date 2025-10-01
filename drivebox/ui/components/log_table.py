from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from datetime import datetime


class LogTableWidget(QTableWidget):
    """Self-contained log table with time, type, status, result columns."""
    
    COLUMNS = ["Time", "Type", "Status", "Result"]
    
    def __init__(self):
        super().__init__(0, len(self.COLUMNS))
        self.setHorizontalHeaderLabels(self.COLUMNS)
    
    def add_entry(self, event_type: str, status: str, result: str = ""):
        """Add a new log entry."""
        row = self.rowCount()
        self.insertRow(row)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        items = [timestamp, event_type, status, result]
        for col, value in enumerate(items):
            self.setItem(row, col, QTableWidgetItem(value))
