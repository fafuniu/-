from lxml import etree
text='''
    <html>
        <head>
            <title>春晚</title>
        </head>
        <body>
            <h1 name="title">个人简介</h1>
            <div name="desc">
                <p name = "name" id="123">姓名：<span>小岳岳</span></p>
                <p name = "addr" class="abc">住址：中国 河南</p>
                <p name="info">代表作：五环之歌</p>
            </div>
            <div name="desc">
                <p name = "name" id="123">姓名：<span>小岳岳</span></p>
                <p name = "addr" class="abc">住址：中国 河南</p>
                <p name="info">代表作：五环之歌</p>
            </div>
'''
# 初始化
html=etree.HTML(text)
print(html)

# 用全路径查询标签获取信息
p_x=html.xpath('/html/head/title')# 返回列表对象
# print(p_x[0].text)# 获取里面的文本信息
# print("-"*20)
# p_x=html.xpath('/html/head/title/text()')# 返回列表对象,包含的是所有符合要求标签下的文本信息
# print(p_x[0])
# print("-"*20)
# p_x=html.xpath('/html/body/div/p')#
# print(p_x)
# for p in p_x:
#     print(p.text)
# print("-"*20)
# p_x = html.xpath('/html/body/div/p/text()')  #将多个标签内的文本信息以列表形式返回
# print(p_x)
# print("-"*20)
#
# # 获得多个相同标签中指定的标签信息
# p_x = html.xpath('/html/body/div/p[2]/text()')  #返回列表,包含指定标签内的内容
# print(p_x)
# print("-"*20)

# 获得标签中的其他信息
# p_x = html.xpath('/html/body/div/p[2]/@class')  #返回列表,包含标签指定属性
# print(p_x)
# print("-"*20)
# p_x = html.xpath('/html/body/div/p[2]/@name')  #返回列表,包含标签指定属性
# print(p_x)
print("-"*20)

# 其他方法查询标签
# p_x=html.xpath("//p")# 查询到所有的p标签
# print(p_x)
# print("-"*20)
# p_x=html.xpath("//div")# 查询到所有的div标签
# print(p_x)
print("-"*20)

# # 查询所有的标签属性
# p_x=html.xpath("//@id")
# print(p_x)
# print("-"*20)

# # 通过标签属性查询指定的标签(重点)
# p_x=html.xpath("//p[@name='info']/text()")
# print(p_x)
print("-"*20)

p_x=html.xpath("//p[@id='123']/text()")
print(p_x)
print("-"*20)

# # 提取一个标签下的所有字符信息
# p_x=html.xpath("//p[@id='123']")
# for p in p_x:
#     print(p.xpath('string(.)'))
# print("-"*20)
# divs=html.xpath("//div[@name='desc']")
# print(divs[0].xpath('string(.)'))

# # 访问最后一个p标签
# p_x=html.xpath("//p[last()]/text()")
# print(p_x)
# print("-"*20)
# p_x=html.xpath("//p[last()-1]/text()")
# print(p_x)
# print("-"*20)

# 构建多个xpath标签对象

# divs=html.xpath("//div")
# print(divs)
# print(divs[0].xpath("p"))


