# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
#from urllib.request import urlretrieve
import requests,os,time
from utils.file_manager import FileManager


if __name__=='__main__':
    server = 'https://www.80s.tw/'
    url = 'https://www.80s.tw/movie/list'
    headers = {
        'Referer':'https://www.80s.tw/movie/list',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36'
    }
    r = requests.get(url=url,headers=headers)
    bf = BeautifulSoup(r.text,'lxml')
    clearfix = bf.find(class_='me1 clearfix')
    clearfix_bf = BeautifulSoup(str(clearfix),'lxml')
    div_a = clearfix_bf.find_all('a')

    #print(clearfix_bf)

    fm = FileManager()

    for a in div_a:
        a_bf = BeautifulSoup(str(a),'lxml')
        href = a_bf.a.get('href')
        url_info = server+href
        print('详情链接',server + href) #迅雷谜中电影详情链接
        info = requests.get(url=url_info,headers=headers)

        info_bf = BeautifulSoup(info.text,'lxml')
        minfo = info_bf.find('div',class_='clearfix',id='minfo')
        img_info = info_bf.find('div', class_='img')

        name = ''
        src_url = ''
        if img_info is not None:
            name = img_info.img.get('title')
            src_url = 'http:'+ img_info.img.get('src')
        print(src_url)

        desc = info_bf.find('div',id='movie_content',class_='clearfix')
        desc_text = ''
        try:
            desc_text = desc.text
        except AttributeError as e:
            desc_text = '暂无介绍'
        print(desc_text)

        video_url = info_bf.find('span',class_='dlname nm')
        try:
            video_thunder = '迅雷链接：'+video_url.span.a.get('href')
        except AttributeError as e:
            video_thunder = '暂无链接'
        print(video_thunder, '\n')
        filename = 'y80s电影大全.txt'
        fm.writelines(filename,str_list=[name,url_info,desc_text,video_thunder+'\n'])
        # fm.write(filename,url_info,split='')
        # fm.write(filename,desc_text,split='')
        # fm.write(filename,video_thunder,split='\n\n')

        time.sleep(1)

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












