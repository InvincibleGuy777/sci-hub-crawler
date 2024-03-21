"""
update date: 2021/09/24
Author: Xu Chenchen
content: 1. download_pdf()中，在GET请求前确保url没有转义字符

update date: 2021/08/05
Author: Xu Chenchen
content: 1. 修改了主函数的示例，导入version2的xpath筛选模块
        2. 下载的pdf文件可以自主确定文件路径(新增功能)
"""

import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from filename import get_valid_filename
import time





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
            else:
                print('Download error, code: {}, tries_remain: {}'.format(resp.status_code, num_retries))
                return None
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
    if len(components.scheme) == 0:  # 不存在协议时，自行添加
        url = 'https:{}'.format(url)
    # 去掉url中的转移符号(默认下载url中没有转义字符)
    url = url.replace('\\', '')
    print('File downloading: ', url)
    try:
        resp = requests.get(url, headers=headers, proxies=proxies, verify=False)
        if resp.status_code >= 400:
            print('File download error: ', resp.status_code)
            if num_retries and 500 <= resp.status_code < 600:
                return download_pdf(result, headers, dir, proxies, num_retries-1)
            else:  # 资源本身的问题
                print('Download error, code: {}, tries_remain: {}'.format(resp.status_code, num_retries))
                return False
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
        print('File download error', e)
        return False
    return True


def sci_hub_crawler(doi_list, dir, robot_url=None, user_agent='sheng', proxies=None,num_retries=2, delay=3, start_url='www.sci-hub.wf', useSSL=True, get_link=None, nolimit=False, cache=None):
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
    print('Traversing doi_list...')
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


# 测试下载pdf功能，需要确保下载资源的url没问题
def download_pdf_test(url, headers, dir, proxies=None, num_retries=2, doi=None):
    """
    :param dir: pdf文献下载的文件路径
    """
    print('File downloading: ', url)
    try:
        resp = requests.get(url, headers=headers, proxies=proxies, verify=False)
        if resp.status_code >= 400:
            print('File download error: ', resp.status_code)
            if num_retries and 500 <= resp.status_code < 600:
                return download_pdf_test(url, headers, dir, proxies, num_retries-1)
            else:  # 资源本身的问题
                print('Download error, code: {}, tries_remain: {}'.format(resp.status_code, num_retries))
                return False
        #  ok, let's write it to file
        with open(dir, 'wb') as fp:
            fp.write(resp.content)
    except requests.exceptions.RequestException as e:
        print('File download error', e)
        return False
    return True


# 测试用例 - download和download_pdf功能验证
def testcase_download():
    headers = {'User-Agent': 'sheng'}
    print('Testing download...')
    html_url = 'https://www.sci-hub.wf/10.1117/12.584586'
    html = download(html_url, headers)
    print(html)
    print('Testing download_pdf...')
    url_pdf_test = 'https://sci.bban.top//pdf//10.1117//12.584586.pdf?download=true'
    save_dir = '/'.join(['.', 'example.pdf'])
    download_pdf_test(url_pdf_test, headers, save_dir)
    print('done.')


def testcase_sci_hub_scrawler():
    print('Testing sci_hub_scrawler...')
    doi_list = ['10.1117/12.584586']
    headers = {'User-Agent': 'sheng'}
    save_dir = '.'
    from scraping_using_lxml import get_link_xpath
    sci_hub_crawler(doi_list, save_dir, start_url='www.sci-hub.wf', nolimit=True, get_link=get_link_xpath)
    print('done.')


if __name__ == '__main__':
    # testcase_download()
    testcase_sci_hub_scrawler()
