from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import csv
import json

table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

def dec(x):
	r=0
	for i in range(6):
		r+=tr[x[s[i]]]*58**i
	return (r-add)^xor

page = range(900)

def getHTMLText(url):


    with open('C:/Users/zhang/Desktop/videoinfo/video.csv', 'w', newline='',encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['标题', '上传日期', 'up主', 'av号', 'bv号','观看', '弹幕', '评论', '收藏', '硬币', '分享', '点赞'])
        print(page)

        for i in page:

            headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                       "Accept-Encoding": "gzip",
                       "Accept-Language": "zh-CN,zh;q=0.8",
                       "Referer": "http://www.bilibili.com/",
                       "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}

            chrom_opt = webdriver.ChromeOptions()
            chrom_opt.add_argument('--headless')
            chrom_opt.add_argument('--disable-gpu')
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrom_opt.add_experimental_option("prefs", prefs)
            browser = webdriver.Chrome(executable_path="C:/Users/zhang/PycharmProjects/biliS/venv/Scripts/chromedriver.exe", chrome_options=chrom_opt)


            browser.get(url + str(page[i]+851))

            time.sleep(0.5)
            soup = BeautifulSoup(browser.page_source , 'html.parser')
            browser.quit()
            #print(soup)
            for child in soup.select('.l-item'):
                suburl = child.a['href']
                bvid = suburl[suburl.find('BV'):]
                aid = dec(bvid)
                username = child.select('.v-author')[0].text.strip()
                title = child.select('.title')[0].text.strip()

                payload = {'keyword': 'keyword'}
                headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                           "Accept-Encoding": "gzip",
                           "Accept-Language": "zh-CN,zh;q=0.8",
                           "Referer": "http://www.bilibili.com/",
                           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
                r = requests.get('https://www.bilibili.com/video/' + bvid, params=payload, headers=headers)
                r.raise_for_status
                r.encoding = 'utf-8'
                video = BeautifulSoup(r.text, 'html.parser')
                # soup = soup.select('#viewbox_report')
                #title = video.select('.video-title')[0].text.strip()
                if video.select('.video-data'):
                    data = video.select('.video-data')[0].text.strip()
                    data = data[4:]
                #username = video.select('.username')[0].text.strip()


                subhtml = requests.get('https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + bvid , headers=headers)
                subhtml.encoding = subhtml.apparent_encoding
                infojson = subhtml.text
                infojson = infojson[infojson.find('data') + 6:-1]
                videoinfo = json.loads(infojson)
                videolist = []
                videolist.append([title, data, username, aid, bvid, videoinfo["view"], videoinfo["danmaku"], videoinfo["reply"],videoinfo["favorite"], videoinfo["coin"], videoinfo["share"], videoinfo["like"]])
                print(i)
                for videoinfo_useful in videolist:
                    print(videoinfo_useful)
                    writer.writerow(videoinfo_useful)



if __name__ == "__main__":
    url = "https://www.bilibili.com/v/dance/otaku/#/47977/default/0/"
    print(getHTMLText(url))



