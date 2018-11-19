#-*- coding:utf-8 -*-

#写入数据的工具类
class FileManager(object):

    #写一个写入数据的接口
    @classmethod
    def write(self, filename, content, split = '\n'):
        '''
        :param content:要写入的数据
        :param split: 每条数据之间的分隔符
        :return:
        '''
        #判断传入的参数是否为字符串类型，如果是，写入数据，如果不是则抛出异常
        if isinstance(content, str):
            #打开文件
            f = open(filename, 'a')
            #写入数据
            f.write(content)
            f.write(split)
            #关闭文件
            f.close()
        else:
            raise TypeError('content must be a str!')
    #写入多行数据
    @classmethod
    def writelines(self, filename, str_list, split= '\n'):
        rs = isinstance(str_list, list)
        #判断某个对象是否是某个类型，如果是返回True，如果不是返回False
        if rs:
            #遍历列表，取出每一数据，判断数据类型是否为字符串
            for content in str_list:
                #如果不是字符串类型
                if isinstance(content, str) == False:
                    #抛出异常
                    raise TypeError('str_list must be a list of str!,such as:[str1,str2,...]')
            #如果没抛出异常，就可以写入数据
            f = open(filename, 'a',encoding='utf-8')
            string =split.join(str_list)
            f.write(string)
            f.close()
        else:
            #如果不是列表，抛出异常
            raise TypeError('str_list must be a list of str,ex[str1, str2,...]')

