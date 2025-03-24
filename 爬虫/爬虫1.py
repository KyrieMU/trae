import requests
from bs4 import BeautifulSoup
import time
import os
import random
import re
from urllib.parse import urljoin

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

# 创建保存文章的目录
save_dir = 'e:\\Desktop\\1\\爬虫\\政府网文章'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 已爬取的URL集合，避免重复爬取
crawled_urls = set()

def get_page(url):
    """获取网页内容"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'  # 确保中文内容正确解码
        if response.status_code == 200:
            return response.text
        else:
            print(f"获取页面失败: {url}, 状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求异常: {url}, 错误: {e}")
        return None

def parse_article_list(html, base_url):
    """解析文章列表页，提取文章链接"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    article_links = []
    
    # 查找可能的文章链接
    for link in soup.find_all('a', href=True):
        href = link['href']
        # 过滤掉非文章链接
        if re.search(r'content|article|news|xinwen', href, re.IGNORECASE):
            full_url = urljoin(base_url, href)
            article_links.append(full_url)
    
    return article_links

def parse_article(html, url):
    """解析文章内容"""
    if not html:
        return None, None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 尝试不同的选择器来获取标题
    title = None
    for selector in ['h1', '.article-title', '.title', '.bt', '#title']:
        title_tag = soup.select_one(selector)
        if title_tag and title_tag.text.strip():
            title = title_tag.text.strip()
            break
    
    if not title:
        # 如果没有找到标题，尝试使用页面title标签
        title_tag = soup.title
        if title_tag:
            title = title_tag.text.strip()
    
    # 尝试不同的选择器来获取内容
    content = None
    for selector in ['.article-content', '.TRS_Editor', '.content', '#content', '.text', '.zhengwen', '.con_txt']:
        content_div = soup.select_one(selector)
        if content_div:
            # 移除脚本和样式元素
            for script in content_div.find_all(['script', 'style']):
                script.decompose()
            
            # 获取所有段落文本
            paragraphs = [p.text.strip() for p in content_div.find_all('p') if p.text.strip()]
            if paragraphs:
                content = '\n\n'.join(paragraphs)
                break
    
    if not content:
        # 如果没有找到内容，尝试直接获取body中的所有段落
        body = soup.body
        if body:
            paragraphs = [p.text.strip() for p in body.find_all('p') if p.text.strip()]
            if paragraphs:
                content = '\n\n'.join(paragraphs)
    
    return title, content

def save_article(title, content, url):
    """保存文章到文件"""
    if not title or not content:
        return False
    
    # 清理标题，移除不允许作为文件名的字符
    clean_title = re.sub(r'[\\/*?:"<>|]', '', title)
    clean_title = clean_title[:50]  # 限制标题长度
    
    filename = os.path.join(save_dir, f"{clean_title}.txt")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"标题: {title}\n")
            f.write(f"来源: {url}\n")
            f.write(f"爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + "="*50 + "\n\n")
            f.write(content)
        print(f"保存文章成功: {filename}")
        return True
    except Exception as e:
        print(f"保存文章失败: {e}")
        return False

def crawl(start_url, max_articles=50, max_depth=2):
    """爬取文章的主函数"""
    queue = [(start_url, 0)]  # (URL, 深度)
    article_count = 0
    
    while queue and article_count < max_articles:
        url, depth = queue.pop(0)
        
        # 如果URL已经爬取过或深度超过限制，则跳过
        if url in crawled_urls or depth > max_depth:
            continue
        
        print(f"正在爬取: {url}")
        crawled_urls.add(url)
        
        html = get_page(url)
        if not html:
            continue
        
        # 尝试解析为文章
        title, content = parse_article(html, url)
        if title and content:
            if save_article(title, content, url):
                article_count += 1
                print(f"已爬取 {article_count}/{max_articles} 篇文章")
        
        # 如果深度未达到最大值，继续爬取链接
        if depth < max_depth:
            new_links = parse_article_list(html, url)
            for link in new_links:
                if link not in crawled_urls:
                    queue.append((link, depth + 1))
            
            # 随机延迟，避免请求过于频繁
            time.sleep(random.uniform(1, 3))
    
    print(f"爬取完成，共爬取 {article_count} 篇文章")

def parse_search_results(html, base_url):
    """解析搜索结果页面，提取文章链接"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    article_links = []
    
    # 查找搜索结果中的文章链接
    result_items = soup.select('.result-item')
    for item in result_items:
        link_tag = item.select_one('a')
        if link_tag and link_tag.has_attr('href'):
            href = link_tag['href']
            full_url = urljoin(base_url, href)
            article_links.append(full_url)
    
    # 如果没有找到结果项，尝试查找所有可能的文章链接
    if not article_links:
        for link in soup.find_all('a', href=True):
            href = link['href']
            if re.search(r'content|article|news|xinwen', href, re.IGNORECASE):
                full_url = urljoin(base_url, href)
                article_links.append(full_url)
    
    return article_links

def get_next_page_url(html, base_url):
    """获取下一页的URL"""
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    next_page = soup.select_one('a.next-page')
    if next_page and next_page.has_attr('href'):
        return urljoin(base_url, next_page['href'])
    
    # 尝试其他可能的下一页链接
    for link in soup.find_all('a', href=True):
        if '下一页' in link.text or '下页' in link.text:
            return urljoin(base_url, link['href'])
    
    return None

def crawl_search_results(search_url, max_articles=50, max_pages=5):
    """爬取搜索结果页面的文章"""
    article_count = 0
    page_count = 0
    current_url = search_url
    
    while current_url and article_count < max_articles and page_count < max_pages:
        print(f"正在爬取搜索结果页面: {current_url}")
        page_count += 1
        
        html = get_page(current_url)
        if not html:
            break
        
        # 解析搜索结果页面中的文章链接
        article_links = parse_search_results(html, current_url)
        print(f"找到 {len(article_links)} 个文章链接")
        
        # 爬取每篇文章
        for link in article_links:
            if link in crawled_urls or article_count >= max_articles:
                continue
            
            print(f"正在爬取文章: {link}")
            crawled_urls.add(link)
            
            article_html = get_page(link)
            if not article_html:
                continue
            
            # 解析文章内容
            title, content = parse_article(article_html, link)
            if title and content:
                if save_article(title, content, link):
                    article_count += 1
                    print(f"已爬取 {article_count}/{max_articles} 篇文章")
            
            # 随机延迟，避免请求过于频繁
            time.sleep(random.uniform(1, 3))
        
        # 获取下一页URL
        current_url = get_next_page_url(html, current_url)
        
        # 页面间延迟
        if current_url:
            time.sleep(random.uniform(2, 4))
    
    print(f"爬取完成，共爬取 {article_count} 篇文章，浏览了 {page_count} 页搜索结果")

if __name__ == "__main__":
    start_url = "https://www.gov.cn/"
    crawl(start_url, max_articles=30, max_depth=2)
    # 使用提供的搜索URL
    search_url = "https://sousuo.www.gov.cn/sousuo/search.shtml?code=17da70961a7&searchWord=%E6%9D%8E%E5%BC%BA%E4%B8%BB%E6%8C%81%E5%8F%AC%E5%BC%80%E5%9B%BD%E5%8A%A1%E9%99%A2%E5%B8%B8%E5%8A%A1%E4%BC%9A%E8%AE%AE&dataTypeId=107&sign=5cd35b1e-32ec-45df-a4dd-cffc0fce7222"
    
    # 调用新的爬取搜索结果的函数
    crawl_search_results(search_url, max_articles=30, max_pages=5)