import argparse
import sys
import os

# 导入爬虫类
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wallhaven爬虫 import PowerfulCrawler

def main():
    parser = argparse.ArgumentParser(description='Wallhaven壁纸爬虫工具')
    parser.add_argument('url', help='要爬取的Wallhaven URL')
    parser.add_argument('--save-dir', '-s', default='./wallpapers', help='图片保存目录')
    parser.add_argument('--username', '-u', help='Wallhaven用户名')
    parser.add_argument('--password', '-p', help='Wallhaven密码')
    parser.add_argument('--max-pages', '-mp', type=int, default=10, help='最大爬取页面数')
    parser.add_argument('--max-images', '-mi', type=int, help='最大下载图片数')
    parser.add_argument('--workers', '-w', type=int, default=10, help='下载线程数')
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    crawler = PowerfulCrawler(
        base_url=args.url,
        save_dir=args.save_dir,
        username=args.username,
        password=args.password,
        max_workers=args.workers
    )
    
    # 开始爬取
    crawler.start(max_pages=args.max_pages, max_images=args.max_images)
    
if __name__ == '__main__':
    main()