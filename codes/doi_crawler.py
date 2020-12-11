from download import download
import re
from lxml.html import fromstring


def url_changer(source_url):
    """获取文献网站url的模式"""
    url = re.findall(r'''(.*)&doc''', source_url)[0]
    doc = '&doc='
    return url + doc


def get_doi(html):
    """根据获取到的html获得其中的doi并返回"""
    try:
        tree = fromstring(html)
        doi = tree.xpath('//span[text()="DOI:"]/following::*[1]')[0].text
        return doi
    except Exception as e:
        print('get_doi() error: ', e)
        return None


def doi_crawler(pattern_url, headers=None, number=500):
    """  获得搜索结果中第 [1, number] 的 doi
    pass the following parameter
    :param pattern_url: 搜索结果内任意一篇文献的url，不是分页或者搜索结果页的!
    :param number: doi获取数目，不要超过页面最大结果数
    """
    if headers is None:
        headers = {'User-Agent': 'sheng'}
    base_url = url_changer(pattern_url)
    dois = []
    for i in range(1, number + 1):
        url = base_url + str(i)
        html = download(url, headers)
        doi = get_doi(html)
        if doi:
            dois.append(doi)
    return dois


def save_doi_list(dois, filename):
    """将doi列表项以[filename].txt保存到当前文件夹中，"""
    filepath = filename[:128] + '.txt'
    try:
        with open(filepath, 'w') as fp:
            for doi in dois:
                fp.writelines(doi + '\n')
    except Exception as e:
        print('save error: ', e)


def read_dois_from_disk(filename):
    """从磁盘文件[filename].txt中
        按行读取doi，返回一个doi列表"""
    dois = []
    try:
        filepath = filename + '.txt'
        with open(filepath, 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                dois.append(line.strip('\n'))
            return dois
    except Exception as e:
        print('read error: ', e)
        return None


if __name__ == '__main__':
    import time
    source_url = 'http://apps.webofknowledge.com/full_record.do?product=UA&' \
                 'search_mode=GeneralSearch&qid=2&SID=6F9FiowVadibIcYJShe&page=1&doc=2'
    start = time.time()
    dois = doi_crawler(source_url, number=10)
    save_doi_list(dois, 'dois')
    print('time spent: %ds' % (time.time()-start))
    print('now read the dois from disk: ')
    doi_list = read_dois_from_disk('dois')
    for doi in doi_list:
        print(doi)