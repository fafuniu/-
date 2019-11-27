import requests
import json,time,random
from multiprocessing import Pool
import pymysql
'http://www.7799520.com/api/user/pc/list/search?marry=1&page=2'

def get_json(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
        response=requests.get(url,headers=headers,timeout=10)
        if response.status_code==200:
            return response.content.decode("utf-8")
        else:
            print("返回状态码错误!!!")
            return None

    except Exception as e:
        print("请求出现错误,错误类型是%s"%e)
        return None

def get_data(html):
    info_list=[]
    dicts = json.loads(html)['data']['list']
    # print(json.dumps(data,indent=4))
    for dt in dicts:
        print(dt)
        print('-' * 30)
        userid = dt['userid']
        province = dt['province']
        city = dt['city']
        height = dt['height']
        education = dt['education']
        username = dt['username'].replace(","," ")
        monolog = dt['monolog'].replace("\n", " ")
        birthdayyear = dt['birthdayyear']
        gender = dt['gender']
        d = {'1': '男', '2': '女'}
        gender = d[gender]
        salary = dt['salary']
        marry = dt['marry']
        info_list.append([userid, username, gender, height, marry, education, birthdayyear, salary, province, city, monolog])
    return info_list
    # time.sleep(random.uniform(3,10))

def save(info_list):
    with open("我主良缘信息表.csv",'a',encoding='utf-8-sig') as f:
        for line in info_list:
            f.write(','.join(line))
            f.write('\n')

def create_table():
    conn = pymysql.connect(host="localhost", user="root", password="123456", db="spider", charset="utf8")
    cursor = conn.cursor()
    create_sql = """
        create table if not exists `wzly`(`用户id` varchar(255) not null primary key,`用户名` varchar(255) not null,`性别` varchar(20) not null,`身高` int(11) not null,
        `婚姻状况` varchar(255) not null,`教育水平` varchar(255) not null,`出生年份` int(11) not null,`薪水` varchar(255) not null,`省份` varchar(255) not null,
        `城市` varchar(255) not null,`个性签名` varchar(255) not null)
        """
    # 用户id,用户名,性别,身高,婚姻状况,教育水平,出生年份,薪水,省份,城市,个性签名
    cursor.execute(create_sql)
    conn.commit()
    cursor.close()
    conn.close()

def save_to_mysql(info_list):
    conn=pymysql.connect(host="localhost",user="root",password="123456",db="spider",charset="utf8")
    cursor=conn.cursor()
    insert_sql="insert into `wzly` values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for line in info_list:
        try:
            cursor.execute(insert_sql,line)
        except Exception as e:
            print("{0}此信息数据库中已存在{0}".format("-"*15))
            continue
    conn.commit()
    cursor.close()
    conn.close()

def main(i):
    start_url='http://www.7799520.com/api/user/pc/list/search?marry=1&page={}'.format(i+1)
    print("-----------当前请求的网页是%s--------------"%start_url)
    try:
        html= get_json(start_url)
        info_list=get_data(html)
        # save(info_list)
        save_to_mysql(info_list)
    except Exception as e:
        print("{0}网页解析出现错误:{1}{0}".format('-'*30,e))
        time.sleep(10)
if __name__ == '__main__':
    # with open("我主良缘信息表.csv",'w',encoding='utf-8-sig') as f:
    #     f.write('用户id,用户名,性别,身高,婚姻状况,教育水平,出生年份,薪水,省份,城市,个性签名\n')
    create_table()
    start = time.time()
    pool = Pool()
    pool.map(main, range(300))
    pool.close()
    pool.join()
    end = time.time()
    print("{0}程序运行总时间为{1}秒{0}".format("-" * 15, end - start))
