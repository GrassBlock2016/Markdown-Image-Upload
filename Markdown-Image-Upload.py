import re
import sys
import requests
import time
import os
from requests.exceptions import SSLError

def get_local_img(markdown_file):
    """
    正则匹配Markdown文件中的本地图片路径
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    image_pattern = r'!\[.*?\]\((?!https?://)(.*?)\)'
    image_local_path = re.findall(image_pattern, content)
    return image_local_path

def get_network_img(image_local, token, max_retries=3):
    """
    上传本地图片到SM.MS并获取网络图片地址
    """
    if not os.path.isfile(image_local):
        print(f"图片不存在: {image_local}")
        return None
    
    upload_url = 'https://smms.app/api/v2/upload'
    headers = {
        'Authorization': token
    }

    for attempt in range(max_retries):
        try:
            with open(image_local, 'rb') as img_file:
                files = {'smfile': img_file}
                response = requests.post(upload_url, files=files, headers=headers)
            
            if response.status_code == 200:
                res_data = response.json()
                if res_data['success']:
                    return res_data['data']['url']
                elif "Image upload repeated limit" in res_data['message']:
                    return res_data['images']
                else:
                    print(f"上传失败: {res_data['message']}")
                    return None
            else:
                print(f"HTTP 请求错误: {response.status_code}")
                return None

        except SSLError as e:
            print(f"SSL错误: {e}")
            if attempt < max_retries - 1:
                print("等待20秒后重试...")
                time.sleep(20)
            else:
                print("达到最大重试次数，跳过该图片")
                return None

def replace_single_img(markdown_file, img_local_path, img_network_path):
    """
    替换Markdown文件中的单个图片路径
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(img_local_path, img_network_path)
    print(f"\n已将图片 {img_local_path} 替换为 {img_network_path}")

    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(content)

def print_progress_bar(processed, total, width=50):
    """
    打印进度条
    """
    percent = processed / total
    bar_length = int(width * percent)
    bar = '■' * bar_length + '□' * (width - bar_length)
    progress_text = f"\r进度: [{bar}] {processed}/{total} 图片 ({percent:.1%})"
    
    # 清除当前行并打印进度条
    print(progress_text, end='', flush=True)

def process_images(markdown_file, authorization, upload_limit_per_minute=20):
    img_local_paths = get_local_img(markdown_file)
    total_images = len(img_local_paths)
    processed_images = 0
    upload_count = 0
    start_time = time.time()

    print_progress_bar(processed_images, total_images)

    for img_local_path in img_local_paths:
        img_network_path = get_network_img(img_local_path, authorization)
        
        if img_network_path:
            replace_single_img(markdown_file, img_local_path, img_network_path)
            upload_count += 1
            processed_images += 1

            print_progress_bar(processed_images, total_images)

            # 处理上传限制
            if upload_count >= upload_limit_per_minute:
                elapsed_time = time.time() - start_time
                if elapsed_time < 65:
                    wait_time = 65 - elapsed_time
                    print(f"\n达到每分钟上传限制，等待 {wait_time:.2f} 秒...")
                    time.sleep(wait_time)
                    print_progress_bar(processed_images, total_images)
                upload_count = 0
                start_time = time.time()
        else:
            print(f"\n跳过图片 {img_local_path} 的处理")
            processed_images += 1
            print_progress_bar(processed_images, total_images)

    print("\n所有图片均已处理完成。")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("使用方法: python script.py <markdown文件路径> <authorization_token>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    authorization = sys.argv[2]

    process_images(markdown_file, authorization)