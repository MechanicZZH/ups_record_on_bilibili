from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import json



list = ['16791313','389857131','389857131','491474052']

def videoinfo(url):




#payload = {'keyword': 'keyword'}
for mid in list:
    chrom_opt = webdriver.ChromeOptions()
    chrom_opt.add_argument('--headless')
    chrom_opt.add_argument('--disable-gpu')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrom_opt.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(executable_path="C:/Users/zhang/PycharmProjects/biliS/venv/Scripts/chromedriver.exe", chrome_options=chrom_opt)
    video = browser.get('https://space.bilibili.com/' + mid + '/video')
    time.sleep(0.5)
    soup = BeautifulSoup(browser.page_source , 'html.parser')
    page = soup.select('.be-pager-total')[0].text.strip()
    username = soup.select('#h-name')[0].text.strip()
    print(username)
    page = int(page[2: -3])


    for child in soup.select('.small-item'):
        suburl = child.a['href']
        bvid = suburl[suburl.find('BV'):]
        title = child.select('.title')[0].text.strip()
        length = child.select('.length')[0].text.strip()


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
        # title = video.select('.video-title')[0].text.strip()
        if video.select('.video-data'):
            data = video.select('.video-data')[0].text.strip()
            data = [data[4:]]
            for i in range(0, len(date)):
                date = date[i].split("20")[1]
            print(date)
        # username = video.select('.username')[0].text.strip()

        subhtml = requests.get('https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + bvid, headers=headers)
        subhtml.encoding = subhtml.apparent_encoding
        infojson = subhtml.text
        infojson = infojson[infojson.find('data') + 6:-1]
        videoinfo = json.loads(infojson)
        videolist = []
        videolist.append([title, data, username, bvid, videoinfo["view"], videoinfo["danmaku"], videoinfo["reply"],
                          videoinfo["favorite"], videoinfo["coin"], videoinfo["share"], videoinfo["like"]])
        print(videolist)



    if page != 1:
        page = range(page - 1)
        for i in page:
            video = browser.get('https://space.bilibili.com/' + mid + '/video?tid=0&page=' + str(i + 2) + '&keyword=&order=pubdate')
            time.sleep(0.5)
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            username = soup.select('#h-name')[0].text.strip()
            for child in soup.select('.small-item'):
                suburl = child.a['href']
                bvid = suburl[suburl.find('BV'):]
                title = child.select('.title')[0].text.strip()
                length = child.select('.length')[0].text.strip()

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
                # title = video.select('.video-title')[0].text.strip()
                if video.select('.video-data'):
                    data = video.select('.video-data')[0].text.strip()
                    data = data[4:]
                # username = video.select('.username')[0].text.strip()

                subhtml = requests.get('https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + bvid,
                                       headers=headers)
                subhtml.encoding = subhtml.apparent_encoding
                infojson = subhtml.text
                infojson = infojson[infojson.find('data') + 6:-1]
                videoinfo = json.loads(infojson)
                videolist = []
                videolist.append(
                    [title, data, username, bvid, videoinfo["view"], videoinfo["danmaku"], videoinfo["reply"],
                     videoinfo["favorite"], videoinfo["coin"], videoinfo["share"], videoinfo["like"]])
                print(videolist)


