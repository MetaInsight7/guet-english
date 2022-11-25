#!/user/bin/env python
# -*- coding:utf-8 -*-
# Copyright：MetaInsight

import requests
from lxml import etree
import time

def login_web(user,password):
    print("\n正在执行登陆...")
    time.sleep(2)
    url = "https://zhihui.guet.edu.cn/Default.aspx"
    data = {
        "txtUserName":user,
        "txtPassword":password,
        "loginend":"登录",
    }
    r = session.post(url,data=data)
    tree = etree.HTML(r.text)
    result = tree.xpath("/html/head/title//text()")[0]
    if result == "学生信息管理系统":
        print("登录成功！\n")
        print("开始获取cookie和userid")
        cookie_dict = requests.utils.dict_from_cookiejar(session.cookies)
        cookie = cookie_dict['ASP.NET_SessionId']
        userid = cookie_dict['T_Stu'][-5:]
        print("cookie：" + cookie)
        print("userid：" + userid)
        return userid
    else:
        userid = 0
        print("登录失败！")
        return userid

    
def get_info():
    print("\n正在获取用户信息...")
    time.sleep(2)
    url = "https://zhihui.guet.edu.cn/stu/user/zonghe.aspx"
    r = session.get(url)
    tree = etree.HTML(r.text)
    s_name = tree.xpath("normalize-space(//tr[1]/td[2]/text())")
    s_num = tree.xpath("normalize-space(//tr[1]/td[4]/text())")
    s_onlinetime = tree.xpath("normalize-space(//tr[6]/td[2]/text())")
    s_logintime = tree.xpath("normalize-space(//tr[6]/td[4]/text())")
    s_reviewtime = tree.xpath("normalize-space(//tr[4]/td[4]/text())")
    print("姓名：{}\n学号：{}\n在线学习时长：{}\n在线复习时长：{}\n登陆次数：{}\n".format(s_name,s_num,s_onlinetime,s_reviewtime,s_logintime))
    return s_name,s_num,s_onlinetime,s_logintime,s_reviewtime




def skip_study(user,userid,skip_online_hour,skip_review_hour):
    print("正在开始刷时长...")
    
    # 刷完成度
    for i in range(2000,2400):
            url_pass = "https://zhihui.guet.edu.cn/stu/webuc/liulja.aspx?uid={}&nid={}".format(userid,i)
            session.get(url_pass)
    
    # 刷在线学习时长
    print("刷在线时长共需{}轮".format(2*skip_online_hour))
    epoch_online = 0
    while epoch_online < 2*skip_online_hour:
        for i in range(2000,2400):
            url_online = "https://zhihui.guet.edu.cn/stu/webuc/lookjx.aspx?jxid={}&u={}&tcid=318&name={}&zjs={}".format(i,userid,user,i)
            session.get(url_online)
        epoch_online += 1
        print("第{}轮结束！".format(epoch_online))
    
    # 刷在线复习时长
    print("刷复习时长共需{}轮".format(3*skip_review_hour))
    epoch_review = 0
    while epoch_review < 3*skip_review_hour:
        for i in range(2000,2400):
            url_review = "https://zhihui.guet.edu.cn/stu/user/Style/liul.aspx?uid={}&nid=endtime".format(userid)
            session.get(url_review)
        epoch_review += 1
        print("第{}轮结束！".format(epoch_review))
    
    print("程序运行结束！！")

    
    
print("-------科研小助手 v1.0-------")
print("自动挂英语平台学习时长，把更多的时间留给科研")
print("仅适用于读写平台，听说貌似没有时长要求")
print("Bug反馈地址：https://docs.qq.com/form/page/DRkZCV3JUandRaFlu")
print("-------Copyright@数学与计算科学学院：MetaInsight--------\n")
time.sleep(3)
while True:
    user = input("请输入读写平台账号：")
    password = input("请输入密码：")
    session = requests.session()
    userid= login_web(user,password)
    if userid ==0:
        print("请检查账号密码！\n")
    else:
        break
        
        
while True:
    get_info()
    print("\n请注意区分在线时长和复习时长！！！！")
    skip_online_hour = input("请输入需要刷的在线时长，以小时为单位，最大值为30小时：")
    skip_review_hour = input("请输入需要刷的复习时长，以小时为单位，最大值为30小时：")
    try:
        skip_online_hour = int(skip_online_hour)
        skip_review_hour = int(skip_review_hour)

        if skip_online_hour > 30 or skip_review_hour > 30:
            print("请输入0-30之间的整数！！")
        else:
            skip_study(user,userid,skip_online_hour,skip_review_hour)
            get_info()
            input('按 Enter 退出…')
            break
    except:
        print("请输入0-30之间的整数！！") 