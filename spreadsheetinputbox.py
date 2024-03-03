
from PySide6.QtWidgets import *


class InputBox(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()

        self.input_label = QLabel("Enter your input:")
        layout.addWidget(self.input_label)

        self.input_line_edit = QLineEdit()
        layout.addWidget(self.input_line_edit)

        self.store_button = QPushButton("Store Input")
        self.store_button.clicked.connect(self.store_input)
        layout.addWidget(self.store_button)

        self.display_label = QLabel("Stored input will appear here.")
        layout.addWidget(self.display_label)

        self.setLayout(layout)
        

    def store_input(self):
        input_text = self.input_line_edit.text()
        self.display_label.setText(f"Stored input: {input_text}")