# coding: utf-8

from firstSpider.DataOutput import DataOutput
from firstSpider.HtmlDownloader import HtmlDownloader
from firstSpider.HtmlParser import HtmlParser
from firstSpider.UrlManager import UrlManager

class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # 添加入口 URL
        self.manager.add_new_url(root_url)
        # 判断 URL 管理器中是否有新的 URL，同时判断抓取了多少个 URL
        while(self.manager.has_new_url() and self.manager.old_url_size() < 100)
            try:
                # 从 URL 管理器获取新的 URL
                new_url = self.manager.get_new_url()
                # 使用 HTML 下载器下载网页
                html = self.downloader.download(new_url)
                # 使用 HTML 解析器提取网页数据
                new_urls, data = self.parser.parser(new_url, html)
                # 将抽取的 URL 添加到 URL 管理器中
                self.manager.add_new_urls(new_urls)
                # 使用数据存储器存储文件
                self.output.store_data(data)
                print("已抓取 %s 个链接"%self.manager.old_url_size())
            except Exception, e:
                print("Crawl failed.")
        # 数据存储器将文件输出为指定格式
        self.output.output_html()
    
if __name__ == "__main__":
    spider_man = SpiderMan()
    spider_man.crawl("https://baike.baidu.com/item/%E9%98%BF%E6%A3%AE%E7%BA%B3%E8%B6%B3%E7%90%83%E4%BF%B1%E4%B9%90%E9%83%A8")