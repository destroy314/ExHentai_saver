from html.parser import HTMLParser
from tkinter.filedialog import *
from tkinter import *
import urllib.request
import requests
import time
import re
import os

root = Tk()
root.title("ExHentai")

headers = {
    'User-Agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    'Cookie':
    ""
}
url = StringVar()
nexturl = StringVar()
name = StringVar()
name.set("未知")
number = StringVar()
number.set("未知")
address = StringVar()
address.set("选择位置")
imgpath = StringVar()
imgname = StringVar()
imgurl=StringVar()
originalimgurl=StringVar()
realoriginalimgurl=StringVar()


def gethtml(url):#获取网页源码
    html_parser = HTMLParser()
    request = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(request)
    originalhtml = page.read().decode('utf-8')
    html = html_parser.unescape(originalhtml)#将html编码的字符转换为原字符
    return html


def getname(html):#获取图集名称
    reg = r'<h1 id="gj">([^>]+)</h1>'
    namere = re.compile(reg)
    name.set("".join(re.findall(namere, html)))
    if name.get() == "":#如果没有原名
        reg = r'<h1 id="gn">([^>]+)</h1>'
        namere = re.compile(reg)
        name.set("".join(re.findall(namere, html)))

def getnumber(html):#获取图片张数
    reg = r'<td class="gdt2">([0-9]+) pages</td>'
    numberre = re.compile(reg)
    number.set(re.findall(numberre, html))


def inquire():#查询图集信息
    html = gethtml(url.get())
    getname(html)
    getnumber(html)


def getaddress():
    address.set(askdirectory())



def downloadall(html):#下载所有图片
    judgmenturl = str(url.get())
    reg = r'exhentai.org/s/'#检查地址是图集还是图片
    galleryre = re.compile(reg)
    judgment = "".join(re.findall(galleryre,judgmenturl))
    if judgment == "":
        imgpath.set(address.get()+"/"+name.get())
        path = str(imgpath.get())
        os.makedirs(path)
        reg = r'<a href="([^>]+)"><img alt="0*1"'#匹配首张图片的链接
        firstre = re.compile(reg)
        url.set("".join(re.findall(firstre,html)))
    else:
        imgpath.set(address.get())
        path = str(imgpath.get())

    while 1:#无限循环下载图片

        html = gethtml(url.get())

        reg = r'<div>([^>]+\.(?:jpg|png))'#匹配图片名称
        imgnamere = re.compile(reg)
        imglist = re.findall(imgnamere,html)
        imgname.set("".join(imglist[0]))#设定图片名称

        reg = r'<img id="img" src="(.+)" style="'#匹配图片地址
        imgurlre = re.compile(reg)
        imgurl.set("".join(re.findall(imgurlre,html)))#设定图片地址

        reg = r'<a href="([^>]+)">Download'#匹配原图地址
        originalimgurlre = re.compile(reg)
        originalimgurl.set("".join(re.findall(originalimgurlre,html)))#设定原图地址
        
        if originalimgurl.get() == "":#没原图就直接下，有原图就下原图
            imgsave(imgurl.get(),imgname.get())
        else:
            originalimgsave(originalimgurl.get(),imgname.get())
        
        reg = r'<a id="next" onclick="return load_image.[0-9]{1,4}.{15}" href="([^>]+)">'#匹配下一页链接
        urlre = re.compile(reg)
        urllist = re.findall(urlre,html)
        nexturl.set("".join(urllist[0]))#设定链接

        if url.get() == nexturl.get():#与当前页链接比对
            over = Toplevel()
            over.resizable(0,0)
            Label(over, text="下载完成").pack(padx=20, pady=5)
            url.set("")
            name.set("未知")
            number.set("未知")
            break#跳出循环
        else:#设定新的链接
            url.set(nexturl.get())
        
        time.sleep(1)#据说这样可以防止被防火墙ban掉


def imgsave(imgurl,imgname):#下载这张图片
    url = str(imgurl)
    path = str(imgpath.get())
    while 1:#服务器无响应的异常处理
        try:
            urllib.request.urlretrieve(url, path+"/"+imgname)
        except:
            time.sleep(1)
        else:
            break


def originalimgsave(originalimgurl,imgname):#下载这张图片的原始大小
    path = str(imgpath.get())
    while 1:#服务器无响应的异常处理
        try:#获取服务器响应
            response = requests.get(originalimgurl, headers=headers, allow_redirects=False)
        except:
            time.sleep(1)
        else:
            break
    realurl = response.headers["Location"]
    while 1:#服务器无响应的异常处理
        try:
            urllib.request.urlretrieve(realurl, path+"/"+imgname)
        except:
            time.sleep(1)
        else:
            break


def download():
    html = gethtml(url.get())
    downloadall(html)


urlframe = Frame()
urlentry = Entry(urlframe, textvariable=url).pack(side=LEFT)#网址输入框
inquirebutton = Button(urlframe, text="查询", command=inquire).pack(side=RIGHT)#查询按钮
urlframe.pack()

nameframe = Frame()
namelabel = Label(nameframe, text="名称：").pack(side=LEFT)
namelabel_show = Label(nameframe, textvariable=name).pack(side=RIGHT)#名称框
nameframe.pack()

nunberframe = Frame()
numberlabel = Label(nunberframe, text="图片数：").pack(side=LEFT)
numberlabel_show = Label(nunberframe, textvariable=number).pack(side=RIGHT)#图片数框
nunberframe.pack()

addressframe = Frame()
addresslabel_show = Label(addressframe, textvariable=address).pack(side=LEFT)#地址框
addressbutton = Button(addressframe, text="保存", command=getaddress).pack(side=RIGHT)#保存按钮
addressframe.pack()

downloadbutton = Button(root, text="下载", command=download).pack()#下载按钮

root.mainloop()
