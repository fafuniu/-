import time,random
import requests
from lxml import etree
import pymysql
from multiprocessing import Pool
def get_html(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.content.decode("gbk")
        else:
            print("返回状态码错误!!!")
    except Exception as e:
        print("请求出现错误,错误类型是%s"%e)

def parse_html(html):
    html=etree.HTML(html)
    t_list=[]
    zwmc=html.xpath('/html/body/div[2]/div[4]/div[@class="el"]/p/span/a/text()')
    gsmc=html.xpath('/html/body/div[2]/div[4]/div[@class="el"]/span[1]/a/text()')
    gsdd=html.xpath('/html/body/div[2]/div[4]/div[@class="el"]/span[2]/text()')
    gz=html.xpath('/html/body/div[2]/div[4]/div[@class="el"]/span[3]')
    gz=list(map(lambda x:x.xpath("string(.)"),gz))
    fbsj=html.xpath('/html/body/div[2]/div[4]/div[@class="el"]/span[4]/text()')
    # 查看每个元素的数量
    # print(len(zwmc),len(gsmc),len(gsdd),len(gz),len(fbsj))
    # 统计最低和最高薪酬
    # 转换单位 空的数据

    for i in range(len(zwmc)):
        try:
            if len(gz[i])!=0:
                if gz[i].find("元")!=-1:
                    low=float(gz[i][:gz[i].find("元")])*22
                    high=float(gz[i][:gz[i].find("元")])*22
                elif gz[i][-4:-1]=="以下/":
                    # low=float(gz[i][:gz[i].find("万")])*10000/12
                    # high=float(gz[i][:gz[i].find("万")])*10000/12
                    low=0
                    high=0
                else:
                    gz_split=gz[i].split('-')
                    if gz[i][-3:]=="万/月":
                        low=float(gz_split[0])*10000
                        high=float(gz_split[1][:gz_split[1].find("万")])*10000
                    elif gz[i][-3:]=="千/月":
                        low = float(gz_split[0])*1000
                        high = float(gz_split[1][:gz_split[1].find("千")])*1000
                    elif gz[i][-3:]=="万/年":
                        low =float(gz_split[0])*10000/12
                        high =float(gz_split[1][:gz_split[1].find("万")])*10000/12
                    else:
                        print("未考虑的情况")
                        assert 1>2
            else:
                low=0
                high=0
        except Exception as e:
            print("异常情况:%s"%e)
            print("异常数据为%s"%gz[i])
            low=0
            high=0
        t_list.append([zwmc[i].strip().replace(",",""),gsmc[i],gsdd[i],str(round(low,-2)),str(round(high,-2)),fbsj[i]])
        # print(t_list[i])
    return t_list

def save_to_mysql(info_list):
    conn=pymysql.connect(host="localhost",user='root',password='123456',db='spider',charset='utf8')
    cursor=conn.cursor()
    insert_sql="insert into 51_job values(%s,%s,%s,%s,%s,%s,%s)"
    for line in info_list:
        try:
            addline=[''.join(line[:5])]+line
            # print(addline)
            cursor.execute(insert_sql,addline)
        except Exception as e:
            print("{0}此数据数据库中已经存在{0}".format("-"*15))
            continue
        # set_string=''.join(line[:5])
        # if set_string in job_set:
        #     print("{0}此数据数据库中已经存在{0}".format("-"*15))
        # else:
        #     job_set.add(set_string)
        #     cursor.execute(insert_sql,line)
    # cursor.executemany(insert_sql,info_list)
    conn.commit()
    cursor.close()
    conn.close()

def main(i):
    start_url='https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%25E5%25B8%2588,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(i+1)
    print("开始访问%s页的信息"%(i+1))
    print(start_url)
    html=get_html(start_url)
    info_list=parse_html(html)
    save_to_mysql(info_list)
    # time.sleep(random.uniform(5,10))
if __name__ == '__main__':
    job_set=set()
    start=time.time()
    # for i in range(100):
    #     main(i)
    pool=Pool()
    pool.map(main,range(100))# main(0) main(1) main(2) ... main(88)
    pool.close()
    pool.join()
    end=time.time()
    print("程序运行时间为%s"%(end-start))