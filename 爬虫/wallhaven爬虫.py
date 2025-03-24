import requests
from bs4 import BeautifulSoup
import os
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import re

class PowerfulCrawler:
    def __init__(self, base_url, save_dir, username=None, password=None, max_workers=10):
        """初始化爬虫"""
        self.base_url = base_url
        self.save_dir = save_dir
        self.visited_urls = set()
        self.image_count = 0
        self.max_workers = max_workers
        self.username = username
        self.password = password
        
        # 创建保存目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        # 设置请求头，模拟浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        # 创建会话，用于保持登录状态
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # 如果提供了用户名和密码，则进行登录
        if username and password:
            self.login()
    
    def login(self):
        """登录到 Wallhaven"""
        try:
            # 首先访问登录页面获取 CSRF token
            login_url = "https://wallhaven.cc/login"
            response = self.session.get(login_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取 CSRF token
            csrf_token = soup.find('input', {'name': '_token'})['value']
            
            # 准备登录数据
            login_data = {
                '_token': csrf_token,
                'username': self.username,
                'password': self.password
            }
            
            # 发送登录请求
            login_post_url = "https://wallhaven.cc/auth/login"
            login_response = self.session.post(login_post_url, data=login_data)
            
            # 检查登录是否成功
            if login_response.url == "https://wallhaven.cc/":
                print("登录成功!")
                return True
            else:
                print("登录失败，请检查用户名和密码")
                return False
        except Exception as e:
            print(f"登录过程中出错: {e}")
            return False
    
    def is_valid_url(self, url):
        """检查URL是否有效且属于同一域名"""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        return parsed_url.netloc == parsed_base.netloc or not parsed_url.netloc
    
    def download_image(self, img_url):
        """下载单个图片"""
        try:
            # 构建完整URL
            full_url = img_url if img_url.startswith('http') else urljoin(self.base_url, img_url)
            
            # 提取文件名
            img_name = os.path.basename(urlparse(full_url).path)
            if not img_name or '.' not in img_name:
                img_name = f"image_{self.image_count}.jpg"
            
            # 保存路径
            save_path = os.path.join(self.save_dir, img_name)
            
            # 使用会话下载图片
            response = self.session.get(full_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                self.image_count += 1
                print(f"已下载: {img_name}")
                return True
        except Exception as e:
            print(f"下载图片失败: {img_url}, 错误: {e}")
        return False
    
    def get_wallpaper_url(self, wallpaper_page_url):
        """获取壁纸详情页中的原始图片URL"""
        try:
            # 使用会话访问壁纸详情页
            response = self.session.get(wallpaper_page_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # 在壁纸详情页中查找原始图片链接
                img_element = soup.find('img', id='wallpaper')
                if img_element and img_element.get('src'):
                    return img_element.get('src')
            return None
        except Exception as e:
            print(f"获取壁纸URL失败: {wallpaper_page_url}, 错误: {e}")
            return None
    
    def crawl_page(self, url):
        """爬取单个页面"""
        if url in self.visited_urls:
            return {'images': [], 'links': []}
        
        self.visited_urls.add(url)
        try:
            full_url = urljoin(self.base_url, url)
            print(f"正在爬取页面: {full_url}")
            # 使用会话访问页面
            response = self.session.get(full_url, timeout=10)
            if response.status_code != 200:
                return {'images': [], 'links': []}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 针对Wallhaven搜索页面的特殊处理
            if 'search' in full_url:
                # 查找所有壁纸缩略图链接
                wallpaper_links = []
                figure_elements = soup.select('figure.thumb')
                for figure in figure_elements:
                    a_tag = figure.find('a', class_='preview')
                    if a_tag and a_tag.get('href'):
                        wallpaper_links.append(a_tag.get('href'))
                
                print(f"在页面 {full_url} 中找到 {len(wallpaper_links)} 个壁纸链接")
                
                # 查找下一页链接
                next_page = None
                pagination = soup.find('ul', class_='pagination')
                if pagination:
                    next_link = pagination.find('a', class_='next')
                    if next_link and next_link.get('href'):
                        next_page = next_link.get('href')
                        print(f"找到下一页链接: {next_page}")
                
                links = [next_page] if next_page else []
                return {'images': [], 'links': links, 'wallpaper_pages': wallpaper_links}
            
            # 普通页面处理
            img_tags = soup.find_all('img')
            img_urls = []
            for img in img_tags:
                img_url = img.get('src')
                if img_url:
                    img_urls.append(img_url)
                    
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if self.is_valid_url(href) and href not in self.visited_urls:
                    links.append(href)
            
            return {'images': img_urls, 'links': links}
        except Exception as e:
            print(f"爬取页面失败: {url}, 错误: {e}")
            return {'images': [], 'links': []}
    
    def start(self, max_pages=50, max_images=None):
        """开始爬取
        
        Args:
            max_pages: 最大爬取页面数
            max_images: 最大下载图片数，设置为None表示无限制
        """
        print(f"开始爬取网站: {self.base_url}")
        start_time = time.time()
        
        # 从当前URL开始，而不是从根路径
        initial_path = urlparse(self.base_url).path
        if urlparse(self.base_url).query:
            initial_path += '?' + urlparse(self.base_url).query
        to_visit = [initial_path]
        visited_count = 0
        page_count = 1
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while to_visit and visited_count < max_pages:
                if max_images is not None and self.image_count >= max_images:
                    print(f"已达到最大图片数量限制 ({max_images}张)，停止爬取")
                    break
                    
                current_url = to_visit.pop(0)
                print(f"\n===== 正在处理第 {page_count} 页 =====")
                result = self.crawl_page(current_url)
                visited_count += 1
                page_count += 1
                
                # 处理壁纸详情页
                if 'wallpaper_pages' in result and result['wallpaper_pages']:
                    wallpaper_futures = []
                    for wallpaper_page in result['wallpaper_pages']:
                        print(f"发现壁纸页面: {wallpaper_page}")
                        # 提交任务获取壁纸原始URL
                        future = executor.submit(self.get_wallpaper_url, wallpaper_page)
                        wallpaper_futures.append(future)
                    
                    # 收集并下载壁纸
                    for future in wallpaper_futures:
                        if max_images is not None and self.image_count >= max_images:
                            print(f"已达到最大图片数量限制 ({max_images}张)，停止下载")
                            break
                            
                        wallpaper_url = future.result()
                        if wallpaper_url:
                            print(f"找到壁纸: {wallpaper_url}")
                            self.download_image(wallpaper_url)
                
                if 'images' in result and result['images']:
                    # 并行下载图片
                    list(executor.map(self.download_image, result['images'][:max_images-self.image_count if max_images else None]))
                
                if 'links' in result and result['links']:
                    # 将有效的下一页链接添加到待访问列表
                    valid_links = [link for link in result['links'] if link]
                    to_visit.extend(valid_links)
                    print(f"添加了 {len(valid_links)} 个新链接到队列，当前队列长度: {len(to_visit)}")
        
        end_time = time.time()
        print(f"\n爬取完成! 共访问 {len(self.visited_urls)} 个页面, 下载 {self.image_count} 张图片")
        print(f"耗时: {end_time - start_time:.2f} 秒")


if __name__ == "__main__":
    # 使用示例 - 爬取Wallhaven网站的图片
    # 注意：实际使用时请遵守网站的robots.txt规则和相关法律法规
    
    # 需要登录的URL
    target_url = "https://wallhaven.cc/search?categories=010&purity=001&sorting=hot&order=desc&ai_art_filter=1&page=2" 
    save_directory = "e:\\Desktop\\1\\爬虫\\downloaded_images5"
    
    # 填入你的Wallhaven账号和密码
    username = "kyriechen1949"  # 替换为你的用户名
    password = "kfddXiZH8H2e.zR"    # 替换为你的密码
    
    crawler = PowerfulCrawler(target_url, save_directory, username=username, password=password)
    # 设置最大爬取10个页面，最大下载100张图片
    crawler.start(max_pages=10, max_images=5)


   