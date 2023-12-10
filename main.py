import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin

# 定义要抓取的页面范围
start_page = 8
end_page = 79  # 假设抓取 100 个页面，根据实际情况修改

for page_num in range(start_page, end_page + 1):
    # 创建保存文件的文件夹
    folder_name = f'web_pages/page_{page_num}'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    url = f'http://www.yuehussp.com/htm/{page_num}.htm'

    # 获取页面内容
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.content

        # 解析 HTML 内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 下载页面中的所有文件（图片、样式表、脚本等）
        resources = soup.find_all(['img', 'link', 'script'])
        for resource in resources:
            if resource.name == 'img':
                resource_url = resource.get('src')
            else:
                resource_url = resource.get('href') or resource.get('src')

            if resource_url and len(resource_url) > 0:
                # 处理相对链接
                if not resource_url.startswith('http'):
                    resource_url = urljoin(url, resource_url)

                # 编码处理
                resource_url = quote(resource_url, safe=':/')

                # 生成本地文件名
                local_filename = f'{folder_name}/{os.path.basename(resource_url)}'

                # 修改 HTML 中的链接为本地链接
                if resource.name == 'img':
                    resource['src'] = f'./{os.path.basename(resource_url)}'
                else:
                    resource['href'] = f'./{os.path.basename(resource_url)}'

                if resource.name == 'script':
                    resource['src'] = f'./{os.path.basename(resource_url)}'
                else:
                    resource['href'] = f'./{os.path.basename(resource_url)}'


                # 下载资源并保存到文件夹
                try:
                    resource_response = requests.get(resource_url)
                    if resource_response.status_code == 200:
                        with open(local_filename, 'wb') as resource_file:
                            resource_file.write(resource_response.content)
                except Exception as e:
                    print(f"Failed to fetch resource: {e}")

        # 保存修改后的 HTML 文件
        modified_html = soup.prettify(formatter=None)
        filename = f'{folder_name}/page_{page_num}.htm'
        with open(filename, 'wb') as file:
            file.write(modified_html.encode('utf-8'))
    else:
        print(f"Failed to fetch page {page_num}")

print("抓取完成！")
