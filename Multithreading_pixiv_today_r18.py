import re
import requests
import datetime
import os ,json
from threading import Thread




class today_r18:
    def __init__(self):
        proxies = json.load(open('name.json', mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.run()

    def headers(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "referer": "https://www.pixiv.net/ranking.php?mode=daily_r18",
            "cookie": json.load(open('name.json', mode='r')).get('cookie'),
        }
        return headers


    def request_2(self,url):
        try:
            global d
            response = requests.get('https://www.pixiv.net' + url,proxies=self.proxies)
            name = re.search(r'"title":"(.*?)"', response.text).group(1)
            name = name.strip('?').replace('\*', '').replace('<', '_').replace('>', '_').replace('"', '_').replace(':',
                                                                                                                   '_')
            name = name.replace('.', '').replace('\\', '').replace('|', '_')
            name = name.replace('\u0027', '_').replace('\u3000', '_')
            img_url = re.findall(r'"original":"(.*?)"},', response.text, re.S)
            for it in img_url:
                resp = requests.get(it, headers=self.headers(),proxies=self.proxies)
                if not os.path.exists(path + name + it[-3:]):
                    with open(path + '%s.%s' % (name.replace(r'/', '_'), it[-3:]), mode='wb') as f:
                        f.write(resp.content)
                else:
                    with open(path + '%s(%s).%s' % (name.replace(r'/', '_'), str(d), it[-3:]), mode='wb') as f:
                        f.write(resp.content)
                        d += 1
        except OSError as a:
            print('\033[2;32m{}\033[0m'.format(str(a)))

    def request_1(self):
        try:
            global d
            list = []
            for i in range(1,2 + 1):
                url = 'https://www.pixiv.net/ranking.php?mode=daily_r18&p=%d' % i
                resp = requests.get(url, headers=self.headers(),proxies=self.proxies)
                resp.encoding = 'utf-8'
                title_url = re.findall(r'<h2>.*?<a href="(.*?)"', resp.text)
                print('\033[2;32m???????????????????????????????????????\033[0m')
                for i in title_url:
                    if i is not None:
                        list.append(i)
                    else:
                        list.append(i)
                        print('??????url????????????')
                        break
            print('????????????,????????????')
            print('??? %d ?????????'.center(20, '-') % len(list))
            for d in (1, len(list)):
                ts = [Thread(target=self.request_2, args=(i,)) for i in list]
                for it in ts:
                    it.start()
                for it in ts:
                    it.join()
            print('??????????????????????????????')
        except requests.exceptions.ChunkedEncodingError:
            print('\033[2;32m??????????????????,???????????????????????????\033[0m')

    def run(self):
        global path
        with open('name.json', mode='r', encoding='UTF-8') as f:
            path = json.load(f).get('dirs').get('r18_Today_date')
            path = (path + '%s/' % datetime.date.today())
        if os.path.exists(path) is False:
            os.mkdir(path)
            print('??????????????????,????????????\n?????????:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
            os.system('start {}'.format(path))
            self.request_1()
        else:
            print('?????????????????????,????????????\n?????????:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
            os.system('start {}'.format(path))
            self.request_1()

if __name__=='__main__':
    # ????????????????????????????????? run ??????
    pixiv = today_r18()