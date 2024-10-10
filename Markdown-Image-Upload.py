import re
import os
import shutil
import sys

markdown_file = sys.argv[1]
with open(markdown_file, 'r', encoding='utf-8') as f:
    content = f.read()

image_pattern = r'!\[.*?\]\((.*?)\)'
image_paths = re.findall(image_pattern, content)
current_directory = os.getcwd()

for image_path in image_paths:
    if os.path.exists(image_path):
        image_name = os.path.basename(image_path)
        
        destination = os.path.join(current_directory, 'result', image_name)
        shutil.copy(image_path, destination)
        print(f"已将图片 {image_name} 复制到当前目录")
    else:
        print(f"图片路径 {image_path} 不存在或不是本地路径")

print("图片处理完成。")