from bs4 import BeautifulSoup
import re


def get_link_using_bs4(html, parser='html5lib'):
    # parse the HTML
    try:
        soup = BeautifulSoup(html, parser)
    except:
        print('parser not available, now use the default parser "html.parser"...')
        parser = 'html.parser'
        soup = BeautifulSoup(html, parser)
    try:
        div = soup.find('div', attrs={'id': 'buttons'})
        if div:
            a = div.find('a', attrs={'href': '#'})
            if a:
                a = a.attrs['onclick']
                onclick = re.findall(r"location.href\s*=\s*'(.*?)'", a)[0]
                div = soup.find('div', attrs={'id': 'citation'})
                title = div.find('i')
                if title:
                    title = title.get_text()
                else:
                    title = div.get_text()
                return {'title': title, 'onclick': onclick}
    except Exception as e:
        print('error occured: ', e)
    return None



if __name__ == '__main__':
    from download import download
    from download import doi_parser
    dois = ['10.1016/j.apergo.2020.103286',  # VR
            '10.1016/j.jallcom.2020.156728',  # SOFC
            '10.3964/j.issn.1000-0593(2020)05-1356-06']  # 飞行器
    links = []
    for doi in dois:
        url = doi_parser(doi, 'sci-hub.do')
        html = download(url, headers={'User-Agent': 'sheng'})
        #  print(html)
        link = get_link_using_bs4(html)
        if link:
            links.append(link)
    for link in links:
        print(link)
