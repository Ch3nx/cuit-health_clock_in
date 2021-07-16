import random
import requests
import re

def get_ua():
    ua_pools = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48'
    ]
    ua = random.choice(ua_pools)
    return ua

def get_cookie_id(username, password, user_agent):
    # 目标网址列表
    login_url = [
        'http://login.cuit.edu.cn/Login/xLogin/Login.asp',
        'http://jszx-jxpt.cuit.edu.cn/jxgl/xs/netks/sj.asp?jkdk=Y',
        'http://login.cuit.edu.cn/Login/qqLogin.asp',
        'http://jszx-jxpt.cuit.edu.cn/Jxgl/UserPub/Login.asp?UTp=Xs',
        'http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp',
        'http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/syLogin.asp',
        'http://jszx-jxpt.cuit.edu.cn/Jxgl/UserPub/Login.asp?UTp=Xs&Func=Login',
        'http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/MainMenu.asp',
        'http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/sj.asp'
    ]
    # 构造GET请求头
    get_headers_1 = {
        'Host': 'login.cuit.edu.cn',
        'User-Agent': user_agent,
        'Accept': 'image/webp,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    # 获取第一个Cookie
    r = requests.get(login_url[0], headers=get_headers_1, allow_redirects=False)
    # r.cookies返回RequestsCookieJar对象
    cookie_1 = ''
    for key, value in r.cookies.items():
        cookie_1 = '%s=%s' % (key, value)
    # 从登录界面获取动态登陆码codeKey（更新图片验证码），正则匹配后返回值为列表
    codeKey = re.findall(r"(?<=var codeKey = ').*?(?=';)", r.text)[0]
    # 构造GET请求头
    get_headers_2 = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    # 获取第二个Cookie
    r = requests.get(login_url[1], headers=get_headers_2, allow_redirects=False)
    cookie_2 = ''
    for key, value in r.cookies.items():
        cookie_2 = '%s=%s' % (key, value)
    get_headers_1['Cookie'] = cookie_1
    get_headers_2['Cookie'] = cookie_2
    # 构造POST信息
    login_data = {
        # 屏幕分辨率
        'WinW': '1920',
        'WinH': '1040',
        # 登录信息
        'txtId': username,
        'txtMM': password,
        # 现阶段暂时不需要验证码，故可以为空
        'verifycode': '',
        'codeKey': codeKey,
        'Login': 'Check',
        # 登录时鼠标点击点相对位置，范围为0~111、0~122
        'IbtnEnter.x': '18',
        'IbtnEnter.y': '18'
    }
    # 构造POST请求头
    post_headers = {
        'Host': 'login.cuit.edu.cn',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '152',
        'Origin': 'http://login.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Referer': 'http://login.cuit.edu.cn/Login/xLogin/Login.asp',
        'Cookie': cookie_1,
        'Upgrade-Insecure-Requests': '1'
    }
    # 实现模拟登录
    r = requests.post(login_url[0], headers=post_headers, data=login_data, allow_redirects=False)
    r = requests.get(login_url[2], headers=get_headers_1, allow_redirects=False)
    r = requests.get(login_url[3], headers=get_headers_2, allow_redirects=False)
    r = requests.get(login_url[4], headers=get_headers_2, allow_redirects=False)
    trs_url = re.findall(r"(?<=;URL=).*?(?=\">)", r.text)[0]
    r = requests.get(trs_url, headers=get_headers_1, allow_redirects=False)
    for i in range(4, 9):
        r = requests.get(login_url[i], headers=get_headers_2, allow_redirects=False)
    # 获取第三个Cookie
    cookie_3 = ''
    for key, value in r.cookies.items():
        cookie_3 = '%s=%s' % (key, value) + '; ' + cookie_2
    id = re.findall(r'(?<=&Id=).*?(?=target=_self>)', r.text)[0]
    return cookie_3, id

def simu_clock(cookie, id, username, user_agent):
    sub_info = {
        'RsNum': '3',
        'Id': id,
        'Tx': '33_1',
        'canTj': '1',
        'isNeedAns': '0',
        'UTp': 'Xs',
        'ObjId': username,
        # 个人健康现状
        'th_1': '21650',
        'wtOR_1': '1\|/'+ data['省'] + '\|/' + data['市'] + '\|/' + data['区（县）'] + '\|/1\|/1\|/1\|/1\|/1\|/',
        'sF21650_1': '1',
        'sF21650_2': data['省'].encode('gb2312'),
        'sF21650_3': data['市'].encode('gb2312'),
        'sF21650_4': data['区（县）'].encode('gb2312'),
        'sF21650_5': '1',
        'sF21650_6': '1',
        'sF21650_7': '1',
        'sF21650_8': '1',
        'sF21650_9': '1',
        'sF21650_10': '',
        'sF21650_N': '10',
        # 进出学校报备
        'th_2': '21912',
        # 模式说明：默认今天6点离校，当天23点前返校
        # 1/2/3：今天/明天/后天
        # 06~22：离校时间
        # 1/2/3/9：当天/第2天/第3天/当晚（离校）
        # 07~23：返校时间
        'wtOR_2': data['目的地'] + '\|/' + data['事由'] +'\|/1\|/06\|/1\|/23',
        'sF21912_1': data['目的地'].encode('gb2312'),
        'sF21912_2': data['事由'].encode('gb2312'),
        'sF21912_3': '1',
        'sF21912_4': '06',
        'sF21912_5': '1',
        'sF21912_6': '23',
        'sF21912_N': '6',
        # 最近14天以来的情况
        'th_3': '21648',
        'wtOR_3': 'N\|/\|/N\|/\|/N\|/',
        'sF21648_1': 'N',
        'sF21648_2': '',
        'sF21648_3': 'N',
        'sF21648_4': '',
        'sF21648_5': 'N',
        'sF21648_6': '',
        'sF21648_N': '6',
        'zw1': '',
        'cxStYt': 'A',
        'zw2': '',
        'B2': '提交打卡'.encode('gb2312')
    }
    url = [
        'http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/sjDb.asp?UTp=Xs&jkdk=Y',
        'http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/editSjRs.asp'
    ]
    url_1 = url[0] + '&ObjId=' + username + '&Id=' + id
    url_2 = url[1] + '?UTp=Xs&Tx=33_1&ObjId=' + username + '&Id=' + id
    get_headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/sj.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cookie': cookie
    }
    post_headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://jszx-jxpt.cuit.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': url_2,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cookie': cookie
    }
    r = requests.get(url_1, headers=get_headers, allow_redirects=False)
    r = requests.get(url_2, headers=get_headers, allow_redirects=False)
    r = requests.post(url[1], headers=post_headers, data=sub_info)
    # 编码格式改为从响应体中分析出的编码格式
    r.encoding = r.apparent_encoding
    state = re.findall(r'(?<=alert\(").*?(?="\);)', r.text)[0]
    print(state)

if __name__ == "__main__":
    # username = '帐号'
    # password = '密码'
    username = input("请输入学号：")
    password = input("请输入密码：")
    data = {
        # 离校、返校时间设置具体见sub_info
        '省': '四川',
        '市': '成都',
        '区（县）': '双流区',
        '目的地': '春熙路方所书店',
        '事由': '会友'
    }
    cookie, id = get_cookie_id(username, password, get_ua())
    simu_clock(cookie, id, username, get_ua())
