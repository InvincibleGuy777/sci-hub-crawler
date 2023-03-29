"""
update date: 2021/08/05
Author: Xu Chenchen
content: 爬取doi列表由原来的html变为了txt文件，用re的模式来识别doi(稳定性比html低)
"""

from lxml.html import fromstring
import re

def get_doi(text):
    """根据txt文本获得其中的doi并返回"""
    try:
        return re.compile('''(?<=DI )10.*''').findall(text)
    except Exception as e:
        print('get_doi() error: ', e)
        return None


def doi_crawler(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as fp:
            txt_file = fp.read()
            doi_list = get_doi(txt_file)
            return doi_list
    except Exception as e:
        print('doi_crawler() error', e)
        return None


if __name__ == '__main__':
    import time
    start = time.time()
    filepath = './data.txt'
    doi_list = doi_crawler(filepath)
    print('time spent: %ds' % (time.time() - start))
    print('%d doi records in total: ' % len(doi_list))
    for doi in doi_list:
        print(doi)
    print('Done.')