import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime   # 新增

def write_json_file(post):
    f_path = Path.cwd().joinpath('static', 'posts', post['slug'], 'index.json')
    f_path.parent.mkdir(parents=True, exist_ok=True)
    json_string = json.dumps(post, ensure_ascii=False, indent=2)
    with open(f_path, 'w', encoding="utf8") as f:
        f.write(json_string)
    print('生成' + str(f_path) + '文件成功')

def download_file(url, local_path):
    local_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(local_path, 'wb') as f:
        f.write(response.content)

def sync_data():
    try:
        # 同步 category.json
        category_path = Path.cwd().joinpath('static', 'config', 'category.json')
        url_cat = 'https://raw.githubusercontent.com/gmaox/gmaox.github.io/main/blog/static/config/category.json'
        download_file(url_cat, category_path)
        # 同步 posts.json
        db_path = Path.cwd().joinpath('static', 'config', 'posts.json')
        url_db = 'https://raw.githubusercontent.com/gmaox/gmaox.github.io/main/blog/static/config/posts.json'
        download_file(url_db, db_path)
        messagebox.showinfo("成功", "数据同步完成！")
    except Exception as e:
        messagebox.showerror("同步失败", str(e))

def get_category(category):
    category_path = Path.cwd().joinpath('static', 'config', 'category.json')
    if not category_path.exists():
        messagebox.showerror("错误", "数据库文件不存在！")
        return
    with open(category_path, 'rb') as json_file:
        categories = json.load(json_file)
        for cate in categories:
            if category == cate['name']:
                return cate['slug']
    return category

def insert_db(post):
    db_path = Path.cwd().joinpath('static', 'config', 'posts.json')
    if not db_path.exists():
        messagebox.showerror("错误", "数据库文件不存在！")
        return
    with open(db_path, 'rb') as json_file:
        json_data = json.load(json_file)
    json_data.insert(0, post)
    json_string = json.dumps(json_data, ensure_ascii=False, indent=2)
    with open(db_path, 'w', encoding="utf8") as f:
        f.write(json_string)
    print('插入数据库成功')

def submit():
    title = title_var.get()
    description = desc_var.get()
    date = date_var.get()
    category = cat_var.get()
    slug = slug_var.get()
    body = body_text.get("1.0", tk.END).strip()  # 获取正文内容
    if not (title and description and date and category and slug and body):
        messagebox.showerror("错误", "所有字段都不能为空！")
        return
    post = {
        "title": title,
        "description": description,
        "status": "published",
        "date": date,
        "dateModified": "",
        "coverImage": "",
        "category": get_category(category),
        "slug": slug
    }
    try:
        write_json_file(post)
        insert_db(post)
        # 写入正文到 index.md
        md_path = Path.cwd().joinpath('static', 'posts', slug, 'index.md')
        md_path.parent.mkdir(parents=True, exist_ok=True)
        with open(md_path, 'w', encoding='utf8') as f:
            f.write(f"# {title}\n{body}")
        messagebox.showinfo("成功", "文章信息已保存！")
    except Exception as e:
        messagebox.showerror("错误", str(e))

def load_categories():
    category_path = Path.cwd().joinpath('static', 'config', 'category.json')
    if not category_path.exists():
        return []
    with open(category_path, 'r', encoding='utf8') as f:
        categories = json.load(f)
    return [c['name'] for c in categories]

def update_desc_from_body(event=None):
    body = body_text.get("1.0", tk.END).strip()
    if len(body) > 37:
        desc = body[:37] + "......"
    else:
        desc = body
    desc_var.set(desc)

root = tk.Tk()
root.title("文章信息编辑器")

tk.Label(root, text="标题:").grid(row=0, column=0, sticky='e')
tk.Label(root, text="描述:").grid(row=1, column=0, sticky='e')
tk.Label(root, text="日期:").grid(row=2, column=0, sticky='e')
tk.Label(root, text="分类:").grid(row=3, column=0, sticky='e')
tk.Label(root, text="英文标签:").grid(row=4, column=0, sticky='e')
tk.Label(root, text="正文:").grid(row=5, column=0, sticky='ne')  # 新增正文标签

title_var = tk.StringVar()
desc_var = tk.StringVar()
date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 默认当前时间
cat_var = tk.StringVar()
slug_var = tk.StringVar()

# 加载分类选项
category_list = load_categories()
if not category_list:
    sync_data()  # 没有分类时自动同步一次
    category_list = load_categories()
if category_list:
    cat_var.set(category_list[0])  # 默认选中第一个
else:
    cat_var.set("")  # 没有分类时设为空

tk.Entry(root, textvariable=title_var, width=40).grid(row=0, column=1)
tk.Entry(root, textvariable=desc_var, width=40).grid(row=1, column=1)
tk.Entry(root, textvariable=date_var, width=40).grid(row=2, column=1)
tk.OptionMenu(root, cat_var, *category_list).grid(row=3, column=1, sticky='ew')
tk.Entry(root, textvariable=slug_var, width=40).grid(row=4, column=1)

# 新增正文多行文本框
body_text = tk.Text(root, width=40, height=12)
body_text.grid(row=5, column=1, pady=5)
body_text.bind("<KeyRelease>", update_desc_from_body)  # 绑定事件

tk.Button(root, text="同步数据", command=sync_data).grid(row=6, column=0)
tk.Button(root, text="保存文章", command=lambda: submit()).grid(row=6, column=1, columnspan=2, pady=5)

root.mainloop()