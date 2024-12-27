import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QLabel, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from admin_operation import AdminOperation
from NormalUser_operation import ItemManagement

class User:
    def __init__(self, username, password, address, contact_info):
        self.username = username
        self.password = password
        self.address = address
        self.contact_info = contact_info

class Admin(User):
    def __init__(self, username, password, address, contact_info):
        super().__init__(username, password, address, contact_info)

class NormalsUer(User):
    def __init__(self, username, password, address, contact_info, is_approved):
        super().__init__(username, password, address, contact_info)
        self.is_approved = is_approved

class UserManagement(QWidget):
    def __init__(self, user_filename, admin_filename):
        super().__init__()
        self.users = {}
        self.admins = {}
        self.user_filename = user_filename
        self.admin_filename = admin_filename
        self.initUI()
        self.load_data()

    def initUI(self):#包含选择用户类型的按钮，输入用户名和密码的框和按钮，以及注册和登录的按钮
        self.setWindowTitle("用户管理")
        self.resize(500, 300)

        layout = QVBoxLayout()

        title_label = QLabel("请选择用户类型：", self)
        title_font = QFont()
        title_font.setPointSize(18)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 用户类型选择
        self.user_type_group = QButtonGroup(self)
        self.normaluser_radio = QRadioButton("普通用户", self)
        self.admin_radio = QRadioButton("管理员", self)
        self.user_type_group.addButton(self.normaluser_radio)
        self.user_type_group.addButton(self.admin_radio)
        self.normaluser_radio.setChecked(True)  # 默认选择普通用户

        font = QFont()
        font.setPointSize(14)
        for radio in [self.normaluser_radio, self.admin_radio]:
            radio.setFont(font)

        layout.addWidget(self.normaluser_radio)
        layout.addWidget(self.admin_radio)

        # 用户名输入框
        self.username_label = QLabel("用户名：", self)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # 密码输入框
        self.password_label = QLabel("密码：", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # 注册按钮
        self.register_button = QPushButton("注册", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        # 登录按钮
        self.login_button = QPushButton("登录", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def load_data(self):
        try:
            with open(self.user_filename, 'r', encoding="utf8") as file:
                user_data = json.load(file)
                self.users = {user['username']: NormalsUer(**user) for user in user_data}
        except FileNotFoundError:
            print(f"文件 {self.user_filename} 未找到。初始化为空用户字典。")
            self.users = {}
        except json.JSONDecodeError as e:
            print(f"解析JSON时出错:{e}。初始化为空用户字典。")
            self.users = {}
        except Exception as e:
            print(f"加载用户信息时出错：{e}")

        try:
            with open(self.admin_filename, 'r', encoding="utf8") as file:
                admin_data = json.load(file)
                self.admins = {admin['username']: Admin(**admin) for admin in admin_data}
        except FileNotFoundError:
            print(f"文件 {self.admin_filename} 未找到。初始化为空管理员字典。")
            self.admins = {}
        except json.JSONDecodeError as e:
            print(f"解析JSON时出错:{e}。初始化为空管理员字典。")
            self.admins = {}
        except Exception as e:
            print(f"加载管理员信息时出错：{e}")

    def save_data(self):
        try:
            user_data = [user.__dict__ for user in self.users.values()]
            with open(self.user_filename, 'w', encoding="utf8") as file:
                json.dump(user_data, file, indent=4, ensure_ascii=False)

            admin_data = [admin.__dict__ for admin in self.admins.values()]
            with open(self.admin_filename, 'w', encoding="utf8") as file:
                json.dump(admin_data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存用户信息时出错：{e}")

    def register(self):
        if self.normaluser_radio.isChecked():
            self.normaluser_register()
        else:
            self.admin_register()

    def login(self):    
        if self.normaluser_radio.isChecked():
            self.normaluser_login()
        else:
            self.admin_login()

    def normaluser_register(self):#创建一个新窗口，输入用户名、密码、地址、联系方式
        self.register_window = QWidget()
        self.register_window.setWindowTitle("普通用户注册")
        layout = QVBoxLayout()

        self.reg_username_label = QLabel("用户名：", self.register_window)
        self.reg_username_input = QLineEdit(self.register_window)
        layout.addWidget(self.reg_username_label)
        layout.addWidget(self.reg_username_input)

        self.reg_password_label = QLabel("密码：", self.register_window)
        self.reg_password_input = QLineEdit(self.register_window)
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password_label)
        layout.addWidget(self.reg_password_input)

        self.reg_confirm_password_label = QLabel("确认密码：", self.register_window)
        self.reg_confirm_password_input = QLineEdit(self.register_window)
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_confirm_password_label)
        layout.addWidget(self.reg_confirm_password_input)

        self.reg_address_label = QLabel("地址：", self.register_window)
        self.reg_address_input = QLineEdit(self.register_window)
        layout.addWidget(self.reg_address_label)
        layout.addWidget(self.reg_address_input)

        self.reg_contact_label = QLabel("联系方式：", self.register_window)
        self.reg_contact_input = QLineEdit(self.register_window)
        layout.addWidget(self.reg_contact_label)
        layout.addWidget(self.reg_contact_input)

        self.reg_submit_button = QPushButton("提交", self.register_window)
        self.reg_submit_button.clicked.connect(self.submit_normaluser_registration)
        layout.addWidget(self.reg_submit_button)

        self.register_window.setLayout(layout)
        self.register_window.show()

    def admin_register(self):#创建一个新窗口，输入用户名、密码、地址、联系方式
        self.register_window = QWidget()
        self.register_window.setWindowTitle("管理员注册")
        layout = QVBoxLayout()

        self.reg_username_label = QLabel("用户名：", self.register_window)
        self.reg_username_input = QLineEdit(self.register_window)
        layout.addWidget(self.reg_username_label)
        layout.addWidget(self.reg_username_input)

        self.reg_password_label = QLabel("密码：", self.register_window)
        self.reg_password_input = QLineEdit(self.register_window)
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password_label)
        layout.addWidget(self.reg_password_input)

        self.reg_confirm_password_label = QLabel("确认密码：", self.register_window)
        self.reg_confirm_password_input = QLineEdit(self.register_window)
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_confirm_password_label)
        layout.addWidget(self.reg_confirm_password_input)

        self.reg_address_label = QLabel("地址：", self.register_window)
        self.reg_address_input = QLineEdit(self.register_window)
        layout.addWidget(self.reg_address_label)
        layout.addWidget(self.reg_address_input)

        self.reg_contact_label = QLabel("联系方式：", self.register_window)
        self.reg_contact_input = QLineEdit(self.register_window)
        layout.addWidget(self.reg_contact_label)
        layout.addWidget(self.reg_contact_input)

        self.reg_submit_button = QPushButton("提交", self.register_window)
        self.reg_submit_button.clicked.connect(self.submit_admin_registration)
        layout.addWidget(self.reg_submit_button)

        self.register_window.setLayout(layout)
        self.register_window.show()

    def normaluser_login(self):#读取用户名和密码，判断是否正确，不存在则提示错误
        username = self.username_input.text()
        password = self.password_input.text()
        if username in self.users and self.users[username].password == password:
            if not self.users[username].is_approved:
                QMessageBox.warning(self, "登录失败", "您的账户尚未通过审核！")
            else:
                QMessageBox.information(self, "登录成功", "普通用户登录成功！")
                self.normal_user_operation = ItemManagement()
                self.normal_user_operation.show()              
        else:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误！")

    def admin_login(self):#读取用户名和密码，判断是否正确，不存在则提示错误
        username = self.username_input.text()
        password = self.password_input.text()
        if username in self.admins and self.admins[username].password == password:
            QMessageBox.information(self, "登录成功", "管理员登录成功！")
            self.admin_operation = AdminOperation(self)
            self.admin_operation.show()
        else:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误！")

    def submit_normaluser_registration(self):
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()
        address = self.reg_address_input.text()
        contact = self.reg_contact_input.text()
        if password != confirm_password:
            QMessageBox.warning(self, "注册失败", "密码和确认密码不一致。")
            return
        if username in self.users:
            QMessageBox.warning(self.register_window, "注册失败", "用户名已存在！")
        elif username and password and address and contact:
            user = NormalsUer(username, password, address, contact, False)
            self.users[username] = user
            self.save_data()
            QMessageBox.information(self.register_window, "注册成功", "普通用户注册成功！")
            self.register_window.close()
        else:
            QMessageBox.warning(self.register_window, "注册失败", "请填写所有字段！")

    def submit_admin_registration(self):
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()
        address = self.reg_address_input.text()
        contact = self.reg_contact_input.text()
        if password != confirm_password:
            QMessageBox.warning(self, "注册失败", "密码和确认密码不一致。")
            return
        if username in self.admins:
            QMessageBox.warning(self.register_window, "注册失败", "用户名已存在！")
        elif username and password and address and contact:
            admin = Admin(username, password, address, contact)
            self.admins[username] = admin
            self.save_data()
            QMessageBox.information(self.register_window, "注册成功", "管理员注册成功！")
            self.register_window.close()
        else:
            QMessageBox.warning(self.register_window, "注册失败", "请填写所有字段！")
