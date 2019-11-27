from bs4 import BeautifulSoup
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" id="key"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!--Elsie--></a>
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup=BeautifulSoup(html_doc,'lxml')
# print(type(soup))
# print(soup)

# 格式化输出
# print(soup.prettify())

# BeautifulSoup有4个对象

# Tag标签 NavigableString内容 BeautifulSoup对象

# # 1、tag标签
# print(soup.title)# 获得标题标签
# # 两个属性:name attrs
# print(soup.name)
# print(soup.head.name)
#
# # attrs
# print(soup.p.attrs)# 获得标签属性信息返回字典
# print(soup.p['id'])
#
# # 2、NavigableString内容
# print(soup.p.string)
#
# # 3、BeautifulSoup对象
# print(soup.name)

# 4、Comment类型(注释信息)

# # 遍历文档树
# # 1.子标签节点
# # contents(返回的是列表)
# print(soup.body.contents)
# for bs in soup.body.contents:
#     print(type(bs))# 返回NavigableString Tag对象
#
# # children
# # 返回生成器
# print(soup.body.children)
# for bs in soup.body.children:
#     print(type(bs))

# 2.节点内容
# print(soup.head.string)# 返回标签字符串
# print(soup.body.string)# 包含多个子标签时返回None
# print(soup.body.p.string)

# print(soup.body.strings)# 返回标签下的所有内容,是一个生成器对象
# for s in soup.body.strings:
#     print(s)

# print(soup.body.get_text())# 返回标签下的所有内容

# 3.父节点
# parent
# p=soup.p
# print(p)
# print(p.parent)# 返回某个节点的父节点
#
# # 返回某个节点的所有父节点以及上层节点
# print(p.parents)
# for parent in p.parents:
#     print(parent)
#     print("*******")

# 4.兄弟节点
# next_sibling previous_sibling next_siblings previous_siblings
# print(soup.body.contents)
# print(soup.p)
# print(soup.p.next_sibling.next_sibling)
# print(soup.p.previous_sibling)

# # next_element previous_element next_elements previous_elements
# print(soup.head.next_sibling.next_sibling)# 查看下面一个兄弟标签
# print(soup.head.next_element)# 查看下一个标签

# 搜索文档树
# 1.find_all搜索指定的tag对象的子节点,并通过调节进行判断筛选
# # 查找所有的p标签
# print(soup.find_all("p"))# 返回列表
#
# # 查找多个标签
# print(soup.find_all(["a","b"]))

# 通过属性查找
# print(soup.find_all(id="key"))
# # <a href="http://example.com/elsie" class="sister" id="link1"><!--Elsie--></a>
# print(soup.find_all(href="http://example.com/elsie"))
# print(soup.find_all(class_="sister"))
# print(soup.find_all(class_="sister",id="link1"))
# print(soup.find_all("p",class_="title"))

# print(soup.find_all(attrs={"class":"sister","id":"link1"}))

# print(soup.find(attrs={"class":"sister"}))# 标签对象
# print(soup.find("body").text)# 标签对象类似于get_text()





