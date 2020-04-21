import requests
import re
import random
import time
class DownPic():

    def __init__(self, stop_page,theme , start_page = 1):
        self.path = 'D://pic/'
        self.url = None
        self.start_page = start_page
        self.stop_page = stop_page + 1
        self.num = start_page             #当前页面信息
        self.download_url = None
        self.params = {
            'callback':'handleResponse',
            'type' : '10',
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

            'Connection': 'keep-alive',
            'cookie' : ' ',     #在页面中查找你的cookie
            'User-Agent': '',#在页面中查找ua
            'pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Host': '588ku.com'
        }
        self.response = None
        self.theme = theme
        self.picid = None#记录图片picid的列表

    def get_response(self):
        '''
        获取起始页面
        :return: self.respongse = respongs
        '''
        response = requests.get(self.url, headers = self.headers)
        if response.status_code == 200 :
            print('\n')
            print('第{}页成功，一共有{}页开始解析图片地址'.format(self.num, self.stop_page - self.start_page))
            response.encoding = response.apparent_encoding
            self.num += 1
            # print(response.status_code)
            # print(len(response.text))
            # print(response.text)
            self.response = response

    def get_params(self, pic_num):
        '''
        构造字典，返回params
        :return:self.params = params
        '''
        self.params['picid'] = self.picid[pic_num]
        self.params['refererUrl'] = self.url
        self.params['_'] = '1587393716' + str(random.randint(100, 999))

    def get_url(self,num):
        '''
        构造页面url链接
        :return: self.url = url
        '''
        url = 'https://588ku.com/sheyingtu/{}-0-default-0-{}/'.format(str(self.theme), num)
        print(url)
        self.url = url

    def get_pic_url(self):
        '''
        获取图片下载地址url
        :return: self.download_url = url
        '''
        url = 'https://dl.588ku.com/down/pic'
        response = requests.get(url, params=self.params, headers = self.headers)
        response.encoding = response.apparent_encoding
        try:
            download_url = re.findall(r'http:.*.jpg', response.text)
            print(download_url)
            s = download_url[0]
            result = eval(repr(s).replace('\\', ''))
            # print(result)
            # response2 = requests.get(result)
            # print(response2.url)
            # print(response2.status_code)
            # with open('01.jpg', 'wb')as f:
            #     f.write(response2.content)
            self.download_url = result
        except :
            mes = re.search(r'下载限量', response.text)
            if mes != None:
                print('当前以达到下载数量限制，请稍后再试')
                time.sleep(1000)
            print('download_pic_url获取失败')

    def download_pic(self, num):
         '''
         根据提供的url下载图片到本地
         :return:
         '''
         url = self.download_url
         num = num
         download = requests.get(url)
         try:
            with open(self.path + '{}-{}.jpg'.format(self.num, num), 'wb') as f:
                f.write(download.content)
                print('第{}张图片下载成功，图片id为{}'.format(num+1, self.picid[num]))
         except:
             print('图片下载失败')

    def get_picid(self):
        '''
        从self.num页面中解析出来图片的url
        从图片的url中生成picid储存在列表中
        :return: picid_ls = ls
        '''
        i = 0
        lis = re.findall(r'\d{6}.html', self.response.text) + re.findall(r'/\d{5}.html', self.response.text)
        for url in lis:
            if url[0] == '/':
                lis[i] = url[1:6]
            else:
                lis[i] = url[0:6]
            i = i+1
        print('当前页面一共有{}张图片，开始下载'.format(len(lis)))
        print('\n')
        self.picid = lis




    def run(self, num):
        '''
        程序运行一次，下载一页的内容
        :return:
        '''
        self.get_url(num)  #获取页面url
        self.get_response()#获取页面信息
        self.get_picid()#获取当前页面picid
        pic_num = len(self.picid)
        for i in range(pic_num):
            self.get_params(i)
            self.get_pic_url()
            self.download_pic(i)

    def pages_run(self):
        '''
        多次运行，抓取多页图片
        :return:
        '''
        for num in range(self.start_page, self.stop_page):
            self.run(num)
A = DownPic(83, 'shuiguo', start_page= 65)
A.pages_run()
