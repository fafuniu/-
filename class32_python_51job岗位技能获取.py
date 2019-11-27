import time,random
import requests
from lxml import etree
import re
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

def get_url_list(html):
    html=etree.HTML(html)
    urls=html.xpath('/html/body/div[2]/div[4]/div/p/span/a/@href')
    return urls# 返回详细信息的链接

def parse_html(html):
    html=etree.HTML(html)
    divs=html.xpath("//div[@class='bmsg job_msg inbox']")[0]
    info=divs.xpath("string(.)")
    info=re.sub("\s+"," ",info)
    return info

def save_to_txt(info):
    with open("岗位需求.txt",'a',encoding='gbk') as f:
        f.write(info+'\n\n\n')

def main(i):
    start_url='https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%25E5%25B8%2588,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(i+1)
    print("开始访问%s页的信息"%(i+1))
    print(start_url)
    html=get_html(start_url)
    url_list=get_url_list(html)
    for url in url_list:
        try:
            job_html=get_html(url)
            print("--------------正在解析%s--------------"%url)
            info=parse_html(job_html)
            save_to_txt(info)
        except:
            print("跳转到%s网页出现异常"%url)
            continue
        # save_to_csv(info_list)
        # time.sleep(random.uniform(5,10))
if __name__ == '__main__':
    with open("岗位需求.txt", 'w', encoding='gbk') as f:
        f.write('')
    start=time.time()
    pool=Pool()
    pool.map(main,range(100))
    end=time.time()
    print("{0}程序运行总时间为{1}秒{0}".format("-"*15,end-start))





