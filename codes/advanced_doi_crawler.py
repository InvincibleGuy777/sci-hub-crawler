from lxml.html import fromstring


def get_doi(html):
    """根据获取到的html获得其中的doi并返回"""
    results = []
    try:
        tree = fromstring(html)
        dois = tree.xpath('//td[text()="DI "]/following::*[1]')
        for doi in dois:
            results.append(doi.text)
        return results
    except Exception as e:
        print('get_doi() error: ', e)
        return None


def doi_crawler(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as fp:
            html = fp.read()
            doi_list = get_doi(html)
            return doi_list
    except Exception as e:
        print('doi_crawler() error', e)
        return None


if __name__ == '__main__':
    import time
    start = time.time()
    filepath = './data.html'
    doi_list = doi_crawler(filepath)
    print('time spent: %ds' % (time.time() - start))
    print('%d doi records in total: ' % len(doi_list))
    for doi in doi_list:
        print(doi)
    print('Done.')