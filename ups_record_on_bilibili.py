from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import json
import csv
import random
import xlrd


n = 2 #从这个人对应的行数n开始，与序号无关
m = 6 #mid为单行数据的第m个，m从0开始计算


def LoadUserAgent(uafile):
    uas = []
    with open(uafile,'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1])
    random.shuffle(uas)
    return uas


uas = LoadUserAgent("user_agents.txt")

'''list = []
i = 0

list = []
filename = 'C:/Users/zhang/Desktop/list.csv'
with open(filename,'r', encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        i+= 1
        if i >=7: #从第n行开始
            list.append(row[6])#mid列号
    print(list)
    print(len(list))'''


list = []
data = xlrd.open_workbook('C:/Users/zhang/Desktop/给D100的表格.xlsx')
table = data.sheet_by_name(data.sheet_names()[0])
for i in range(n - 1,table.nrows):
    list.append(str(table.row_values(i)[6])[:-2])
print(list)
print(len(list))


def videoinfo(child):

        ua = random.choice(uas)

        global date
        suburl = child.a['href']
        bvid = suburl[suburl.find('BV'):]
        title = child.select('.title')[0].text.strip()
        length = child.select('.length')[0].text.strip()

        payload = {'keyword': 'keyword'}
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                   "Accept-Encoding": "gzip",
                   "Accept-Language": "zh-CN,zh;q=0.8",
                   "Referer": "http://www.bilibili.com/",
                   "User-Agent": ua}



        # username = video.select('.username')[0].text.strip()
        while True:
            r = requests.get('https://www.bilibili.com/video/' + bvid, params=payload, headers=headers)
            time.sleep(0.5)
            r.raise_for_status
            r.encoding = 'utf-8'
            video = BeautifulSoup(r.text, 'html.parser')
            # soup = soup.select('#viewbox_report')
            # title = video.select('.video-title')[0].text.strip()
            if video.select('.video-data'):
                date = video.select('.video-data')[0].text.strip()
                date = date[4:]
                date = date[date.find('20'):date.find(' ')]

            subhtml = requests.get('https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + bvid, headers=headers)

            time.sleep(0.5)
            subhtml.encoding = subhtml.apparent_encoding
            infojson = subhtml.text
            allvideoinfo = json.loads(infojson)
            if allvideoinfo['code'] == 0:

                videoinfo = allvideoinfo['data']
                videolist = []
                videolist.append([title, date, username, videoinfo["aid"], bvid, length, videoinfo["view"], videoinfo["danmaku"], videoinfo["reply"],
                                  videoinfo["favorite"], videoinfo["coin"], videoinfo["share"], videoinfo["like"]])
                for videoinfo_useful in videolist:
                    print(videoinfo_useful)
                    writer.writerow(videoinfo_useful)
                break
            else:
                print('10min')
                time.sleep(600)


# payload = {'keyword': 'keyword'}
with open('C:/Users/zhang/Desktop/videoinfo/VTBsinfo.csv', 'w', newline='',encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['标题', '上传日期', 'up主', 'av号', 'bv号','时长', '观看', '弹幕', '评论', '收藏', '硬币', '分享', '点赞'])
    for mid in list:
        chrom_opt = webdriver.ChromeOptions()
        chrom_opt.add_argument('--headless')
        chrom_opt.add_argument('--disable-gpu')
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrom_opt.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(executable_path="C:/Users/zhang/PycharmProjects/biliS/venv/Scripts/chromedriver.exe",
                                   chrome_options=chrom_opt)
        video = browser.get('https://space.bilibili.com/' + mid + '/video')
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        page = soup.select('.be-pager-total')[0].text.strip()
        username = soup.select('#h-name')[0].text.strip()
        print(username)
        page = int(page[2: -3])

        for child in soup.select('.small-item'):

            videoinfo(child)


        if page != 1:
            page = range(page - 1)
            for i in page:
                video = browser.get(
                    'https://space.bilibili.com/' + mid + '/video?tid=0&page=' + str(i + 2) + '&keyword=&order=pubdate')
                time.sleep(2)
                soup = BeautifulSoup(browser.page_source, 'html.parser')

                username = soup.select('#h-name')[0].text.strip()
                for child in soup.select('.small-item'):
                    videoinfo(child)