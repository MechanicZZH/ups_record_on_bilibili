from bs4 import BeautifulSoup

list = []
with open('C:/Users/zhang/Desktop/vtb.html', 'r', encoding='UTF-8')as wb_data:            #python打开本地网页文件
    soup = BeautifulSoup(wb_data, 'lxml')
    for child in soup.select('.space'):
        #id = child.select('#space')#[0].text.strip()
        id = child.string[1:-1]
        print(id)
        list.append(id)

    print(list)