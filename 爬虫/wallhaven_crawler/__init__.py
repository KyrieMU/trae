# 导入主要类，使其可以直接从包中导入
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wallhaven爬虫 import PowerfulCrawler

__version__ = "1.0.0"