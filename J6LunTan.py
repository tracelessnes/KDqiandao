# -*- coding: utf-8 -*-
"""
cron: 21 6 * * *
new Env('96论坛');
"""

import requests, sys, re, traceback
from io import StringIO
from bs4 import BeautifulSoup
from KDconfig import getYmlConfig, send

class J6LunTan:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''
    def getcookie(self):
        if self.cookie == "":
            print("请配置Cookie再试试")
            self.sio.write("请配置Cookie再试试\n")
            return
        
        headers = {
            'cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/114.0.0.0'
        }
        session = requests.session()
        url_page = 'https://www.steamcom.cn/'
        rep = session.get(url=url_page, headers=headers)
        #print(rep,rep.text)
        url = 'https://www.steamcom.cn/home.php?mod=spacecp&ac=credit&op=base'
        rep = session.get(url=url, headers=headers)
        self.getJB()

    def getJB(self):
        session = requests.session()
        headers = {
            'cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/114.0.0.0'
        }        

        url = 'https://www.steamcom.cn/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu'
        headers = {
            "Referer": "www.znbbs.vip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Cookie": self.cookie
        }
        res = session.get(url=url,headers=headers)
        
        print(res.text)
        jf = re.findall('金币: <span id="hcredit_1">(.*)</span></li><li> 积分', res.text)[0]
        print(f'剩余{jf}')
        jq = re.findall('积分: <span id="hcredit_2">(.*)</span></li></ul>', res.text)[0]
        print(f'剩余{jq}')
        self.sio.write(f', 剩余金币{jq} 剩余积分{jf}\n')

    def SignIn(self):
        print("【96论坛 日志】")
        self.sio.write("【96论坛】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            self.cookie = cookie.get("cookie")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            try:
                self.getcookie()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}\n")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('J6LunTan')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            J6LunTan = J6LunTan(Cookies['cookies'])
            sio = J6LunTan.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('96论坛', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 96论坛 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 96论坛')
        
        
        
        