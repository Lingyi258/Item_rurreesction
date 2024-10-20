import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ItemManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_data()

    def initUI(self):
        self.setWindowTitle("物品复活软件")
        self.resize(1500, 1000)  # 设置窗口大小

        # 布局
        layout = QVBoxLayout()

        # 添加标签
        title_label = QLabel("请输入物品信息：", self)
        title_font = QFont()
        title_font.setPointSize(18)  # 设置标签字体大小
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)  # 标签居中
        layout.addWidget(title_label)

        # 输入区域
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("物品名称")
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("物品描述")
        self.contact_input = QLineEdit(self)
        self.contact_input.setPlaceholderText("联系人信息")

        # 调整字体大小
        font = QFont()
        font.setPointSize(14)  # 设置输入框字体大小
        self.name_input.setFont(font)
        self.description_input.setFont(font)
        self.contact_input.setFont(font)

        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.contact_input)

        # 按钮
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加物品", self)
        self.add_button.clicked.connect(self.add_item)
        self.delete_button = QPushButton("删除物品", self)
        self.delete_button.clicked.connect(self.delete_item)
        self.search_button = QPushButton("查找物品", self)
        self.search_button.clicked.connect(self.search_item)
        self.return_button = QPushButton("返回", self)
        self.return_button.clicked.connect(self.return_to_full_list)
        self.return_button.setVisible(False)  # 初始隐藏

        # 设置按钮字体
        for button in [self.add_button, self.delete_button, self.search_button, self.return_button]:
            button.setFont(font)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.return_button)

        layout.addLayout(button_layout)

        # 物品列表
        self.item_table = QTableWidget(self)
        self.item_table.setColumnCount(3)
        self.item_table.setHorizontalHeaderLabels(["物品名称", "物品描述", "联系人信息"])
        layout.addWidget(self.item_table)

        # 设置表格属性
        self.item_table.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁止编辑
        self.item_table.horizontalHeader().setStretchLastSection(True)  # 自动调整最后一列宽度
        self.item_table.setAlternatingRowColors(True)  # 交替行颜色
        self.item_table.setColumnWidth(0, 300)  # 设置列宽
        self.item_table.setColumnWidth(1, 600)
        self.item_table.setColumnWidth(2, 300)

        # 设置表格字体
        self.item_table.setFont(font)

        # 设置表头字体
        header_font = QFont()
        header_font.setPointSize(16)  # 设置表头字体大小
        self.item_table.horizontalHeader().setFont(header_font)


        self.setLayout(layout)

    def load_data(self):
        """ 从JSON文件加载数据 """
        try:
            with open('items.json', 'r', encoding='utf-8') as f:
                self.items = json.load(f)
                self.update_item_table()
        except FileNotFoundError:
            self.items = []
            # 创建一个新的空 JSON 文件
            with open('items.json', 'w', encoding='utf-8') as f:
                json.dump(self.items, f, ensure_ascii=False, indent=4)

    def save_data(self):
        """ 将数据保存到JSON文件 """
        with open('items.json', 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)

    def update_item_table(self):
        """ 更新物品列表显示 """
        self.item_table.setRowCount(0)  # 清空表格
        for item in self.items:
            row_position = self.item_table.rowCount()
            self.item_table.insertRow(row_position)
            self.item_table.setItem(row_position, 0, QTableWidgetItem(item['name']))
            self.item_table.setItem(row_position, 1, QTableWidgetItem(item['description']))
            self.item_table.setItem(row_position, 2, QTableWidgetItem(item['contact']))

        # 设置居中对齐
        for i in range(self.item_table.rowCount()):
            for j in range(3):
                self.item_table.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def add_item(self):
        """ 添加物品 """
        name = self.name_input.text()
        description = self.description_input.text()
        contact = self.contact_input.text()

        if name and description and contact:
            item = {'name': name, 'description': description, 'contact': contact}
            self.items.append(item)
            self.save_data()
            self.update_item_table()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "警告", "请填写所有字段！")

    def delete_item(self):
        """ 删除选中的物品 """
        selected_row = self.item_table.currentRow()
        if selected_row >= 0:
            del self.items[selected_row]
            self.save_data()
            self.update_item_table()
        else:
            QMessageBox.warning(self, "警告", "请选中一个物品进行删除！")

    def search_item(self):
        """ 查找物品 """
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()
        contact = self.contact_input.text().strip()

        # 检查三个值是否均为空
        if not name and not description and not contact:
            QMessageBox.warning(self, "警告", "请至少输入一个查找条件！")
            return

        results = [
            item for item in self.items
            if (name in item['name'] if name else True) and
               (description in item['description'] if description else True) and
               (contact in item['contact'] if contact else True)
        ]

        self.item_table.setRowCount(0)  # 清空表格
        for item in results:
            row_position = self.item_table.rowCount()
            self.item_table.insertRow(row_position)
            self.item_table.setItem(row_position, 0, QTableWidgetItem(item['name']))
            self.item_table.setItem(row_position, 1, QTableWidgetItem(item['description']))
            self.item_table.setItem(row_position, 2, QTableWidgetItem(item['contact']))

        # 设置居中对齐
        for i in range(self.item_table.rowCount()):
            for j in range(3):
                self.item_table.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 显示返回按钮
        self.return_button.setVisible(True)

        if not results:
            QMessageBox.information(self, "信息", "未找到匹配的物品。")

    def return_to_full_list(self):
        """ 返回完整物品列表 """
        self.update_item_table()
        self.return_button.setVisible(False)  # 隐藏返回按钮
        self.clear_inputs()

    def clear_inputs(self):
        """ 清空输入框 """
        self.name_input.clear()
        self.description_input.clear()
        self.contact_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = ItemManager()
    manager.resize(1500, 1000)  # 设置窗口大小
    manager.show()
    sys.exit(app.exec_())