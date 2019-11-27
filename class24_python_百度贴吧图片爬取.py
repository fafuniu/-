import requests
import re
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
number=1
for i in range(6):
    url='https://tieba.baidu.com/p/5815297430?pn={}'.format(i+1)
    response=requests.get(url,headers=headers)
    text=response.content.decode('utf-8')
    print(type(text),len(text))
    # print(text)
    pattern=re.compile(r'src="(https://imgsa.baidu.com/forum/.+?jpg)"')
    pic_list=re.findall(pattern,text)
    for pic in pic_list:

        response=requests.get(pic,headers=headers)
        path=r'E:\代码\Python文件\mypy_class03\百度贴吧图片\图片{}.jpg'.format(number)
        with open(path,'wb')as f:
            print("正在下载第%s张图片"%number)
            f.write(response.content)
        number+=1

# 函数式编程
# 请求url get_html
# 解析网页 parse_html
# 文本保存 save_to_picture






