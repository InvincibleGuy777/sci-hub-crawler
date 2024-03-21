"""
update date: 2023/03/29
Author: Xu Chenchen
content: 很多文章没有收录，此时爬取的html将不会存在onlick属性，这里简单print一下"文章无法获取"，而不是触发exception

update date: 2021/09/24
Author: Xu Chenchen
content: 由于sci-hub文献的html结构有变，故对xpath筛选模式作修改, 相较2.0版本，发现有些pdf文件下载链接仍然在<a>标记中，
因此除了考虑<button>外，还得考虑原来的 ul/li/a的层次；另外，获取列表的元素时，要单独考虑列表为空的情况，避免 list index out of range
"""

import re
from lxml.html import fromstring


def get_link_xpath(html):
    try:
        #  print(html)
        tree = fromstring(html)
        a = tree.xpath('//div[@id="buttons"]/button')
        if len(a) == 0:  # 下载链接所在的层次不是<button> 而是 <ul><a><li>
            a = tree.xpath('//div[@id="buttons"]/ul/li/a')
        # print(a.text_content())

        if len(a) == 0:  # 还是不行，那就认定为sci-hub未收录了
            print('Sorry, sci-hub has not included this article yet. Skipped it.')
            return None

        for a_unit in a:  # 寻找带有onclick属性的<a>标签
            onclick = a_unit.get('onclick')
            if onclick:
                break
        # print(onclick)
        onclick = re.findall(r"location.href\s*=\s*'(.*?)'", onclick)[0]
        flag = True  # 执行位置标记
        title = tree.xpath('//div[@id="citation"]/i/text()')  # 标题在斜体标记中
        if len(title) == 0:
            title = tree.xpath('//div[@id="citation"]/text()')
        return {'title': title[0], 'onclick': onclick}
    except Exception as e:
        print('error occurred: ', e)
        return None


def test_selector(selector):
    from download import download
    from download import doi_parser
    dois = ['10.1016/j.apergo.2020.103286',  # VR
           '10.1016/j.jallcom.2020.156728',  # SOFC
           '10.3964/j.issn.1000-0593(2020)05-1356-06']  # 飞行器
    links = []
    header = {'User-Agent': 'sheng'}
    for doi in dois:
        url = doi_parser(doi, start_url='www.sci-hub.wf')
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