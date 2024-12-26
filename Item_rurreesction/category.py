import json

class Category:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

class CategoryManagement:
    def __init__(self, filename="categories.json"):
        self.categories = {}
        self.filename = filename
        self.load_data()

    def add_category(self, name, attributes):
        if name in self.categories:
            print(f"类别 {name} 已存在。")
        else:
            self.categories[name] = Category(name, attributes)
            self.save_data()
            print(f"类别 {name} 添加成功。")

    def modify_category(self, name, new_name=None, new_attributes=None):
        if name not in self.categories:
            print(f"类别 {name} 不存在。")
        else:
            if new_name:
                self.categories[name].name = new_name
            if new_attributes:
                self.categories[name].attributes = new_attributes
            self.save_data()
            print(f"类别 {name} 修改成功。")

    def delete_category(self, name):
        if name in self.categories:
            del self.categories[name]
            self.save_data()
            print(f"类别 {name} 删除成功。")
        else:
            print(f"类别 {name} 不存在。")

    def display_all_categories(self):
        if not self.categories:
            print("没有任何类别。")
        else:
            for name, category in self.categories.items():
                print(f"类别名称: {name}, 属性: {category.attributes}")

    def load_data(self):
        try:
            with open(self.filename, 'r', encoding="utf8") as file:
                data = json.load(file)
                self.categories = {name: Category(**category) for name, category in data.get('categories', {}).items()}
        except FileNotFoundError:
            print(f"文件 {self.filename} 未找到。初始化为空类别字典。")
            self.categories = {}
        except json.JSONDecodeError as e:
            print(f"解析JSON时出错:{e}。初始化为空类别字典。")
            self.categories = {}
        except Exception as e:
            print(f"加载类别信息时出错：{e}")

    def save_data(self):
        try:
            data = {'categories': {name: category.__dict__ for name, category in self.categories.items()}}
            with open(self.filename, 'w', encoding="utf8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存类别信息时出错：{e}")