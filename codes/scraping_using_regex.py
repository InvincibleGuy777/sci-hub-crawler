import re


def get_links(pattern, html):
    regex = re.compile(pattern, re.IGNORECASE)
    return regex.findall(html)


def get_link_using_regex(html):
    pattern_onclick = '''<div id\s*=\s*"buttons">\s*<ul>\s*.*?\s*<li.*?\s*<li><a[^>]+href\s*=\s*#\s*onclick\s*=\s*"location.href='(.*?)'">'''
    pattern_title = '''<div id\s*=\s*"citation"[^>]+>(.*?)</div>'''
    try:
        title = get_links(pattern_title, html)[0]
        if title:
            i = get_links('<i>(.*?)</i>', title)
            title = i[0] if i else title
        onclick = get_links(pattern_onclick, html)[0]
        if onclick and title:
            return {'title': title, 'onclick': onclick}
        elif onclick:
            print('No title, now use onclick string to be the title.')
            return {'title': onclick, 'onclick': onclick}
    except Exception as e:
        print('error occurred: ', e)
    return None

if __name__ == '__main__':
    from download import download
    from download import doi_parser
    dois = ['10.1016/j.apergo.2020.103286',  # VR
           '10.1016/j.jallcom.2020.156728',  # SOFC
           '10.3964/j.issn.1000-0593(2020)05-1356-06']  # 飞行器
    # pattern = '''<a href="#" onclick="location.href='(.*?)'">'''
    # pattern = '''<script[^>]+type="text/javascript">(.*?)</script>'''
    links = []
    for doi in dois:
        url = doi_parser(doi, 'sci-hub.do')
        html = download(url, headers={'User-Agent': 'sheng'})
        link = get_link_using_regex(html)
        if link:
            links.append(link)

    for link in links:
        print(link)
