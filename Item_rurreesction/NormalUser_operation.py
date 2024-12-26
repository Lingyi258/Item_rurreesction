import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QComboBox, QFormLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from item import Item
from category import CategoryManagement

class NormalUserOperation(QWidget):
    def __init__(self):
        super().__init__()
        self.items = []
        self.category_management = CategoryManagement()
        self.initUI()
        self.load_items()

    def initUI(self):
        self.setWindowTitle("普通用户物品管理")
        self.resize(800, 600)

        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        add_button = QPushButton("添加物品")
        add_button.clicked.connect(self.show_add_item_form)
        delete_button = QPushButton("删除物品")
        delete_button.clicked.connect(self.show_delete_item_form)
        search_button = QPushButton("查找物品")
        search_button.clicked.connect(self.show_search_item_form)
        display_button = QPushButton("显示全部物品")
        display_button.clicked.connect(self.display_items)

        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(search_button)
        button_layout.addWidget(display_button)

        layout.addLayout(button_layout)

        self.form_layout = QFormLayout()
        layout.addLayout(self.form_layout)

        self.items_table = QTableWidget()
        self.items_table.setColumnCount(7)
        self.items_table.setHorizontalHeaderLabels(["物品类别","物品名称", "物品说明", "物品所在地址", "联系人手机", "联系人邮箱", "附加属性"])
        layout.addWidget(self.items_table)

        self.setLayout(layout)

    def show_add_item_form(self):
        self.clear_form_layout()
        self.item_category_input = QComboBox()
        self.item_category_input.addItems(self.category_management.categories.keys())
        self.item_category_input.currentIndexChanged.connect(self.update_additional_attributes_placeholder)
        self.item_name_input = QLineEdit()
        self.item_description_input = QLineEdit()
        self.item_address_input = QLineEdit()
        self.item_contact_phone_input = QLineEdit()
        self.item_contact_email_input = QLineEdit()
        self.item_additional_attributes_input = QLineEdit()

        self.form_layout.addRow("物品类型：", self.item_category_input)
        self.form_layout.addRow("物品名称：", self.item_name_input)
        self.form_layout.addRow("物品说明：", self.item_description_input)
        self.form_layout.addRow("物品所在地址：", self.item_address_input)
        self.form_layout.addRow("联系人手机：", self.item_contact_phone_input)
        self.form_layout.addRow("联系人邮箱：", self.item_contact_email_input)
        self.form_layout.addRow("附加属性（逗号分隔）：", self.item_additional_attributes_input)

        add_button = QPushButton("添加物品")
        add_button.clicked.connect(self.add_item)
        self.form_layout.addRow(add_button)

    def update_additional_attributes_placeholder(self):
        category = self.item_category_input.currentText()
        if category in self.category_management.categories:
            attributes = self.category_management.categories[category].attributes
            self.item_additional_attributes_input.setPlaceholderText("，".join(attributes))

    def show_delete_item_form(self):
        self.clear_form_layout()
        self.delete_item_name_input = QLineEdit()
        delete_button = QPushButton("删除物品")
        delete_button.clicked.connect(self.delete_item)

        self.form_layout.addRow("物品名称：", self.delete_item_name_input)
        self.form_layout.addRow(delete_button)

    def show_search_item_form(self):
        self.clear_form_layout()
        self.search_item_category_input = QComboBox()
        self.search_item_category_input.addItems(self.category_management.categories.keys())
        self.search_item_keyword_input = QLineEdit()
        search_button = QPushButton("查找物品")
        search_button.clicked.connect(self.search_item)

        self.form_layout.addRow("物品类型：", self.search_item_category_input)
        self.form_layout.addRow("关键字：", self.search_item_keyword_input)
        self.form_layout.addRow(search_button)

    def clear_form_layout(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_items(self):
        try:
            with open("items.json", 'r', encoding="utf8") as file:
                items_data = json.load(file)
                self.items = [Item(**item) for item in items_data]
                self.display_items()
        except FileNotFoundError:
            print("文件 items.json 未找到。初始化为空物品列表。")
            self.items = []
        except json.JSONDecodeError as e:
            print(f"解析JSON时出错:{e}。初始化为空物品列表。")
            self.items = []
        except Exception as e:
            print(f"加载物品信息时出错：{e}")

    def save_items(self):
        try:
            items_data = [item.__dict__ for item in self.items]
            with open("items.json", 'w', encoding="utf8") as file:
                json.dump(items_data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存物品信息时出错：{e}")

    def add_item(self):
        name = self.item_name_input.text()
        description = self.item_description_input.text()
        address = self.item_address_input.text()
        contact_phone = self.item_contact_phone_input.text()
        contact_email = self.item_contact_email_input.text()
        category = self.item_category_input.currentText()
        additional_attributes_text = self.item_additional_attributes_input.text()

        if not all([name, description, address, contact_phone, contact_email, category, additional_attributes_text]):
            QMessageBox.warning(self, "添加失败", "请填写所有字段。")
            return

        if any(item.name == name for item in self.items):
            QMessageBox.warning(self, "添加失败", "物品名称不能重复。")
            return

        category_attributes = self.category_management.categories[category].attributes
        additional_attributes_values = additional_attributes_text.split(',')
        if len(category_attributes) != len(additional_attributes_values):
            QMessageBox.warning(self, "添加失败", "附加属性数量不匹配，请检查输入。")
            return

        additional_attributes = dict(zip(category_attributes, additional_attributes_values))

        item = Item(name, description, address, contact_phone, contact_email, category, additional_attributes)
        self.items.append(item)
        self.save_items()
        self.display_items()
        QMessageBox.information(self, "添加成功", "物品添加成功。")

    def delete_item(self):
        name = self.delete_item_name_input.text()
        if not name:
            QMessageBox.warning(self, "删除失败", "物品名称不能为空。")
            return

        self.items = [item for item in self.items if item.name != name]
        self.save_items()
        self.display_items()
        QMessageBox.information(self, "删除成功", "物品删除成功。")

    def search_item(self):
        category = self.search_item_category_input.currentText()
        keyword = self.search_item_keyword_input.text().lower()
        results = [item for item in self.items if item.category == category and (keyword in item.name.lower() or keyword in item.description.lower())]

        self.items_table.setRowCount(0)
        for item in results:
            row_position = self.items_table.rowCount()
            self.items_table.insertRow(row_position)
            self.items_table.setItem(row_position, 0, QTableWidgetItem(item.category))           
            self.items_table.setItem(row_position, 1, QTableWidgetItem(item.name))
            self.items_table.setItem(row_position, 2, QTableWidgetItem(item.description))
            self.items_table.setItem(row_position, 3, QTableWidgetItem(item.address))
            self.items_table.setItem(row_position, 4, QTableWidgetItem(item.contact_phone))
            self.items_table.setItem(row_position, 5, QTableWidgetItem(item.contact_email))
            self.items_table.setItem(row_position, 6, QTableWidgetItem(json.dumps(item.additional_attributes, ensure_ascii=False)))


    def display_items(self):
        self.items_table.setRowCount(0)
        for item in self.items:
            row_position = self.items_table.rowCount()
            self.items_table.insertRow(row_position)
            self.items_table.setItem(row_position, 0, QTableWidgetItem(item.category))           
            self.items_table.setItem(row_position, 1, QTableWidgetItem(item.name))
            self.items_table.setItem(row_position, 2, QTableWidgetItem(item.description))
            self.items_table.setItem(row_position, 3, QTableWidgetItem(item.address))
            self.items_table.setItem(row_position, 4, QTableWidgetItem(item.contact_phone))
            self.items_table.setItem(row_position, 5, QTableWidgetItem(item.contact_email))
            self.items_table.setItem(row_position, 6, QTableWidgetItem(json.dumps(item.additional_attributes, ensure_ascii=False)))

