# -*- coding:utf-8 -*-

from wxpy import *
import  time

# 初始化一个机器人对象
bot = Bot(cache_path='E:\privateFile\pythonProject\wxpy.pkl')
# 向文件传输助手发送消息
#bot.file_helper.send("hello,I'm 嘟嘟")

#查找朋友，并向朋友发送消息
my_friends = bot.friends(update=False)

#查看自己好友数(除了自己)
print('我的好友数：'+str(len(my_friends)-1))

#获取我的群组数[返回列表包含Groups对象]
my_groups = bot.groups(update=False)
print('我的微信群聊数：'+str(len(my_groups)))

#查看我关注的微信公众号[返回列表包含Chats对象]
mps = bot.mps(update=False)
print('我关注的微信公众号数：'+str(len(mps)))

friend = my_friends.search('北极星')[0]
#发送消息
friend.send('Good morning,the early bird catches the worm!(早上好，早起的鸟儿有虫吃！)')

















