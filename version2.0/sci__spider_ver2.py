"""
update date: 2021/08/05
Author: Xu Chenchen
content: 1. 爬取doi列表由原来的html变为了txt文件，用re的模式来识别doi(稳定性比html低)
        2. 下载的pdf文件可以自主确定文件路径(新增功能)，sci_spider设置pdf存储路径为默认参数
        3. 改动细节详见各个代码
"""

from download_ver2 import sci_hub_crawler
from scraping_using_lxml_ver2 import get_link_xpath
from cache import Cache
from advanced_doi_crawler_ver2 import doi_crawler


def sci_spider(savedrec_html_filepath, dir='./documents', robot_url=None, user_agent='sheng', proxies=None, num_retries=2,
                delay=3, start_url='sci-hub.do', useSSL=True, get_link=get_link_xpath,
               nolimit=False, cache=None):
    """
    给定一个文献索引导出文件 (来自 Web of Science)，(按照DOI)下载文献对应的 pdf文件 (来自 sci-hub)
    :param savedrec_html_filepath: 搜索结果的导出文件 (.txt)，其中含有文献记录 (每一条记录可能有doi，也可能没有)
    :param robot_url: robots.txt在sci-bub上的url
    :param user_agent: 用户代理，不要设为 'Twitterbot'
    :param proxies: 代理
    :param num_retries: 下载重试次数
    :param delay: 下载间隔时间
    :param start_url: sci-hub 主页域名
    :param useSSL: 是否开启 SSL，开启后HTTP协议名称为 'https'
    :param get_link: 抓取下载链接的函数对象，调用方式 get_link(html) -> html -- 请求的网页文本
                     所使用的函数在 scraping_using_%s.py % (bs4, lxml, regex) 内，默认用xpath选择器
    :param nolimit: do not be limited by robots.txt if True
    :param cache: 一个缓存类对象，在此代码块中我们完全把它当作字典使用
    """
    print('trying to collect the doi list...')
    doi_list = doi_crawler(savedrec_html_filepath)  # 得到 doi 列表
    if not doi_list:
        print('doi list is empty, crawl aborted...')
    else:
        print('doi_crawler process succeed.')
        print('now trying to download the pdf files from sci-hub...')
        sci_hub_crawler(doi_list, dir, robot_url, user_agent, proxies, num_retries, delay, start_url,
                    useSSL, get_link, nolimit, cache)
    print('Done.')


if __name__ == '__main__':
    from time import time
    start = time()
    filepath = './data.txt'  # doi所在的原始 txt (由web-of-science 搜索结果导出的plain text file)
    cache_dir = './cache_ver2.txt'  # 缓存路径(可更改名称，不可改扩展名)
    start_url = 'sci-hub.ren'
    cache = Cache(cache_dir)
    sci_spider(filepath, start_url=start_url, nolimit=True, cache=cache)
    print('time spent: %ds' % (time() - start))





