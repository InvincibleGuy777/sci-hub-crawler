"""
update date: 2021/08/05
Author: Xu Chenchen
content: 1. 修改了主函数的示例，导入version2的xpath筛选模块
        2. 下载的pdf文件可以自主确定文件路径(新增功能)
"""

import requests
from urllib.robotparser import RobotFileParser
import time
from urllib.parse import urlparse
from filename import get_valid_filename


def doi_parser(doi, start_url, useSSL=True):
    """Parse doi to url"""
    HTTP = 'https' if useSSL else 'http'
    url = HTTP + '://{}/{}'.format(start_url, doi)
    return url


def get_robot_parser(robot_url):
    rp = RobotFileParser()
    rp.set_url(robot_url)
    rp.read()
    return rp


def wait(url, delay=3, domains={}):
    """wait until the interval between two
    downloads of the same domain reaches time delay"""
    domain = urlparse(url).netloc  # get the domain
    last_accessed = domains.get(domain)  # the time last accessed
    if delay > 0 and last_accessed is not None:
        sleep_secs = delay - (time.time() - last_accessed)
        if sleep_secs > 0:
            time.sleep(sleep_secs)
    domains[domain] = time.time()


def download(url, headers, proxies=None, num_retries=2):
    print('Downloading: ', url)
    try:
        resp = requests.get(url, headers=headers, proxies=proxies, verify=False)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error: ', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, headers, proxies, num_retries-1)
    except requests.exceptions.RequestException as e:
        print('Download error', e)
        return None
    return html


def download_pdf(result, headers, dir, proxies=None, num_retries=2, doi=None):
    """
    :param dir: pdf文献下载的文件路径
    """
    url = result['onclick']
    components = urlparse(url)
    if len(components.scheme) == 0:
        url = 'https:{}'.format(url)
    print('Downloading: ', url)
    try:
        resp = requests.get(url, headers=headers, proxies=proxies, verify=False)
        if resp.status_code >= 400:
            print('Download error: ', resp.status_code)
            if num_retries and 500 <= resp.status_code < 600:
                return download(result, headers, proxies, num_retries-1)
        if len(result['title']) < 5:  # 处理标题为空的情况
            filename = get_valid_filename(doi) + '.pdf'
        else:
            filename = get_valid_filename(result['title']) + '.pdf'
        path = '/'.join([dir, filename])
        print(path)
        #  ok, let's write it to file
        with open(path, 'wb') as fp:
            fp.write(resp.content)
    except requests.exceptions.RequestException as e:
        print('Download error', e)
        return False
    return True


def sci_hub_crawler(doi_list, dir, robot_url=None, user_agent='sheng', proxies=None,num_retries=2,
                delay=3, start_url='sci-hub.do', useSSL=True, get_link=None, nolimit=False, cache=None):
    """
    给定文献doi列表，爬取对应文献的 pdf 文件
    :param doi_list: doi列表
    :param robot_url: robots.txt在sci-bub上的url
    :param user_agent: 用户代理，不要设为 'Twitterbot'
    :param dir: pdf文献下载的文件路径(若不存在则会自动创建)
    :param proxies: 代理
    :param num_retries: 下载重试次数
    :param delay: 下载间隔时间
    :param start_url: sci-hub 主页域名
    :param useSSL: 是否开启 SSL，开启后HTTP协议名称为 'https'
    :param get_link: 抓取下载链接的函数对象，调用方式 get_link(html) -> html -- 请求的网页文本
                     所使用的函数在 scraping_using_%s.py % (bs4, lxml, regex) 内
    :param nolimit: do not be limited by robots.txt if True
    :param cache: 一个缓存类对象，在此代码块中我们完全把它当作字典使用
    :return:
    """
    headers = {'User-Agent': user_agent}
    HTTP = 'https' if useSSL else 'http'
    if not get_link:
        print('Crawl failed, no get_link method.')
        return None
    if not robot_url:
        robot_url = HTTP + '://{}/robots.txt'.format(start_url)
    # print(robot_url)
    try:
        rp = get_robot_parser(robot_url)
    except Exception as e:
        rp = None
        print('get_robot_parser() error: ', e)
    domains={}  # save the timestamp of accessed domains
    download_succ_cnt: int = 0  # the number of pdfs that're successfully downloaded
    # 如果dir不存在，则创建dir
    import os
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except Exception as e:
        print('directory making error: ', e)
    for doi in doi_list:
        url = doi_parser(doi, start_url, useSSL)
        if cache and cache[url]:
            print('already downloaded: ', cache[url])
            download_succ_cnt += 1
            continue
        if rp and rp.can_fetch(user_agent, url) or nolimit:
            wait(url, delay, domains)
            html = download(url, headers, proxies, num_retries)
            result = get_link(html)
            if result and download_pdf(result, headers, dir, proxies, num_retries, doi):
                if cache:
                    cache[url] = 'https:{}'.format(result['onclick'])  # cache
                download_succ_cnt += 1
        else:
            print('Blocked by robots.txt: ', url)
    print('%d of total %d pdf success' % (download_succ_cnt, len(doi_list)))


if __name__ == '__main__':
    from scraping_using_lxml_ver2 import get_link_xpath

    dois = ['10.1109/TCIAIG.2017.2755699', # HTTP协议头重复
    		'10.3390/s20205967',  # 标题为空
    		'10.1016/j.apergo.2020.103286'  # 没毛病
    ]
    get_link = get_link_xpath
    print('use %s as get_link_method.' % get_link.__name__)
    dir ='./documents' # pdf存储路径
    sci_hub_crawler(dois, dir, get_link = get_link, user_agent='sheng', nolimit=True)
    print('Done.')