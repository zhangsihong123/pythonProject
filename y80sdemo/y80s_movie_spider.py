# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests,os,time

if __name__=='__main__':
    server = 'https://www.80s.tw/'
    url = 'https://www.80s.tw/movie/list'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    r = requests.get(url=url,headers=headers)
    bf = BeautifulSoup(r.text,'lxml')
    clearfix = bf.find('ul',class_='me1 clearfix')
    clearfix_bf = BeautifulSoup(str(clearfix),'lxml')
    div_a = clearfix_bf.find_all('a')

    #print(div_a)

    for a in div_a:
        a_bf = BeautifulSoup(str(a),'lxml')
        href = a_bf.a.get('href')
        url_info = server+href
        print('详情链接',server + href) #迅雷谜中电影详情链接
        info = requests.get(url=url_info,headers=headers)
        print(info.text)
        info_bf = BeautifulSoup(info.text,'lxml')
        clearfix_block1 = info_bf.find_all('div',class_='clearfix block1')
        print(clearfix_block1)


    print('下载完毕')


    #下载图片的#######################
    #p = clearfix_bf.find_all('img',class_='p')

    # for each in p:
    #     img_bf = BeautifulSoup(str(each),'lxml')
    #     name = img_bf.img.get('alt')
    #     img_id = img_bf.img.get('id')
    #     img_url = 'http:' + img_bf.img.get('src')
    #     print(name,' \n img: ',img_id,' \n src: ', img_url)
    #     print('下载 ',name)
    #     if 'y80s' not in os.listdir():
    #         os.makedirs('y80s')
    #     urlretrieve(url=img_url,filename='y80s/'+name.replace('/','-')+'.jpg')
    #     time.sleep(1)












