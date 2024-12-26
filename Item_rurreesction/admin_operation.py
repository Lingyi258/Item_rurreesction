import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QRadioButton, QButtonGroup,
    QTabWidget, QFormLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from category import CategoryManagement

class AdminOperation(QWidget):
    def __init__(self, user_management):
        super().__init__()
        self.user_management = user_management
        self.category_management = CategoryManagement()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("管理员操作")
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_approval_tab(), "审批注册申请")
        self.tabs.addTab(self.create_category_tab(), "类别管理")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_approval_tab(self):
        approval_tab = QWidget()
        layout = QVBoxLayout()

        self.approval_table = QTableWidget()
        self.approval_table.setColumnCount(4)
        self.approval_table.setHorizontalHeaderLabels(["用户名", "地址", "联系方式", "批准"])
        layout.addWidget(self.approval_table)

        self.load_approval_data()

        approval_tab.setLayout(layout)
        return approval_tab

    def load_approval_data(self):
        self.approval_table.setRowCount(0)
        for username, user in self.user_management.users.items():
            if not user.is_approved:
                row_position = self.approval_table.rowCount()
                self.approval_table.insertRow(row_position)
                self.approval_table.setItem(row_position, 0, QTableWidgetItem(username))
                self.approval_table.setItem(row_position, 1, QTableWidgetItem(user.address))
                self.approval_table.setItem(row_position, 2, QTableWidgetItem(user.contact_info))
                approve_button = QPushButton("批准")
                approve_button.clicked.connect(lambda _, u=username: self.approve_user(u))
                self.approval_table.setCellWidget(row_position, 3, approve_button)

    def approve_user(self, username):
        self.user_management.users[username].is_approved = True
        self.user_management.save_data()
        self.load_approval_data()
        QMessageBox.information(self, "批准成功", f"用户 {username} 已批准。")

    def create_category_tab(self):
        category_tab = QWidget()
        layout = QVBoxLayout()

        self.category_table = QTableWidget()
        self.category_table.setColumnCount(2)
        self.category_table.setHorizontalHeaderLabels(["类别名称", "属性"])
        layout.addWidget(self.category_table)

        self.load_category_data()

        form_layout = QFormLayout()
        self.category_name_input = QLineEdit()
        self.category_attributes_input = QLineEdit()
        form_layout.addRow("类别名称：", self.category_name_input)
        form_layout.addRow("属性（逗号分隔）：", self.category_attributes_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton("添加类别")
        add_button.clicked.connect(self.add_category)
        modify_button = QPushButton("修改类别")
        modify_button.clicked.connect(self.modify_category)
        delete_button = QPushButton("删除类别")
        delete_button.clicked.connect(self.delete_category)
        button_layout.addWidget(add_button)
        button_layout.addWidget(modify_button)
        button_layout.addWidget(delete_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        category_tab.setLayout(layout)
        return category_tab

    def load_category_data(self):
        self.category_table.setRowCount(0)
        for name, category in self.category_management.categories.items():
            row_position = self.category_table.rowCount()
            self.category_table.insertRow(row_position)
            self.category_table.setItem(row_position, 0, QTableWidgetItem(name))
            self.category_table.setItem(row_position, 1, QTableWidgetItem(", ".join(category.attributes)))

    def add_category(self):
        name = self.category_name_input.text()
        attributes = self.category_attributes_input.text().split(',')
        self.category_management.add_category(name, attributes)
        self.load_category_data()

    def modify_category(self):
        name = self.category_name_input.text()
        new_attributes = self.category_attributes_input.text().split(',')
        self.category_management.modify_category(name, new_attributes=new_attributes)
        self.load_category_data()

    def delete_category(self):
        name = self.category_name_input.text()
        self.category_management.delete_category(name)
        self.load_category_data()
