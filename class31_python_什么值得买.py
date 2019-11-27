import requests
from bs4 import BeautifulSoup
import time
import pymysql
from multiprocessing import Pool
import random
def get_html(url):
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
             'host':'www.smzdm.com',
             'referer':'https://www.smzdm.com/'}
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.content.decode("utf-8")
        else:
            print("响应状态码错误")
    except:
        print("请求网页出现错误")

def parse_html(html):
    soup=BeautifulSoup(html,'lxml')
    all_li=soup.find_all("li",class_="feed-row-wide")
    tlist=[]
    for li in all_li:
        # print(type(li))
        # print(li)
        title=li.h5.a.text # 标题
        # 白菜 食品 游戏 电脑 历史低价 数码 耳机
        url=li.h5.a['href'] # 链接
        recommender=li.find("div",class_="feed-block-info").span.text[4:]# 推荐人
        try:
            label= li.find("div", class_="feed-block-info").find_all("span")[1].text.replace(" ","").replace("\n"," ")[5:]
        except:
            print("此商品没有标签")
            label=''
        zhi=li.find_all("span",class_="unvoted-wrap")[0].text.strip()
        buzhi=li.find_all("span",class_="unvoted-wrap")[1].text.strip()
        collect=li.find("a",class_="J_zhi_like_fav z-group-data").span.text
        comment=li.find("a",class_='z-group-data').span.text
        date=li.find("span",class_="feed-block-extras").text.split("\n")[0].strip()# 2019-4-28 15:27:00
        if len(date)>6:
            print("{0}此信息发布时间不是今天{0}".format("-" * 15))
            continue
            # date=time.strftime("%Y-",time.localtime())+date+':00'
        else:
            date=time.strftime("%Y-%m-%d ",time.localtime())+date+':00'# 15:27 --> 2019-4-28 15:27:00
        mall=li.find("span",class_="feed-block-extras").text.split("\n")[1].strip()
        if int(zhi)+int(buzhi)!=0:
            rate=round(int(zhi)/(int(zhi)+int(buzhi)),3)
            if rate>0.8 and int(comment)>15:
                tlist.append([title,rate,zhi,buzhi,label,collect,comment,recommender,mall,date,url])
            else:
                continue
        else:
            continue
        # print([title,zhi,buzhi,label,collect,comment,recommender,mall,date,url])
    return tlist
def create_table():
    conn = pymysql.connect(host="localhost", user="root", password="123456", db="spider", charset="utf8")
    cursor = conn.cursor()
    create_sql = """
        create table if not exists `smzdm`(`标题` varchar(255) not null primary key,`好评比` float not null,`值` int(11) not null,`不值` int(11) not null,
        `标签` varchar(255) not null,`收藏` int(11) not null,`评论` int(11) not null,`推荐人` varchar(255) not null,`平台` varchar(255) not null,
        `日期` datetime not null,`链接` varchar(255) not null)
        """
    cursor.execute(create_sql)
    conn.commit()
    cursor.close()
    conn.close()

def save_to_mysql(info_list):
    conn=pymysql.connect(host="localhost",user="root",password="123456",db="spider",charset="utf8")
    cursor=conn.cursor()
    insert_sql="insert into `smzdm` values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for line in info_list:
        try:
            cursor.execute(insert_sql,line)
        except Exception as e:
            print("{0}此信息数据库中已存在{0}".format("-"*15))
            delete_sql="delete from `smzdm` where `标题`=%s"
            cursor.execute(delete_sql,line[0])
            print("{0}删除一条已存在信息{0}".format("-" * 15))
            cursor.execute(insert_sql, line)
    conn.commit()
    cursor.close()
    conn.close()

def main(i):
    url='https://www.smzdm.com/jingxuan/p{}/'.format(i+1)
    html=get_html(url)
    info_list=parse_html(html)
    print("正在访问第%s页"%(i+1))
    save_to_mysql(info_list)
    # time.sleep(random.uniform(3,10))

if __name__ == '__main__':
    create_table()# 创建数据表
    start=time.time()
    pool=Pool()# 2 68 # 4 31 # 8 19 # 16 17 #32 20
    pool.map(main,range(30))
    pool.close()
    pool.join()# 挂起
    end=time.time()
    print("{0}程序运行总时间为{1}秒{0}".format("-"*15,end-start))