# sci-hub-crawler
A small and simple project to crawl the pdf resources on sci-hub according to the doi-list got on Web of Science.
 (Only for learning purpose.)

# Author info
**author**: InvincibleGuy777  (Chenchen Xu)

**github url**:  https://github.com/InvincibleGuy777/

**e-mail**: 2540588513@qq.com  / a2540588513@stu.xjtu.edu.cn

**csdn blog url**: https://me.csdn.net/weixin_42430021


# How to Use

1. 打开 Web of Science，搜索感兴趣的内容，得到一个搜索结果列表

2. 点击 "**导出为其他文件格式**" 按钮，记录条数自选，**记录内容**为**作者、标题、来源出版物**，**文件格式**选择**HTML**，然后点击"导出"，记录该 html 文件的 **绝对路径** `filepath` (也可以是相对路径) 

3. 调用 **doi_crawler(filepath)**，返回一个 doi 列表，将之命名为 `doi_list`

4. 调用 **sci_hub_crawler(doi_list, get_link=get_link_xpath, nolimit=True, cache=Cache(cache_dir))**，如果不需要缓存，可以不传参至 `cache`。另外说明的是，`cache_dir` 是缓存文件的路径，一般用**相对路径**即可；其余参数根据需要来调整

5. 等待结果

# Examples

```python
if __name__ == '__main__':
    from time import time
    start = time()
    filepath = './example_data.html'  # doi所在的原始 html
    cache_dir = './cache.txt'  # 缓存路径
    cache = Cache(cache_dir)
    sci_spider(filepath, nolimit=True, cache=cache)
    print('time spent: %ds' % (time() - start))
```

# Link for more detail

<a href="https://blog.csdn.net/weixin_42430021/article/details/110738063">【Python爬虫】从零开始爬取Sci-Hub上的论文(串行爬取)</a>
