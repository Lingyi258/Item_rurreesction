import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from user import UserManagement

if __name__ == "__main__":
    app = QApplication(sys.argv)
    usermanagement = UserManagement("users.json", "admins.json")
    usermanagement.show()
    sys.exit(app.exec_())
