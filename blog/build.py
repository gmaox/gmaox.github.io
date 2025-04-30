import sys
import json
import pathlib
from pathlib import Path
import re

def markdown(md_file):
    slug = pathlib.PurePath(md_file).parts[-2]
    f = open(md_file,'r',encoding="utf8")
    title = meta(f.readline())
    description =  meta(f.readline())
    date =  meta(f.readline())
    coverImage =  meta(f.readline())
    category =  get_category(meta(f.readline()))
    post = {
        "title": title,
        "description": description,
        "status": "published",
        "date": date,
        "dateModified": "",
        "coverImage": coverImage,
        "category": category,
        "slug": slug
    }
    write_json_file(post)
    insert_db(post)
    f.close()


def meta(line):
    return re.search('\[.+\]:.+\((.+)\)', line).group(1).strip()

def write_json_file(post):
    f_path = Path.cwd().joinpath('static','posts',post['slug'], 'index.json')
    json_string = json.dumps(post,ensure_ascii=False)
    f = open(f_path,'w', encoding="utf8")
    f.write(json_string)
    f.close()
    print('生成' + str(f_path) + '文件成功')

def get_category(category):
    category_path = Path.cwd().joinpath('static','config','category.json')
    with open(category_path, 'rb') as json_file:
        categories = json.load(json_file)
        for cate in categories:
            if category == cate['name']:
                return cate['slug']
    return category

def insert_db(post):
    db_path = Path.cwd().joinpath('static','config','posts.json')
    with open(db_path, 'rb') as json_file:
        json_data = json.load(json_file)
        json_data.insert(0,post)
        json_string = json.dumps(json_data,ensure_ascii=False)
        f = open(db_path,'w',encoding="utf8")
        f.write(json_string)
        f.close()
        print('插入数据库成功')


if __name__ == '__main__':
    markdown(sys.argv[1])