# -*- coding: utf-8 -*-
"""
cron: 21 6 * * *
new Env('精易论坛');
"""

import requests, sys, re, traceback,time
from io import StringIO
from bs4 import BeautifulSoup
from KDconfig import getYmlConfig, send

class JingYi:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def task(self):
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, {item.split("=")[0]: item.split("=")[1] for item in self.cookie.split("; ")})
        session.headers.update({"Referer": "https://bbs.125.la/plugin.php?id=dsu_paulsign:sign"})
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"})
        res = session.get(url="https://bbs.125.la/plugin.php?id=dsu_paulsign:sign")
        while 'antiCC_' in res.text:
            print("Resigning because of antiCC_...")
            self.getcookie()
            time.sleep(2)
        formhash=re.findall(r'formhash=(.*)">退出', res.text)
        if len(formhash) == 0:
            formhash = ['9658ce31']  # 如果没有获取到formhash则默认设置为 '9658ce31'
        print("formhash", formhash[0])        
        url_page ='https://bbs.125.la/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1'
        data = {'formhash':formhash[0],"submit": "1","targerurl": "","todaysay": "","qdxq": "kx"}
        res = session.post(url=url_page, data=data)
        print(res.text)
        print("签到结果:"+re.findall(r'{"status":0,"msg":"(.*)"}', res.text)[0])
        self.sio.write("签到结果:"+re.findall(r'{"status":0,"msg":"(.*)"}', res.text)[0])
        self.getJB()

    
    def getcookie(self):
        if self.cookie == "":
            print("请配置Cookie再试试")
            self.sio.write("请配置Cookie再试试\n")
            return
        
        headers = {
            'cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
        }
        session = requests.session()
        url_page = 'https://bbs.125.la/plugin.php?id=dsu_paulsign:sign&inajax=1'
        rep = session.get(url=url_page, headers=headers)
        print(rep.text)
        pattern = r'(antiCC_[0-9]+)'
        match = re.search(pattern, rep.text)
        if match:
            result = match.group(1)
            self.cookie += '; __ancc_tokenV2=' + result
            print(self.cookie)
            self.task()
        else:
            print("未能匹配到内容antiCC_")
            self.sio.write("未能匹配到内容antiCC_或cookie失效")
        
    
    
    
    def getJB(self):
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, {item.split("=")[0]: item.split("=")[1] for item in self.cookie.split("; ")})
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"})
        url = 'https://bbs.125.la/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu'
        res = session.get(url=url)
        
        print(res.text)
        jb = re.findall('精币: <span id="hcredit_4">(.*)</span></li><li> 荣誉', res.text)[0]
        print(f'剩余{jb}')
        self.sio.write(f', 剩余{jb}\n')

    def SignIn(self):
        print("精易论坛 日志】")
        self.sio.write("【精易论坛】\n")
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
    Cookies = config.get('JingYi')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            JingYi = JingYi(Cookies['cookies'])
            sio = JingYi.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('精易论坛', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 精易论坛 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 精易论坛')
        
        
        
        