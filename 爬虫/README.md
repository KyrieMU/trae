# Wallhaven爬虫使用说明文档

## 简介

这是一个功能强大的Wallhaven网站壁纸爬虫工具，能够自动登录、爬取和下载Wallhaven网站上的高清壁纸，包括需要登录才能查看的NSFW内容。爬虫采用多线程下载，支持自动翻页，可以高效地批量获取壁纸资源。

## 功能特点

- **自动登录**：支持使用账号密码登录Wallhaven，获取访问受限内容的权限
- **多线程下载**：使用线程池并行下载图片，大幅提高下载效率
- **自动翻页**：能够自动识别并访问下一页链接，连续爬取多页内容
- **灵活配置**：可设置最大爬取页数和最大下载图片数量
- **智能解析**：专门针对Wallhaven网站结构进行了优化，能准确获取原始高清图片
- **断点续传**：记录已访问的URL，避免重复爬取

## 使用方法

### 基本用法

1. 确保已安装所需的Python库：
```bash
pip install requests beautifulsoup4
```

2. 修改代码中的配置参数：
```python
# 设置目标URL（可以是搜索结果页面）
target_url = "https://wallhaven.cc/search?categories=010&purity=001&sorting=hot&order=desc&ai_art_filter=1&page=2" 

# 设置保存目录
save_directory = "e:\\Desktop\\1\\爬虫\\downloaded_images"

# 填入Wallhaven账号和密码（如需爬取NSFW内容）
username = "你的用户名"
password = "你的密码"

# 创建爬虫实例并开始爬取
crawler = PowerfulCrawler(target_url, save_directory, username=username, password=password)
crawler.start(max_pages=10, max_images=100)  # 最多爬取10页，下载100张图片
```

### 参数说明

- **target_url**: 爬取的起始URL，可以是Wallhaven的搜索结果页面
- **save_directory**: 图片保存的本地目录
- **username/password**: Wallhaven的账号和密码（爬取NSFW内容时必须提供）
- **max_workers**: 下载线程数，默认为10
- **max_pages**: 最大爬取页面数
- **max_images**: 最大下载图片数量，设为None表示无限制

### URL参数说明

Wallhaven搜索URL中的参数含义：
- **categories**: 图片类别（General=100, Anime=010, People=001）
- **purity**: 内容分级（SFW=100, Sketchy=010, NSFW=001）
- **sorting**: 排序方式（date_added, relevance, random, views, favorites, toplist, hot）
- **order**: 排序顺序（desc, asc）
- **ai_art_filter**: AI生成的艺术作品过滤（0=显示, 1=不显示）
- **page**: 页码

## 注意事项

1. 请遵守Wallhaven的使用条款和robots.txt规则
2. 爬取NSFW内容需要登录账号，且账号需要在Wallhaven设置中启用NSFW内容查看权限
3. 请合理控制爬取速度和频率，避免对网站造成过大负担
4. 下载的图片仅供个人使用，请尊重版权
5. 请妥善保管你的账号密码信息

## 代码结构

- **PowerfulCrawler类**: 主要爬虫类，包含所有爬取和下载功能
  - **login()**: 登录Wallhaven网站
  - **crawl_page()**: 爬取单个页面内容
  - **get_wallpaper_url()**: 从壁纸详情页获取原始图片URL
  - **download_image()**: 下载单个图片
  - **start()**: 开始爬取过程

## 示例

```python
# 爬取动漫类壁纸的热门排行
target_url = "https://wallhaven.cc/search?categories=010&purity=100&sorting=hot&order=desc"
save_directory = "e:\\Desktop\\anime_wallpapers"
crawler = PowerfulCrawler(target_url, save_directory)
crawler.start(max_pages=5, max_images=50)

# 爬取需要登录的NSFW内容
target_url = "https://wallhaven.cc/search?categories=001&purity=001&sorting=toplist&order=desc"
save_directory = "e:\\Desktop\\nsfw_wallpapers"
crawler = PowerfulCrawler(target_url, save_directory, username="your_username", password="your_password")
crawler.start(max_pages=3, max_images=30)
```

## 扩展与改进

如需进一步改进爬虫功能，可以考虑：
1. 添加代理支持，避免IP被封
2. 实现断点续传，支持中断后继续下载
3. 添加图片分类和重命名功能
4. 开发图形用户界面，方便使用

---

**免责声明**：本工具仅供学习和研究使用，请勿用于任何商业或非法用途。使用本工具产生的任何后果由使用者自行承担。
