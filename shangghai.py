from urllib import request
from bs4 import BeautifulSoup
import csv
import os

# # TXT保存路径
# txtSavePath = r"D:\Project\搜狗词库下载\Sougou_dict_spider\haici"
txtSavePath1 = r"D:\Project\搜狗词库下载\Sougou_dict_spider\haici\c.txt"

# # 创建保存路径
# try:
#     os.mkdir(txtSavePath)
# except Exception as e:
#     print(e)


url = 'https://gdh.dict.cn/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'}


def get_final_url():
    urls_tags = get_url_tag()
    urls_page = getUrlPager(urls_tags)
    print("urls_tags==========" + str(len(urls_tags)))
    print("urls_tags==========" + str(len(urls_page)))

    for index, value in enumerate(urls_tags):
        print(index)
        i = 1
        while i <= int(urls_page[index]):

            parseHtml(value + '/' + str(i))
            i = i + 1


def get_url_tag():
    # 创建请求

    req = request.Request(url=url, headers=headers)

    with request.urlopen(req) as response:
        # 读取response里的内容，并转码
        data1 = response.read().decode('utf-8')  # 默认即为 utf-8
        bf = BeautifulSoup(data1, 'lxml')

        # 上海对话分类
        contents = bf.find_all(class_="obox-c fydl fc80")

        urls = []
        # 获取url类别
        for tag in contents[0].descendants:
            if tag.name == 'a':
                url_tag = url + request.quote(tag['href'])
                urls.append(url_tag)
                print(tag['href'])

    return urls


def getUrlPager(urls_tags):
    urls_page = []
    # 获取每个类比的页数
    for url_tag in urls_tags:
        # 创建请求

        req = request.Request(url=url_tag, headers=headers)
        with request.urlopen(req) as response:
            # 读取response里的内容，并转码
            data1 = response.read().decode('utf-8')  # 默认即为 utf-8
            bf = BeautifulSoup(data1, 'lxml')

            # 上海对话分类
            contents = bf.find_all('a', text="最后页")
            page = contents[0]['href'].split('/')[3]
            print(page)
            urls_page.append(page)

            # 获取url类别

    return urls_page


def parseHtml(url_final):
    print('解析：' + url_final)

    req = request.Request(url=url_final, headers=headers)
    # 打开一个文件
    f = open(txtSavePath1, "a+")

    with request.urlopen(req) as response:
        # 读取response里的内容，并转码
        data1 = response.read().decode('utf-8')  # 默认即为 utf-8
        bf = BeautifulSoup(data1, 'lxml')
        content = bf.find(class_='mbox-c')

        for text in content.contents[1].find_all('a'):
            if text.string is not None:
                str=text['href'].split('/')[1]
                if str != text.string:
                    fy = text.string + '\n'
                    f.writelines(fy)
    # 关闭打开的文件
    f.close()


get_final_url()
