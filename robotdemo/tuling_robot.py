# -*- coding:utf-8 -*-

from wxpy import *
import requests,json

api_key='f6978801a9394cdf8c01df6340cf1aa8'
cache_path = 'E:\privateFile\pythonProject\wxpy.pkl'

#方法一
# bot = Bot(cache_path=cache_path)
# tuling = Tuling(api_key=api_key)
# print('图灵机器人已经启动')
# my_friends = bot.friends().search('北极星')[0]

#如果想对所有好友实现机器人回复把参数my_friend改成 chats = [Friend]
#使用图灵机器人自动与指定好友聊天
# @bot.register(chats = [Friend])
# def reply_my_friend(msg):
#     tuling.do_reply(msg)

#进行交互式的Python 命令行页面，并堵塞当前线程
#embed()

def auto_ai(text):
    url = 'http://www.tuling123.com/openapi/api'
    payload = {
        'key':api_key,
        'info':text,
        'userid':'老表'
    }
    r = requests.post(url=url,data=json.dumps(payload))
    result = json.loads(r.content)
    return '【嘟嘟机器人】 ' + result['text']

bot = Bot(cache_path=cache_path)
print('嘟嘟机器人已启动')

my_friends = bot.friends().search('北极星')[0]

@bot.register(my_friends)
def my_friend_message(msg):
    print('[接收]'+str(msg))
    if msg.type != 'Text':
        ret = '你给我看了什么！[拜托]'
    else:
        ret = auto_ai(msg.text)

    print('【发送】'+str(ret))
    return ret

embed()
















