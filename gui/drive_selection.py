import logging

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHBoxLayout, QListWidget, QPushButton, QVBoxLayout, QWidget

from drive_manager.drive_manager import DriveManager

logger = logging.getLogger("global_logger")

class DriveSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        logger.info("Drive Selection Widget created")
        self.selected_drive = None
        self.drive_manager = DriveManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.drive_list = QListWidget()
        self.drive_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.drive_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #aaa;
                border-radius: 5px;
                background-color: #f5f5f5;
                padding: 10px;
                margin-bottom: 10px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #1E90FF;
                color: white;
            }
        """)
        layout.addWidget(self.drive_list)

        button_layout = QHBoxLayout()

        self.select_btn = QPushButton("Select Drive")
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.select_btn.clicked.connect(self.select_drive)
        button_layout.addWidget(self.select_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_drives)
        self.timer.start(300)

        self.refresh_drives()

    def refresh_drives(self):
        connected_drives = self.get_connected_drives()

        current_items = {item.text() for item in self.drive_list.findItems("*", Qt.MatchFlag.MatchWildcard)}

        for drive in connected_drives:
            if drive not in current_items:
                self.drive_list.addItem(drive)

        for item in self.drive_list.findItems("*", Qt.MatchFlag.MatchWildcard):
            if item.text() not in connected_drives:
                self.drive_list.takeItem(self.drive_list.row(item))

        logger.info("Drive list refreshed")

    def get_connected_drives(self):
        self.drive_manager.refresh()
        return self.drive_manager.drive_list

    def select_drive(self):
        selected_item = self.drive_list.selectedItems()
        if selected_item:
            self.selected_drive = selected_item[0].text()
            logger.info("Selected drive: %s", self.selected_drive)
        else:
            logger.info("No drive selected")
