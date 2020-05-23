import requests,time,random,os
from urllib import parse
from lxml import etree



class TieBa:
    def __init__(self):
        self.url = 'https://tieba.baidu.com/f?kw={}&pn={}'
        self.headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        self.name = input('输入贴吧名字:')
        self.directory = '/home/tarena/images/{}/'.format(self.name)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.i = 1

    def get_html(self,url):
        for i in range(3):
            try:
                html = requests.get(url=url,headers=self.headers,timeout=3).text
                return html
            except Exception as e:
                print('Retry')

    def parse_html(self,url):

        p = etree.HTML(self.get_html(url))

        li_list = p.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        for li in li_list:
            url = 'https://tieba.baidu.com' + li if li else None
            two_html = self.get_html(url)
            t = etree.HTML(two_html)
            li_img_list = t.xpath('//div/img[@class="BDE_Image"]/@src| //div[@class="video_src_wrapper"]/embed/@data-video')
            self.save_img_html(li_img_list)

    def save_img_html(self,li_img_list):
        for li in li_img_list:

            html = requests.get(url=li,headers=self.headers).content if li else None
            filename = self.directory + self.name + '_' + str(self.i) + '.' + li.split('.')[-1]
            with open(filename,'wb') as f:
                f.write(html)
            self.i+=1
            print(filename,'抓取完成')


    def run(self):
        params = parse.quote(self.name)
        s_page = int(input('起始页:'))
        e_page = int(input('结束页:'))
        for i in range(s_page,e_page+1):
            pg = (i-1) * 50
            url = self.url.format(params,pg)
            self.get_html(url)
            self.parse_html(url)
            time.sleep(random.uniform(0,1))

if __name__ == '__main__':
    spider = TieBa()
    spider.run()