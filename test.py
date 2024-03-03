from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QSize, Qt

class IntegerTableWidgetItem(QTableWidgetItem):
    def __init__(self, value):
        super().__init__()
        self.setValue(value)

    def setValue(self, value):
        self.setData(Qt.DisplayRole, value)

    def value(self):
        return int(self.data(Qt.DisplayRole))

# Usage:
integer_item = IntegerTableWidgetItem(42)
print(integer_item.value())  # Output: 42


