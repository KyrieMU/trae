import requests
from bs4 import BeautifulSoup
import re
import time
import random
import pandas as pd
from urllib.parse import urljoin

def get_headers():
    """返回随机User-Agent头"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }

def get_search_results(url, pages=5):
    """获取搜索结果页面中的文章链接"""
    all_links = []
    
    for page in range(1, pages + 1):
        # 构造分页URL
        if page == 1:
            page_url = url
        else:
            # 根据URL格式调整分页参数
            if '?' in url:
                page_url = f"{url}&page={page}"
            else:
                page_url = f"{url}?page={page}"
        
        print(f"正在爬取第{page}页的搜索结果...")
        
        try:
            response = requests.get(page_url, headers=get_headers(), timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找搜索结果中的文章链接
            # 这里需要根据实际网页结构调整选择器
            result_items = soup.select('.result-item')
            
            if not result_items:
                # 尝试其他可能的选择器
                result_items = soup.select('.result-list li')
            
            if not result_items:
                # 再尝试其他可能的选择器
                result_items = soup.select('div.result > ul > li')
            
            for item in result_items:
                link_tag = item.find('a')
                if link_tag and link_tag.get('href'):
                    article_url = link_tag.get('href')
                    # 确保URL是完整的
                    if not article_url.startswith('http'):
                        article_url = urljoin(url, article_url)
                    
                    title = link_tag.get_text(strip=True)
                    all_links.append({'title': title, 'url': article_url})
            
            # 随机延迟，避免请求过于频繁
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"爬取第{page}页时出错: {e}")
    
    return all_links

def get_article_content(url):
    """获取文章内容"""
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试不同的选择器来获取文章内容
        # 这些选择器需要根据实际网页结构调整
        content_selectors = [
            'div.article-content',
            'div.TRS_Editor',
            'div.content',
            'div.article',
            'div#content',
            'div.text-content',
            'div.news-content'
        ]
        
        content = None
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                # 移除脚本和样式元素
                for script in content_div.find_all(['script', 'style']):
                    script.decompose()
                
                # 获取文本内容
                content = content_div.get_text(strip=True, separator='\n')
                break
        
        # 如果上面的选择器都没找到内容，尝试获取正文部分
        if not content:
            # 尝试获取所有段落
            paragraphs = soup.find_all('p')
            if paragraphs:
                content = '\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
        
        # 获取发布日期
        date = None
        date_patterns = [
            r'\d{4}年\d{1,2}月\d{1,2}日',
            r'\d{4}-\d{1,2}-\d{1,2}',
            r'\d{4}/\d{1,2}/\d{1,2}'
        ]
        
        for pattern in date_patterns:
            date_match = re.search(pattern, response.text)
            if date_match:
                date = date_match.group()
                break
        
        return {
            'content': content,
            'date': date,
            'url': url
        }
    
    except Exception as e:
        print(f"爬取文章内容时出错 {url}: {e}")
        return {
            'content': None,
            'date': None,
            'url': url
        }

def main():
    # 搜索结果页面URL
    search_url = "https://sousuo.www.gov.cn/sousuo/search.shtml?code=17da70961a7&searchWord=%E6%9D%8E%E5%BC%BA%E4%B8%BB%E6%8C%81%E5%8F%AC%E5%BC%80%E5%9B%BD%E5%8A%A1%E9%99%A2%E5%B8%B8%E5%8A%A1%E4%BC%9A%E8%AE%AE&dataTypeId=107&sign=5cd35b1e-32ec-45df-a4dd-cffc0fce7222"
    
    # 获取搜索结果中的文章链接
    print("开始获取搜索结果...")
    article_links = get_search_results(search_url, pages=3)  # 爬取前3页
    
    if not article_links:
        print("未找到任何文章链接，请检查网页结构或搜索URL")
        return
    
    print(f"共找到 {len(article_links)} 篇文章")
    
    # 爬取每篇文章的内容
    articles = []
    for i, article in enumerate(article_links):
        print(f"正在爬取第 {i+1}/{len(article_links)} 篇文章: {article['title']}")
        article_data = get_article_content(article['url'])
        articles.append({
            'title': article['title'],
            'url': article['url'],
            'date': article_data['date'],
            'content': article_data['content']
        })
        
        # 随机延迟，避免请求过于频繁
        time.sleep(random.uniform(2, 5))
    
    # 将结果保存为CSV文件
    df = pd.DataFrame(articles)
    output_file = 'e:\\Desktop\\1\\爬虫\\政府网站文章.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"爬取完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    main()