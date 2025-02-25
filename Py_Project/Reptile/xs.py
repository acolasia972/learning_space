import requests
from lxml import etree

url = 'https://dl.131437.xyz/book/douluodalu1/1.html'
while True:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    e = etree.HTML(response.text)
    info = '\n'.join(e.xpath('//div[@class="m-post"]/p/text()'))
    title = e.xpath('//h1/text()')[0]
    with open("斗罗大陆.txt", "a+", encoding='utf-8') as f:
        f.write(title + "\n\n" + info + "\n\n")
    next_url = e.xpath('//tr/td[2]/a/@href')[0]
    print(next_url)
    url = f'https://dl.131437.xyz{next_url}'
    # print(next_url)
    # print(info)
    # print(title)
    if next_url == '/book/douluodalu1/3.html':
        break
