# -*- coding:utf-8 -*-

import requests,sys
from bs4 import BeautifulSoup

# 笔趣看
class BiqukanSpider():

    def __init__(self):
        self._server = 'http://www.biqukan.com/'
        self._target = 'http://www.biqukan.com/1_1094/'
        self.names = [] #名称
        self.urls = [] #章节链接
        self.nums = 0 #章节数

    def get_server(self):
        return self._server

    def get_target(self):
        return self._target

    """
    获取章节下载链接
    """
    def get_download_url(self):
        r = requests.get(url=self.get_target())
        bf = BeautifulSoup(r.text,'lxml')
        list_main = bf.find_all('div',class_='listmain')
        a_bf = BeautifulSoup(str(list_main[0]),'lxml')
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.get_server()+each.get('href'))

    """
    获取章节内容
    :param target - 下载链接(string)
    
    :return show_txt - 章节内容
    
    """
    def get_contents(self,target):
        r = requests.get(url=target)
        bf = BeautifulSoup(r.text,'lxml')
        show_txt = bf.find_all('div',class_='showtxt')
        show_txt = show_txt[0].text.replace('\xa0'*8,'\n\n')
        return show_txt

    """
    将下载的章节内容写进文件
    :param
    name - 文件名称
    path - 保存路径
    text - 文件内容
    """
    def writer(self,name,path,text):
        with open(path,'a',encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__=='__main__':
    biqukan = BiqukanSpider()
    biqukan.get_download_url()
    for i in range(biqukan.nums):
        #print('名称：',biqukan.names[i],'链接：',biqukan.urls[i])
        biqukan.writer(biqukan.names[i],'一念永恒.txt',biqukan.get_contents(biqukan.urls[i]))
        sys.stdout.write('已下载:%.3f%%' % float(i/biqukan.nums)+'\r')
        sys.stdout.flush()
    print('《一念永恒》下载完成')











