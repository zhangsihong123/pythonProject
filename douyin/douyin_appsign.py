# -*- coding:utf-8 -*-
from contextlib import closing
import requests, json, re, os, sys, random
from ipaddress import ip_address
from subprocess import Popen, PIPE
import urllib


class DouYin(object):
    def __init__(self, width=500, height=300):
        """
        抖音App视频下载
        """
        rip = ip_address('0.0.0.0')
        while rip.is_private:
            rip = ip_address('.'.join(map(str, (random.randint(0, 255) for _ in range(4)))))
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
            'X-Real-IP': str(rip),
            'X-Forwarded-For': str(rip),
        }

    def getToken(self):
        req = requests.get('https://api.appsign.vip:2688/token/douyin/version/2.7.0').json()
        return self.save_json(req)

    def getDevice(self):
        req = requests.get('https://api.appsign.vip:2688/douyin/device/new/version/2.7.0').json()
        device_info = req['data']
        return device_info

    def getSign(self, token, query):
        req = requests.post('https://api.appsign.vip:2688/sign', json={'token': token, 'query': query}).json()
        if req['success']:
            sign = req['data']
        else:
            sign = req['success']
        return sign

    def params2str(self, params):
        query = ''
        for k, v in params.items():
            query += '%s=%s&' % (k, v)
        query = query.strip('&')
        return query

    def save_json(self, data):
        with open('douyin.txt', 'w') as f:
            json.dump(data, f, ensure_ascii=False)

    def load_json(self):
        with open('douyin.txt', 'r') as f:
            data = json.load(f)
            return data

    def get_video_urls(self, user_id, type_flag='f'):
        """
        获得视频播放地址
        Parameters:
            user_id：查询的用户ID
        Returns:
            video_names: 视频名字列表
            video_urls: 视频链接列表
            nickname: 用户昵称
        """
        video_names = []
        video_urls = []
        share_urls = []
        unique_id = ''
        max_cursor = 0
        has_more = 1
        device_info = self.getDevice()
        APPINFO = {
            'version_code': '2.7.0',
            'app_version': '2.7.0',
            'channel': 'App%20Stroe',
            'app_name': 'aweme',
            'build_number': '27014',
            'aid': '1128'
        }
        params = {
            'iid': device_info['iid'],
            'idfa': device_info['idfa'],
            'vid': device_info['vid'],
            'device_id': device_info['device_id'],
            'openudid': device_info['openudid'],
            'device_type': device_info['device_type'],
            'os_version': device_info['os_version'],
            'os_api': device_info['os_api'],
            'screen_width': device_info['screen_width'],
            'device_platform': device_info['device_platform'],
            'version_code': APPINFO['version_code'],
            'channel': APPINFO['channel'],
            'app_name': APPINFO['app_name'],
            'build_number': APPINFO['build_number'],
            'app_version': APPINFO['app_version'],
            'aid': APPINFO['aid'],
            'ac': 'WIFI',
            'count': '12',
            'keyword': user_id,
            'offset': '0'
        }
        query = self.params2str(params)
        if not os.path.isfile('douyin.txt'):
            self.getToken()
        token = self.load_json()['token']
        sign = self.getSign(token, query)
        if not sign:
            self.getToken()
            token = self.load_json()['token']
            sign = self.getSign(token, query)
        params['mas'] = sign['mas']
        params['as'] = sign['as']
        params['ts'] = sign['ts']
        headers = {
            'User-Agent': 'Aweme/2.7.0 (iPhone; iOS 11.0; Scale/2.00)'
        }
        req = requests.get('https://api.amemv.com/aweme/v1/general/search/', params=params, headers=headers)
        html = json.loads(req.text)
        uid = html['user_list'][0]['user_info']['uid']
        nickname = html['user_list'][0]['user_info']['nickname']
        unique_id = html['user_list'][0]['user_info']['unique_id']
        if unique_id != user_id:
            unique_id = html['user_list'][0]['user_info']['short_id']
            if unique_id != user_id:
                print('用户ID可能输入错误或无法搜索到此用户ID')
                sys.exit()
        share_user_url = 'https://www.amemv.com/share/user/%s' % uid
        share_user = requests.get(share_user_url, headers=self.headers)
        _dytk_re = re.compile(r"dytk:\s*'(.+)'")
        dytk = _dytk_re.search(share_user.text).group(1)
        print('JS签名下载中')
        urllib.request.urlretrieve(
            'https://raw.githubusercontent.com/Jack-Cherish/python-spider/master/douyin/fuck-byted-acrawler.js',
            'fuck-byted-acrawler.js')
        try:
            process = Popen(['node', 'fuck-byted-acrawler.js', str(uid)], stdout=PIPE, stderr=PIPE)
        except (OSError, IOError) as err:
            print('请先安装 node.js: https://nodejs.org/')
            sys.exit()
        sign = process.communicate()[0].decode().strip('\n').strip('\r')
        print('解析视频链接中')
        user_url_prefix = 'https://www.amemv.com/aweme/v1/aweme/favorite' if type_flag == 'f' else 'https://www.amemv.com/aweme/v1/aweme/post'
        while has_more != 0:
            user_url = user_url_prefix + '/?user_id=%s&max_cursor=%s&count=21&aid=1128&_signature=%s&dytk=%s' % (
            uid, max_cursor, sign, dytk)
            req = requests.get(user_url, headers=self.headers)
            while req.status_code != 200:
                req = requests.get(user_url, headers=self.headers)
            html = json.loads(req.text)
            for each in html['aweme_list']:
                share_desc = each['share_info']['share_desc']
                if os.name == 'nt':
                    for c in r'\/:*?"<>|':
                        nickname = nickname.replace(c, '').strip().strip('\.')
                        share_desc = share_desc.replace(c, '').strip()
                share_id = each['aweme_id']
                if share_desc in ['抖音-原创音乐短视频社区', 'TikTok']:
                    video_names.append(share_id + '.mp4')
                else:
                    video_names.append(share_id + '-' + share_desc + '.mp4')
                share_urls.append(each['share_info']['share_url'])
                video_urls.append(each['video']['play_addr']['url_list'][0])
            max_cursor = html['max_cursor']
            has_more = html['has_more']

        return video_names, video_urls, share_urls, nickname

    def get_download_url(self, video_url, watermark_flag):
        """
        获得带水印的视频播放地址
        Parameters:
            video_url：带水印的视频播放地址
        Returns:
            download_url: 带水印的视频下载地址
        """
        # 带水印视频
        if watermark_flag == True:
            download_url = video_url
        # 无水印视频
        else:
            download_url = video_url.replace('playwm', 'play')

        return download_url

    def video_downloader(self, video_url, video_name, watermark_flag=False):
        """
        视频下载
        Parameters:
            video_url: 带水印的视频地址
            video_name: 视频名
            watermark_flag: 是否下载带水印的视频
        Returns:
            无
        """
        size = 0
        video_url = self.get_download_url(video_url, watermark_flag=watermark_flag)
        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))

                with open(video_name, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()

                        sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                        sys.stdout.flush()

    def run(self):
        """
        运行函数
        Parameters:
            None
        Returns:
            None
        """
        self.hello()

        user_id = input('请输入ID (例如 792279162 或 Empty_1996 或 95006183 ):')
        user_id = user_id if user_id else '95006183'

        watermark_flag = input('是否下载带水印的视频 ( 0-否-默认, 1-是 ):')
        watermark_flag = watermark_flag if watermark_flag != '' else '0'
        watermark_flag = bool(int(watermark_flag))

        type_flag = input('f-收藏的-默认, p-上传的:')
        type_flag = type_flag if type_flag != '' else 'f'

        save_dir = input('保存路径 ( 例如"E:/Download/", 默认"./Download/"):')
        save_dir = save_dir if save_dir else "./Download/"

        video_names, video_urls, share_urls, nickname = self.get_video_urls(user_id, type_flag)
        nickname_dir = os.path.join(save_dir, nickname)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if nickname not in os.listdir(save_dir):
            os.mkdir(nickname_dir)

        if type_flag == 'f':
            if 'favorite' not in os.listdir(nickname_dir):
                os.mkdir(os.path.join(nickname_dir, 'favorite'))

        print('视频下载中:共有%d个作品!\n' % len(video_urls))
        for num in range(len(video_urls)):
            print('  解析第%d个视频链接 [%s] 中，请稍后!\n' % (num + 1, share_urls[num]))
            if '\\' in video_names[num]:
                video_name = video_names[num].replace('\\', '')
            elif '/' in video_names[num]:
                video_name = video_names[num].replace('/', '')
            else:
                video_name = video_names[num]
            video_path = os.path.join(nickname_dir, video_name) if type_flag != 'f' else os.path.join(nickname_dir,
                                                                                                      'favorite',
                                                                                                      video_name)
            print(video_path)

            if os.path.isfile(video_path):
                print('视频已存在')
            else:
                self.video_downloader(video_urls[num], video_path, watermark_flag)
            print('\n')
        print('下载完成!')

    def hello(self):
        """
        打印欢迎界面
        Parameters:
            None
        Returns:
            None
        """
        print('*' * 100)
        print('\t\t\t\t抖音App视频下载小助手')
        print('\t\t作者:Jack Cui、steven7851')
        print('*' * 100)


if __name__ == '__main__':
    douyin = DouYin()
    douyin.run()