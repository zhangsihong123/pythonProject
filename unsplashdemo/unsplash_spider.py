# -*- coding:utf-8 -*-

import requests,json

class UnSplashSpider():
    server = 'http://unsplash.com/napi/feeds/home'
    headers = {'authorization':'unsplash.com'}
    r = requests.get(url=server,headers=headers,verify=False)
    html = json.loads(r.text)
    next_page = html['next_page']
    print('下一页地址:', next_page)
    for each in html['photos']:
        print('图片ID:', each['id'])




# if __name__=='__main__':
#     pass



