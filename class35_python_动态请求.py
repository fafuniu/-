'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=0'
'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=20'
'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=40'

import requests
import json
tlist = []
n=0
for i in range(15):
    start_url='https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start={}'.format(20*i)
    response=requests.get(start_url)
    text=response.content.decode('utf-8')
    # print(len(text),type(text))
    data=json.loads(text)
    # print(len(data),type(data))
    # print(data)
    d=json.dumps(data,indent=4)
    # print(d)
    for dt in data['subjects']:
        print(len(dt),type(dt))
        print(dt)
        tlist.append([dt['rate'],dt['title'],dt['url'],dt['cover'],dt['id']])
        n+=1
        print("-"*30)
print("tlist的元素数量",len(tlist),n)
with open('豆瓣选电影.csv','a',encoding='utf-8-sig')as f:
    for line in tlist:
        f.write(','.join(line))
        f.write('\n')