#! /usr/bin/python2
# -*- coding: utf-8-*-
from Tkinter import *
import tkMessageBox
import urllib2
import urllib
import json
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#setting
class Setting_window:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.geometry('260x110')  
        input_frm = Frame(top)
        self.bkn_lab = Label(input_frm, text='bkn:', font=('Arial', 15)).grid(row=0)
        self.cookie_lab = Label(input_frm, text='cookie:', font=('Arial', 15)).grid(row=1)
        self.bkn_ipt = StringVar()
        self.e_bkn = Entry(input_frm, textvariable = self.bkn_ipt)
        self.cookie_ipt = StringVar()
        self.e_cookie = Entry(input_frm, textvariable = self.cookie_ipt)
        self.e_bkn.grid(row=0, column=1)
        self.e_cookie.grid(row=1, column=1)
        input_frm.pack()

        self.save = Button(top, text='save', command=self.save)
        self.save.pack()
        if os.path.exists('biuflower.json'):
            with open("biuflower.json","r") as cfg:
                cfg_json = json.loads(cfg.read())
                cookie_dic["cookie"] = cfg_json["cookie"]
                cookie_dic['bkn'] = cfg_json['bkn']
            self.e_bkn.insert(0,cookie_dic['bkn'])
            self.e_cookie.insert(0,cookie_dic['cookie'])
    def save(self):
        cookie_dic["cookie"] = self.e_cookie.get()
        cookie_dic["bkn"] = self.e_bkn.get()
        with open("biuflower.json",'w') as cfg:
            cfg_json = json.dumps(cookie_dic)
            cfg.write(cfg_json)
        tkMessageBox.showinfo("设置", "设置已保存")
        self.top.destroy()
def set_win():
    inputDialog = Setting_window(root)
    root.wait_window(inputDialog.top)
def biu():
    if not os.path.exists('biuflower.json'):
        tkMessageBox.showinfo("biu", "先设置bkn和cookie再继续")
        return
    gc = gc_ipt.get()
    if not gc:
        tkMessageBox.showinfo("biu", "先填好gc才能继续")
        return
    if not poi_listbox.curselection():
        tkMessageBox.showinfo("biu", "选一个地点来biu")
        return
    biu_dat = sign(cookie_dic["cookie"],cookie_dic['bkn'],gc,poi_dat["info"][poi_listbox.curselection()[0]])
    biu_dic = json.loads(biu_dat)
    if biu_dic["ec"] == 0:
        tkMessageBox.showinfo("biu", "快去看看成功了没！")
    elif biu_dic["ec"] == 1:
        tkMessageBox.showinfo("biu", "cookie过期了。重新抓包吧")
    else:
        tkMessageBox.showinfo("biu", "出错啦。检查看看有没有什么地方填错了")


def btn_get_poi():
    if not os.path.exists('biuflower.json'):
        tkMessageBox.showinfo("poi", "先设置bkn和cookie再继续")
        return
    gc = gc_ipt.get()
    if not gc:
        tkMessageBox.showinfo("poi", "先填好gc才能继续")
        return
    lat = lat_ipt.get()
    if not lat:
        tkMessageBox.showinfo("poi", "先填好lat才能继续")
        return
    lgt = lgt_ipt.get()
    if not lgt:
        tkMessageBox.showinfo("poi", "先填好lgt才能继续")
        return
    with open("biuflower.json","r") as cfg:
            cfg_json = json.loads(cfg.read())
            cookie_dic["cookie"] = cfg_json["cookie"]
            cookie_dic['bkn'] = cfg_json['bkn']
    global poi_dat
    poi_dat = get_poi(cookie_dic["cookie"],gc,lat,lgt,10)
    if poi_dat["ec"] == 0:
        pass
    elif poi_dat["ec"] == 1:
        tkMessageBox.showinfo("poi", "cookie过期了。重新抓包吧")
        return
    else:
        tkMessageBox.showinfo("poi", "出错啦。检查看看有没有什么地方填错了")
        return
    poi_listbox.delete(0,last=END)
    for place in poi_dat["info"]:
        poi_listbox.insert(END,place["name"].replace("&nbsp;",' ').replace("&amp;",'&'))
        print poi_dat["info"].index(place),place["name"].replace("&nbsp;",' ').replace("&amp;",'&'),place["lat"],place["lgt"],place["seckey"]

def send_get(req):
    '''Send get resquest
    '''
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req) 
    try:
        return response.read()
    except Exception, e:
        print u'发生了一个错误: %s' % e
    

def send_post(req,data):  
    '''Send post resquest
    '''
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    response = opener.open(req, data) 
    try:
        return response.read()
    except Exception, e:
        print u'发生了一个错误: %s' % e

def get_poi(cookie,gc,lat,lgt,n):
    get_url = 'http://qiandao.qun.qq.com/cgi-bin/get_lbs_location?'
    get_params = {
                    "lat" : lat,
                    "lgt" : lgt,
                    "s" : 1,
                    "n" : n,
                    "gpstype" : 1,
                    "gc" : gc,
                    "keywords" : "综合商场|商业步行街|娱乐休闲|运动健身|旅游景点|文化场馆|教育学校|住宅区|产业园区|商务楼宇"
                }
    get_url = get_url+urllib.urlencode(get_params)
    get_req = urllib2.Request(get_url)
    req_dic = {
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'http://qiandao.qun.qq.com/qqweb/m/qun/checkin/index.html',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.0.2; zh-cn; Nexus 7 Build/LRX22G) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025442 Mobile Safari/533.1 V1_AND_SQ_5.7.2_260_YYB_D QQ/5.7.2.2490 NetType/WIFI WebP/0.3.0',
                'Accept-Language': 'zh-CN',
                'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.7',
                'Host': 'qiandao.qun.qq.com',
                'Cookie': cookie
                }
    for key in req_dic:
        get_req.add_header(key,req_dic[key])
    poi = send_get(get_req)
    poi_dat = json.loads(poi)
    return poi_dat

def sign(cookie,bkn,gc,place):
    post_url = 'http://qiandao.qun.qq.com/cgi-bin/sign'
    post_req = urllib2.Request(post_url)
    req_dic = {
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'http://qiandao.qun.qq.com/qqweb/m/qun/checkin/index.html',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.0.2; zh-cn; Nexus 7 Build/LRX22G) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025442 Mobile Safari/533.1 V1_AND_SQ_5.7.2_260_YYB_D QQ/5.7.2.2490 NetType/WIFI WebP/0.3.0',
                'Accept-Language': 'zh-CN',
                'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.7',
                'Host': 'qiandao.qun.qq.com',
                'Cookie': cookie
                }
    for key in req_dic:
        post_req.add_header(key,req_dic[key])
    post_dat_dic = {
                    "gc" : gc,
                    "is_sign" : 0,
                    "from" : 1,
                    "bkn" : bkn,
                    "poi" : place["city"] + ' · ' + place["name"].replace("&nbsp;",' ').replace("&amp;",'&'),
                    "lat" : place["lat"],
                    "lgt" : place["lgt"],
                    "seckey" : place["seckey"]
    }
    post_dat = urllib.urlencode(post_dat_dic)
    print post_dat
    sign_dat = send_post(post_req,post_dat)
    print sign_dat
    return sign_dat

# begin of GUI part
root = Tk()
root.title("flower++")
root.geometry('420x155')                 #是x 不是*
root.resizable(width=False, height=False) #宽不可变, 高可变,默认为True
frm_main = Frame(root)
frm = Frame(frm_main)

frm_gc = Frame(frm)
Label(frm_gc, text='gc:', font=('Arial', 15)).grid(row=0)
gc_ipt = StringVar()
e_gc = Entry(frm_gc, textvariable = gc_ipt)
e_gc.grid(row=0, column=1)
frm_gc.grid(row=0)

#lat,lgt
frm_lat = Frame(frm)
Label(frm_lat, text='lat:', font=('Arial', 15)).grid(row=0)
lat_ipt = StringVar()
e_lat = Entry(frm_lat, textvariable = lat_ipt)
e_lat.grid(row=0,column=1)

frm_lgt = Frame(frm)
Label(frm_lgt, text='lgt:', font=('Arial', 15)).grid(row=0)
lgt_ipt = StringVar()
e_lgt = Entry(frm_lgt, textvariable = lgt_ipt)
e_lgt.grid(row=0,column=1)

frm_lat.grid(row=1, column=0)
frm_lgt.grid(row=2, column=0)

#listbox
frm_li = Frame(frm_main)
poi_var = StringVar()
poi_listbox = Listbox(frm_li,height=5, selectmode=BROWSE,listvariable = poi_var)



scrl = Scrollbar(frm_li)
scrl.pack(side=RIGHT, fill=Y)
poi_listbox.configure(yscrollcommand = scrl.set)
poi_listbox.pack(side=LEFT, fill=BOTH)
scrl['command'] = poi_listbox.yview
frm_li.grid(row=0, column=1)

#Button
frm_btn = Frame(root)
Button(frm_btn, text="set", command=set_win, width=10, height=1, font=('Arial', 10)).grid(row=0, column=0)
Button(frm_btn, text="get", command=btn_get_poi, width=10, height=1, font=('Arial', 10)).grid(row=0, column=1)
Button(frm_btn, text="biu", command=biu, width=10, height=1, font=('Arial', 10)).grid(row=0, column=2)
# frm_btn.grid(row = 1)

frm.grid(row=0,column=0)
frm_main.pack()
frm_btn.pack()
cookie_dic = {}
root.mainloop()
