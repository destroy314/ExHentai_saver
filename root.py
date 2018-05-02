from html.parser import HTMLParser
from tkinter.filedialog import *
from tkinter import *
import urllib.request
import requests
import time, re, os


root = Tk()
root.title("")
root.iconbitmap("favicon.ico")


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
imgurl = StringVar()
originalimgurl = StringVar()
newurl = StringVar()
a = IntVar()
a.set(0)
v = IntVar()
v.set(1)


def gethtml(url):#获取网页源码
    html_parser = HTMLParser()
    request = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(request)
    originalhtml = page.read().decode('utf-8')
    html = html_parser.unescape(originalhtml)#将html编码的字符转换为原字符
    return html


def getname(html):#获取图集名称
    namere = re.compile(r'<h1 id="gj">([^>]+)</h1>')
    originalname = "".join(re.findall(namere, html))
    legalname = re.sub(r'[?*/\\<>:"|]',"",originalname)#删去图集名称中不能作为文件名的字符
    name.set(legalname)
    if name.get() == "":#如果没有原名
        namere = re.compile(r'<h1 id="gn">([^>]+)</h1>')
        originalname = "".join(re.findall(namere, html))
        legalname = re.sub(r'[?*/\\<>:"|]',"",originalname)
        name.set(legalname)


def getnumber(html):#获取图片张数
    numberre = re.compile(r'<td class="gdt2">([0-9]+) pages</td>')
    number.set(re.findall(numberre, html))


def inquire():#查询图集信息
    html = gethtml(url.get())
    getname(html)
    getnumber(html)


def getaddress():
    address.set(askdirectory())


def pagere(pageurl):
    html = gethtml(pageurl)

    imgnamere = re.compile(r'<div>([^>]+\.(?:jpg|png))')#匹配图片名称
    imglist = re.findall(imgnamere,html)
    imgname.set("".join(imglist[0]))#设定图片名称，名称会匹配到两个一样的

    imgurlre = re.compile(r'<img id="img" src="(.+)" style="')#匹配图片地址
    imgurl.set("".join(re.findall(imgurlre,html)))#设定图片地址

    originalimgurlre = re.compile(r'<a href="([^>]+)">Download')#匹配原图地址
    originalimgurl.set("".join(re.findall(originalimgurlre,html)))#设定原图地址
        
    urlre = re.compile(r'load_image.\d+.{15}" href="([^>]+)"><img id')#匹配下一页链接
    nexturl.set("".join(re.findall(urlre,html)))#设定链接

    newurlre = re.compile(r'"return nl\(\'(\d{5}-\d{6})\'\)"')#匹配新链接
    newurl.set("".join(re.findall(newurlre,html)))#设定新链接
    newurl.set(url.get()+"#?nl="+newurl.get())


def downloadall(html):#下载所有图片
    judgmenturl = str(url.get())
    galleryre = re.compile(r'exhentai.org/s/')#检查地址是图集还是图片
    judgment = "".join(re.findall(galleryre,judgmenturl))
    if judgment == "":
        imgpath.set(address.get()+"/"+name.get())
        path = str(imgpath.get())
        os.makedirs(path)
        firstre = re.compile(r'<a href="([^>]+)"><img alt="0*1"')#匹配首张图片的链接
        url.set("".join(re.findall(firstre,html)))
    else:
        imgpath.set(address.get())
        path = str(imgpath.get())

    while 1:#无限循环下载图片
        pagere(url.get())

        if v.get() == 0:
            imgsave(imgurl.get(),imgname.get())
        elif originalimgurl.get() == "":#没原图就直接下，有原图就下原图
            imgsave(imgurl.get(),imgname.get())
        else:
            originalimgsave(originalimgurl.get(),imgname.get())

        if a.get() == 2:#有图片下载失败就停止下载
            a.set(0)
            over = Toplevel()
            over.resizable(0,0)
            Label(over, text=imgname.get()+"下载失败").pack(padx=20, pady=5)
            url.set("")
            name.set("未知")
            number.set("未知")
            break
        else:
            a.set(0)

        if url.get() == nexturl.get():#如果下一页链接与当前页链接相同则完成下载
            over = Toplevel()
            over.resizable(0,0)
            Label(over, text="下载完成").pack(padx=20, pady=5)
            url.set("")
            name.set("未知")
            number.set("未知")
            break
        else:#设定新的链接
            url.set(nexturl.get())
        
        time.sleep(0.5)#据说这样可以防止被防火墙ban掉


def imgsave(saveimgurl,saveimgname):#下载这张图片
    url = str(saveimgurl)
    path = str(imgpath.get())
    while a.get() < 2:#服务器无响应的异常处理
        try:
            urllib.request.urlretrieve(url, path+"/"+saveimgname)#下载图片
        except:
            a.set(a.get() + 1)
            time.sleep(1)#若失败则将a加一并等待一秒
        else:
            a.set(0)
            break#若成功则跳出循环
    a.set(0)
    pagere(newurl.get())
    url = str(imgurl.get())
    while a.get() < 2:#从新链接下载图片
        try:
            urllib.request.urlretrieve(url, path+"/"+saveimgname)
        except:
            a.set(a.get() + 1)
            time.sleep(1)
        else:
            a.set(0)
            break


def originalimgsave(saveoriginalimgurl,saveimgname):#下载这张图片的原始大小
    path = str(imgpath.get())
    while 1:#服务器无响应的异常处理
        try:#获取服务器响应
            response = requests.get(saveoriginalimgurl, headers=headers, allow_redirects=False)#获取原图真实地址
        except:
            time.sleep(1)
        else:
            break
    realurl = response.headers["Location"]
    while a.get() < 2:#服务器无响应的异常处理
        try:
            urllib.request.urlretrieve(realurl, path+"/"+saveimgname)
        except:
            a.set(a.get() + 1)
            time.sleep(1)
        else:
            a.set(0)
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

downloadframe = Frame()
downloadoriginal = Checkbutton(downloadframe, text="下载原图", variable=v).pack(side=LEFT)#下载原图选择按钮
downloadbutton = Button(downloadframe, text="下载", command=download).pack(side=RIGHT)#下载按钮
downloadframe.pack()

root.mainloop()
