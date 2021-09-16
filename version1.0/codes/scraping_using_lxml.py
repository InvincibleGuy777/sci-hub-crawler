from lxml.html import fromstring
import re


def get_link_cssselect(html):
    try:
        # print(html)
        tree = fromstring(html)
        a = tree.cssselect('div#buttons > ul > li > a')[0]
        # print(a.text_content())
        onclick = a.get('onclick')
        # print(onclick)
        title = tree.cssselect('div#menu > div#citation > i')
        if len(title) == 0:
            title = tree.cssselect('div#menu > div#citation')
        title = title[0].text
        # print(title)
        onclick = re.findall(r"location.href\s*=\s*'(.*?)'", onclick)[0]
        return {'title': title, 'onclick': onclick}
    except Exception as e:
        print('error occurred: ', e)
        return None


def get_link_xpath(html):
    try:
        #  print(html)
        tree = fromstring(html)
        a = tree.xpath('//div[@id="buttons"]/ul/li/a')[0]
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
    from download import download
    from download import doi_parser
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
    # print('test_cssselect(): ')
    # test_selector(get_link_cssselect)
    print('test_xpath(): ')
    test_selector(get_link_xpath)