# sci-hub-crawler
A small and simple project to crawl the pdf resources on sci-hub according to the doi-list got on Web of Science.
 (Only for learning purpose.)

 Ref https://blog.csdn.net/weixin_42430021/article/details/110738063 for the details.

# Author info
**author**: InvincibleGuy777  (Chenchen Xu)

**github url**:  https://github.com/InvincibleGuy777/

**e-mail**: 2540588513@qq.com  / a2540588513@stu.xjtu.edu.cn

**csdn blog url**: https://me.csdn.net/weixin_42430021

# 日志

**2024-03-21** 

version2.3版本主要改动：

1. 不再依赖PyCharm，仅需要cmd或者Anaconda Prompt即可运行；
2. 使用Python3.10代替Python3.6；
3. 修改了How to Use步骤说明，使得没有看过博文的朋友也能上手，且环境非常light weight；
4. 如果不担心弄乱包环境，也可以直接用pip来代替conda。



**2023-03-29** 

上传了version2.2版本，应对sci-hub的变化进行了小更新：

问题：`error occurred:  local variable 'onclick' referenced before assignment`

这句话的意思：在`onlick`声明前进行了引用。简单看了下，是因为有些文章sci-hub未收录(如下图)，所以呈现的html文本中不存在下载链接，自然没有onclick属性了。
![在这里插入图片描述](https://img-blog.csdnimg.cn/671929f52f49401a966c2c02d2a3b946.png)



这里简单修改了scraping_using_lxml.py的`get_link_xpath(html)`函数：

```python
def get_link_xpath(html):
    try:
        // ...省略
        a = tree.xpath('//div[@id="buttons"]/button')
        if len(a) == 0:  # 下载链接所在的层次不是<button> 而是 <ul><a><li>
            a = tree.xpath('//div[@id="buttons"]/ul/li/a')
        # print(a.text_content())
        
        // ==========================只改了这里==========================
        if len(a) == 0:  # 还是不行，那就认定为sci-hub未收录了
            print('Sorry, sci-hub has not included this article yet. Skipped it.')
            return None
        // =============================================================
		// ...省略		
    except Exception as e:
        print('error occurred: ', e)
        return None
```

**2021-09-24** \
上传了version2.1版本，修复了两个错误：

1. error - list index out of range: 这是由于pdf文献的url在网页中的层次不一致所致，有些为buttons/button，还有些为buttons/ul/li/a，而以往代码只考虑了其中一种层次，解决方法是两种情况全部考虑(不排除还有其他的层次)，筛选列表不为空的即可。

2. error - Invalid URL: 调用requests.get(url, ...)时，有些url中存在转义字符'\'，比如*https:\\/\\/sci.bban.top\\/pdf\\/10.1145\\/3132847.3132909.pdf?download=true*，导致get()方法误认为'\'需要转义，从而额外添加转义字符'\'，使得上述url变为*https:\\\\/\\\\/sci.bban.top\\\\/pdf\\\\/10.1145\\\\/3132847.3132909.pdf?download=true*，因而出错。解决方法是，在GET请求前去掉url中的转义字符'\'。

**2021-09-16** \
上传了version2.0版本，将基站 sci-hub.do(目前不可用)更改为了 sci-hub.ren，并使得模式匹配(找寻pdf文件的url所在的html层次)恢复正常；成功下载的pdf文件会保存在documents文件夹下(程序执行过程中会自动创建该文件夹)。

# How to Use

爬虫代码比较脆弱，可能今天能用明天就用不了了，因此请**尽量使用最新版本的代码!**

这里以conda为例讲述流程(也可以用pip代替)。

## 0. 安装conda，配置镜像源

conda的安装和配置流程在博文中介绍过了，也可以自行上网搜Anaconda。


如果`conda`和`python`命令找不到，请检查是否添加了相应的path环境变量。

以下命令均在Anaconda Prompt或cmd下执行，不要用Window PowerShell。


```
conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/win-64/
conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/win-64/
conda config --set show_channel_urls yes
```

## 1. 创建虚拟环境，指定python版本

注意：要确保Anaconda文件夹有Read/Write/Modify权限，否则可能在环境配置和包安装时出现如下的错误：

```
EnvironmentNotWritableError: The current user does not have write permissions to the target environment.
  environment location: E:\Applications\Programming\Anaconda
```



创建conda虚拟环境：
```
conda create -n [env name] python=[3.x]
```

[env name]即虚拟环境名称，自己取名替换即可。
[3.x]是python版本号，最好是3.10。

例如，

```
conda create -n Py310_Crawler python=3.10
```

## 2. 安装该项目的依赖项

别忘了激活刚创建的虚拟环境：

```
conda activate [env name]
```


依次执行下面命令安装依赖项：

```
conda install requests
```

```
conda install lxml
```

## 3. 使用

1. 打开 Web of Science，搜索感兴趣的内容，得到一个搜索结果列表

2. 点击 "**导出为其他文件格式**" 按钮，记录条数自选，**记录内容**为**作者、标题、来源出版物**，**导出格式**为**TXT文本文件**，然后点击"导出"，记录该导出文件在电脑中的 **绝对路径** `filepath` (也可以是相对于主函数文件`sci__spider.py`的相对路径)，这里建议把文本文件取名为data.txt并放在`sci__spider.py`的同级目录下，否则需要对`sci__spider.py`内`__main__`中的部分变量进行修改。

3. 在`sci__spider.py`脚本所在的目录下打开cmd，激活创建的conda环境，调试并运行 `sci__spider.py`：

    ```
    conda activate [env name]
    python sci__spider.py
    ```

    例如，我的sci__spider.py在`E:\sci-hub-crawler\version2.3`路径下，但是当前cmd路径在`C:\Users\Admin`，conda环境为`Py310_Crawler`，那么就按如下命令逐行执行：

    ```
    E:
    cd E:\sci-hub-crawler\version2.3
    conda activate Py310_Crawler
    python sci__spider.py
    ```

# sci__spider.py的主函数参数简介
程序的主函数PART如下：

```python
if __name__ == '__main__':
    from time import time
    start = time()
    filepath = './data.txt'  # doi所在的原始 txt (由web-of-science 搜索结果导出的plain text file)
    cache_dir = './cache_ver2.txt'  # 缓存路径(可更改名称，不可改扩展名)
    start_url = 'www.sci-hub.wf' # sci-hub网址，可以替换成能其他能用的
    cache = Cache(cache_dir)
    sci_spider(filepath, start_url=start_url, nolimit=True, cache=cache)
    print('time spent: %ds' % (time() - start))
```

注：
1. `filepath` 是web-of-science中导出的论文信息查询列表文件在本地磁盘中的路径，推荐放在代码所在的主目录下，这样就可以用简单的相对路径表示了

2. `start_url` 是 sci-hub的基站，比如sci-hub.ren等，如果当前的用不了，可更换其他可用的url。(不会找的话可以在CSDN上私信笔者)

3. `cache_dir` 是缓存文件的路径，一般用**相对路径**即可；其余参数根据需要来调整

4. `cache` 是缓存类Cache的实例，是sci_spider函数的可选参数。当爬取大量文件时容易出错，可能导致程序终止。缓存记录了已下载的文件，可以避免重复下载，有效应对程序终止的异常情况

5. 代码执行过程中存在警告信息，可以忽略

# Link for more detail

<a href="https://blog.csdn.net/weixin_42430021/article/details/110738063">【Python爬虫】从零开始爬取Sci-Hub上的论文(串行爬取)</a>
