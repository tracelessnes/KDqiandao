# -*- coding: utf-8 -*-
"""
cron: 21 6 * * *
new Env('真牛论坛');
"""

import requests, sys, re, traceback
from io import StringIO
from bs4 import BeautifulSoup
from KDconfig import getYmlConfig, send

class ZhenNiu:
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0'
        }
        session = requests.session()
        url_page = 'https://www.znbbs.vip/'
        rep = session.get(url=url_page, headers=headers)
        formhash=re.findall(r'formhash=(.*)">退出', rep.text)
        if len(formhash) == 0:
            formhash = ['e20152d1']  # 如果没有获取到formhash则默认设置为 '9658ce31'
            print("未获取到formhash,尝试使用默认formhash")
        print("formhash", formhash[0])

        url = 'https://www.znbbs.vip/plugin.php?id=tshuz_sign&mod=sign&formhash=' + formhash[0]
        rep = session.get(url=url, headers=headers)
        match = re.search(r'<div\s+id="messagetext"\s+class="[a-zA-Z]{5}_[a-zA-Z]{5}">\s*<p>(.*?)</p>', rep.text, flags=re.DOTALL)
        if match:
            result = match.group(1)
            print(result)
        else:
            print('未找到目标文本')        
        #print(rep,rep.text)
        url = 'https://www.znbbs.vip/plugin.php?id=tshuz_sign'
        rep = session.get(url=url, headers=headers)

        #print(rep,rep.text)        
        soup = BeautifulSoup(rep.text, 'html.parser')         
        # 提取连续打卡天数
        continuous_days = soup.find('div', {'class': 'tshuz_sign_main wp'}).find_all('span')[1].get_text(strip=True)

        # 提取总打卡天数
        total_days = soup.find('div', {'class': 'tshuz_sign_main wp'}).find_all('span')[4].get_text(strip=True)

        # 提取打卡总奖励
        total_rewards = soup.find('div', {'class': 'tshuz_sign_main wp'}).find_all('span')[7].get_text(strip=True)
        print(f"连续打卡 {continuous_days} 天 |总打卡 {total_days} 天 | 打卡总奖励 {total_rewards} 牛币")
        result = f"连续打卡 {continuous_days} 天 |总打卡 {total_days} 天 | 打卡总奖励 {total_rewards} 牛币\n"
       
        self.sio.write('\n' + result)
        self.getJB()

    def getJB(self):
        session = requests.session()
        headers = {
            'cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/114.0.0.0'
        }        

        url = 'https://www.znbbs.vip/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu'
        headers = {
            "Referer": "www.znbbs.vip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Cookie": self.cookie
        }
        res = session.get(url=url,headers=headers)
        
        print(res.text)
        jf = re.findall('牛币: <span id="hcredit_2">(.*)</span></li><li> 贡献', res.text)[0]
        print(f'剩余{jf}')
        jq = re.findall('贡献: <span id="hcredit_3">(.*)</span></li><li> 银元', res.text)[0]
        print(f'剩余{jq}')
        self.sio.write(f', 剩余牛币{jq} 剩余贡献{jf}\n')

    def SignIn(self):
        print("【真牛论坛 日志】")
        self.sio.write("【真牛论坛】\n")
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
    Cookies = config.get('ZhenNiu')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            ZhenNiu = ZhenNiu(Cookies['cookies'])
            sio = ZhenNiu.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                pass
                #send('真牛论坛', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 真牛论坛 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 真牛论坛')
        
        
        
        