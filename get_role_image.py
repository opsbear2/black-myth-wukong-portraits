import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs



def get_image(url):
    # 使用 requests 获取网页内容
    response = requests.get(url)
    html = response.content

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 找到第一个 GsImageLabel 类别的 <p> 标签
    first_image_label = soup.find('p', class_='GsImageLabel')

    # 从 <a> 标签中提取 URL
    '''
    url格式,提取?后面的路径
    https://www.gamersky.com/showimage/id_gamersky.shtml?https://img1.gamersky.com/image2024/08/20240827_sky_671_4/1104.jpg

    '''
    if first_image_label:
        href = first_image_label.find('a')['href']
        
        # 提取 ? 后面的数据
        if '?' in href:
            image_url = href.split('?')[1]
            print("第一个 GsImageLabel 中的图片 URL:", image_url)
        else:
            print("URL 中不包含 ?")
    else:
        print("未找到 GsImageLabel 类别的 <p> 标签")

    return image_url

def download_image(url, image_path):
    # 发送请求下载图片
    response = requests.get(url)

    # 确保请求成功
    
    if response.status_code == 200:
        # 打开一个文件，准备写入图片数据
        with open(image_path, "wb") as file:
            file.write(response.content)
        print("图片下载成功并保存为 'downloaded_image.jpg'")
    else:
        print(f"下载失败，状态码: {response.status_code}")

if __name__ == '__main__':
    # image_url = get_image('https://www.gamersky.com/handbook/202408/1803371_24.shtml')
    # image_path = "images/人物/aaa.jpg"
    # download_image(image_url, image_path)
    
    roleinfo_config = "roleinfo.json"
    with open (roleinfo_config, 'r', encoding='utf-8') as file:
        roleinfo = file.read()
    roleinfo_dict = json.loads(roleinfo)

    for type, items in roleinfo_dict.items():
        print(f"类型: {type}")
        for item in items:
            role = item['role']
            url= item['url']
            # 获取图片
            image_url = get_image(url)

            # 下载图片
            image_path = f"images/{type}/{role}.jpg"
            download_image(image_url, image_path)

            # print(role,url,image_url)
            # print(f"  角色: {item['role']}")
            # print(f"  URL: {item['url']}")
        print()  # 空行用于分隔不同类型