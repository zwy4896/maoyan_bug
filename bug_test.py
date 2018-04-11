import requests as rq
import re
import os
import json as js
from requests import RequestException

headers = {'User-Agent':'Mozilla/5.0'}

def get_page(url):
    try:
        response = rq.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
    # 正则表达式解析
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?"star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    # yield items

    for i in items:
        yield{
            'index':i[0],
            'image':i[1],
            'title':i[2],
            'actor':i[3].strip()[3:],
            'time':i[4].strip()[5:],
            'score':i[5] + i[6]
        }

def wFile(content):
    with open("results.txt", 'a', encoding='utf-8') as f:
        f.write(js.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def wImage(url, path):
    ir = rq.get(url)
    if ir.status_code == 200:
        with open(path, 'wb') as f:
            f.write(ir.content)
            f.close()

def main():
    url = 'http://maoyan.com/board/4'
    html = get_page(url)
    # print(html)
    # 若不存在名为covers的文件夹，则创建该文件夹
    if not os.path.exists('covers'):
        os.mkdir('covers')
    for i in parse_page(html):
        print(i)
        wFile(i) 
        wImage(i['image'], 'covers/' + '%03d'%int(i['index']) + i['title'] + '.jpg')

if __name__ == '__main__':
    main()