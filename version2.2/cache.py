import json
import os


class Cache:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        self.cache = self.read_cache()  # Load the cache

    def __getitem__(self, url):
        if self.cache.get(url):
            return self.cache[url]
        else:
            return None

    def __setitem__(self, key, value):  # key -> url value -> pdf_url
        """Save data to disk for given URL"""
        filename = self.cache_dir
        self.cache[key] = value
        if os.path.exists(filename):
            with open(filename, 'r') as fp:
                if os.path.getsize(filename):
                    cache = json.load(fp)
                else:
                    cache = {}
                cache.update({key: value})
            with open(filename, 'w') as fp:
                json.dump(cache, fp, indent=0)  # 加换行符

    def read_cache(self):
        """Load data from disk for given URL"""
        try:
            filename = self.cache_dir
            if os.path.exists(filename):
                if os.path.getsize(filename):
                    with open(filename, 'r', encoding='utf-8') as fp:
                        return json.load(fp)
                else:
                    return {}
            else:
                with open(filename, 'w', encoding='utf-8'):
                    return {}
        except Exception as e:
            print('read_cache() error: ', e)
            return {}


if __name__ == '__main__':
    from download import sci_hub_crawler
    from scraping_using_lxml import get_link_xpath
    cache_dir = './cache.txt'
    dois = ['10.1016/j.apergo.2020.103286',  # VR
            '10.1016/j.jallcom.2020.156728',  # SOFC
            '10.3964/j.issn.1000-0593(2020)05-1356-06']  # 飞行器
    sci_hub_crawler(dois, get_link=get_link_xpath, user_agent='sheng', nolimit=True, cache=Cache(cache_dir))
    print('Done.')