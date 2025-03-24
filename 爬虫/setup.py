from setuptools import setup, find_packages

setup(
    name="wallhaven-crawler",
    version="1.0.0",
    description="一个功能强大的Wallhaven网站壁纸爬虫工具",
    # 移除读取README.md的行，直接提供长描述
    long_description="一个功能强大的Wallhaven网站壁纸爬虫工具，支持自动登录、多线程下载和自动翻页功能。",
    long_description_content_type="text/plain",
    author="Trae AI",
    author_email="example@example.com",
    url="https://github.com/yourusername/wallhaven-crawler",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "wallhaven-crawler=wallhaven_crawler.cli:main",
        ],
    },
)