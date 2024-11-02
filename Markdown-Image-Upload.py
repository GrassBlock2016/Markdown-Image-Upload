import re
# import os
# import shutil
import sys
import requests
import time

def get_local_img(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    image_pattern = r'!\[.*?\]\((?!https?://)(.*?)\)'
    image_local_path = re.findall(image_pattern, content)
    # current_directory = os.getcwd()

    return image_local_path


def get_network_img(image_local, token):
    upload_url = 'https://smms.app/api/v2/upload'
    headers = {
        'Authorization' : token
    }

    with open(image_local, 'rb') as img_file:
        files = {'smfile': img_file}
        response = requests.post(upload_url, files=files, headers=headers)
    
    if response.status_code == 200:
        res_data = response.json()
        if res_data['success']:                                     # 上传成功
            return res_data['data']['url']
        elif "Image upload repeated limit" in res_data['message']:  # 重复上传
            return res_data['images']
        else:                                                       # 上传失败
            print(f"上传失败: {res_data['message']}")
    else:
        print(f"HTTP 请求错误: {response.status_code}")
    return None


def replace_img(markdown_file, img_local_path, img_network_path):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    for i in range(len(img_local_path)):
        content = content.replace(img_local_path[i], img_network_path[i])
        print(f"已将图片 {img_local_path[i]} 替换为 {img_network_path[i]}")

    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(content)


def upload_images_with_limit(img_local_path, authorization, upload_limit_per_minute=20):
    upload_count = 0
    start_time = time.time()
    img_network_path = []

    for img_path in img_local_path:
        img_network_path.append(get_network_img(img_path, authorization))
        upload_count += 1

        if upload_count >= upload_limit_per_minute:
            elapsed_time = time.time() - start_time
            if elapsed_time < 65:
                time.sleep(65 - elapsed_time)
            upload_count = 0
            start_time = time.time()

        # 替换成功后的输出
        print(f"本地图片 {img_path} 已替换为网络图片 {img_network_path[-1]}")

    return img_network_path


# for image_path in image_local:
#     if os.path.exists(image_local):
#         image_name = os.path.basename(image_local)
        
#         destination = os.path.join(current_directory, 'result', image_name)
#         shutil.copy(image_local, destination)
#         print(f"已将图片 {image_name} 复制到当前目录")
#     else:
#         print(f"图片路径 {image_local} 不存在或不是本地路径")

# print("图片处理完成。")


if __name__ == '__main__':
    markdown_file = sys.argv[1]
    authorization = sys.argv[2]

    img_local_path = get_local_img(markdown_file)
    img_network_path = upload_images_with_limit(img_local_path, authorization)
    # img_network_path = []

    # for img_path in img_local_path:
    #     img_network_path.append(get_network_img(img_path, authorization))

    replace_img(markdown_file, img_local_path, img_network_path)
    print("所有图片均已处理完成。")
