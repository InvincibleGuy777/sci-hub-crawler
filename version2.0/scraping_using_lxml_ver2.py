"""
update date: 2021/08/05
Author: Xu Chenchen
content: 由于sci-hub文献的html结构有变，故对xpath筛选模式作修改
"""

from lxml.html import fromstring
import re


def get_link_xpath(html):
    try:
        #  print(html)
        tree = fromstring(html)
        a = tree.xpath('//div[@id="buttons"]/button')[0]
        # print(a.text_content())
        onclick = a.get('onclick')
        # print(onclick)
        onclick = re.findall(r"location.href\s*=\s*'(.*?)'", onclick)[0]
        title = tree.xpath('//div[@id="citation"]/i/text()')
        if len(title) == 0:
            title = tree.xpath('//div[@id="citation"]/text()')
        return {'title': title[0], 'onclick': onclick}
    except Exception as e:
        print('error occurred: ', e)
        return None


def test_selector(selector):
    from download_ver2 import download
    from download_ver2 import doi_parser
    dois = ['10.1016/j.apergo.2020.103286',  # VR
           '10.1016/j.jallcom.2020.156728',  # SOFC
           '10.3964/j.issn.1000-0593(2020)05-1356-06']  # 飞行器
    links = []
    header = {'User-Agent': 'sheng'}
    for doi in dois:
        url = doi_parser(doi, start_url='sci-hub.do')
        html = download(url, header)
        #  print(html)
        link = selector(html)
        if link:
            links.append(link)
    for link in links:
        print(link)
    print('Done')


if __name__ == '__main__':
    print('test_xpath(): ')
    test_selector(get_link_xpath)