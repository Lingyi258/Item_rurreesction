
# 物品复活软件

## 项目简介

本项目为上海交通大学《软件工程》课程第一次课后作业，“物品复活“软件开发，要求如下：
>大学生经常有些物品觉得扔掉可惜，不处理又觉得浪费自己的地方。请你编写一个物品“复活”软件
>该程序允许添加物品的信息（物品名称，物品描述，联系人信息），删除物品的信息，显示物品列表，也允许查找物品的信息
>你实现的程序可以采用命令行方式使用，但是鼓励提供GUI


## 功能

- **添加物品**：用户可以输入物品名称、描述和联系人信息，并将其添加到列表中。
- **删除物品**：用户可以从列表中选择一个物品并将其删除。
- **查找物品**：用户可以根据物品名称、描述或联系人信息进行查找，支持模糊匹配。
- **数据持久性**：所有数据存储在 JSON 文件中，程序启动时会加载数据。

## 环境要求

- Python 3.6 或更高版本
- PyQt5
- JSON 模块（Python 内置）

## 安装

1. 确保已安装 Python 3.x，建议使用 [Anaconda](https://www.anaconda.com/products/distribution) 或 [Python 官网](https://www.python.org/downloads/) 进行安装。
2. 安装 PyQt5：
   ```bash
   pip install PyQt5
   ```

## 使用方法

1. 克隆仓库或下载源代码：
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. 运行程序：
   ```bash
   python main.py
   ```

3. 使用界面输入物品信息，点击“添加物品”将其保存到列表中。

4. 可通过输入框进行查找，若未输入任何条件，将提示用户至少输入一个查找条件。

## 数据结构

物品信息存储在 `items.json` 文件中，每个物品以字典形式存储，结构如下：

```json
[
    {
        "name": "物品名称",
        "description": "物品描述",
        "contact": "联系人信息"
    },
    ...
]
```

## 注意事项

- 程序首次运行时，如果没有找到 `items.json` 文件，将自动生成一个空文件。
- 确保 JSON 文件格式正确，以避免加载错误。


