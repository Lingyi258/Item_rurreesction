import sys
from PyQt5.QtWidgets import QApplication
from user import UserManagement

if __name__ == "__main__":
    app = QApplication(sys.argv)
    usermanagement = UserManagement("users.json", "admins.json")
    usermanagement.show()
    sys.exit(app.exec_())
