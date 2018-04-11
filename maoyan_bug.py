import requests
from requests.exceptions import RequestException
import re
import os
import json
from multiprocessing import Pool

headers = {'User-Agent':'Mozilla/5.0'}

# HTML下载器
def get_one_page(url):
    try:
        res = requests.get(url, headers = headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

# 构造HTML解析器
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

# 构造数据存储器
def write_to_file(content):
    with open ('result.txt', 'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    p = Pool()
    p.map(main,[i*10 for i in range(10)])