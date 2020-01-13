import sys
import urllib.request
from bs4 import BeautifulSoup
import csv
import pygal
import cityinfo

cityname = input("请输入城市名称：")
if cityname in cityinfo.city:
    citycode = cityinfo.city[cityname]
else
    sys.exit()

url = 'http://www.weather.com.cn/weather/' + citycode + '.shtml'
header = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36")  # 设置头部信息
http_handler = urllib.request.HTTPHandler()
opener = urllib.request.build_opener(http_handler)  # 修改头部信息
opener.addheaders = [header]
request = urllib.request.Request(url) # 制作请求
response = opener.open(request) # 得到应答
html = response.read() # 读取应答
html = html.decode('utf-8') # 设置编码

# 根据得到的页面信息进行初步筛选
final = [] # 使用 final 列表保存数据
bs = BeautifulSoup(html, "html.parser") # 初始化 BS 对象
body = bs.body
data = body.find('div', {'id': '7d'})
print(type(data))
ul = data.find('ul')
li = ul.find_all('li')

# 爬取自己所需的数据
i = 0 # 控制爬取的天数
lows = [] # 保存低温
highs = [] # 保存高温
daytimes = [] # 保存日期
weathers = [] # 保存天气
for day in li: # 快速找到每个 li 节点
    if i < 7:
        temp = [] # 临时存放每日数据
        date = day.find('h1').string # 获取日期
        # print(date)
        temp.append(date)
        daytimes.append(date)
        inf = day.find_all('p')  # 遍历 li 下面的 p 标签 有多个 p 需要使用 find_all 而不是 find

        #print(inf[0].string)  # 提取第一个p标签的值，即天气
        temp.append(inf[0].string)
        weathers.append(inf[0].string)
        temlow = inf[1].find('i').string  # 最低气温
        if inf[1].find('span') is None:  # 天气预报可能没有最高气温
            temhigh = None
            temperate = temlow
        else:
            temhigh = inf[1].find('span').string  # 最高气温
            temhigh = temhigh.replace('℃', '')
            temperate = temhigh + '/' + temlow
        # temp.append(temhigh)
        # temp.append(temlow)
        lowStr = ""
        lowStr = lowStr.join(temlow.string)
        lows.append(int(lowStr[:-1]))  # 以上三行将低温 NavigableString 转成 int 类型并存入低温列表
        if temhigh is None:
            highs.append(int(lowStr[:-1]))
        else:
            highStr = ""
            highStr = highStr.join(temhigh)
            highs.append(int(highStr))  # 以上三行将高温 NavigableString 转成 int 类型并存入高温列表
        temp.append(temperate)
        final.append(temp)
        i = i + 1

# 将最终的获取的天气写入 csv 文件
with open('weather.csv', 'a', errors='ignore', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerows([cityname])
    f_csv.writerows(final)

# 使用 pygal 完成绘图，并存储为 svg 格式
bar = pygal.Line()  # 创建折线图
bar.add('最低气温', lows)
bar.add('最高气温', highs)

bar.x_labels = daytimes
bar.x_labels_major = daytimes[::30]
# bar.show_minor_x_labels = False  # 不显示 X 轴最小刻度
bar.x_label_rotation = 45

bar.title = cityname+'未来七天气温走向图'
bar.x_title = '日期'
bar.y_title = '气温(摄氏度)'

bar.legend_at_bottom = True

bar.show_x_guides = False
bar.show_y_guides = True

bar.render_to_file('temperate.svg')
