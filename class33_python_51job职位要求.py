from wordcloud import WordCloud,STOPWORDS
import re
from collections import Counter
import numpy as np
import PIL.Image as image
import jieba
f=open('51job技能.txt',encoding='utf-8')
word=f.read().lower()# 读取文本
f.close()
# print(word)
# print(len(word),type(word))
job_all=re.findall("[^a-zA-Z0-9]+",word)
job_string=''.join(job_all)
result=jieba.cut(job_string)

# 设置背景图片
mask=np.array(image.open(r"E:\代码\Python文件\课件中心\数据分析模块\爱心.jpg"))
wordcloud=WordCloud(
    mask=mask,
    background_color='white',
    min_font_size=0,max_font_size=500,
    stopwords=STOPWORDS,
    font_path=r"C:\Windows\Fonts\msyh.ttc",
    random_state=20
).generate(' '.join(result))
image_product=wordcloud.to_image()
# image_product.show()
wordcloud.to_file("爱心词云图.png")
