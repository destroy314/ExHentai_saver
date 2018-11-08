from html.parser import HTMLParser
from tkinter.filedialog import *
from tkinter import *
import urllib.request
import threading
import requests
import time, sys, re, os


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
name = StringVar()#窗口上显示的图集名称
name.set("未知")
number = StringVar()#窗口上显示的图片数
number.set("未知")
address = StringVar()#窗口上显示的保存路径
address.set("选择位置")
imgpath = StringVar()
imgname = StringVar()
imgurl = StringVar()
originalimgurl = StringVar()
newurl = StringVar()
status = StringVar()#当前下载状态
a = IntVar()#记录图片下载尝试次数
a.set(1)
v = IntVar()#判断是否选中下载原图复选框
v.set(1)#默认为选中
r = IntVar()#判断是否选中重命名复选框
r.set(0)#默认为不选中
j = IntVar()#判断在下载的是图集还是图片
j.set(0)#0为图集，1为图片
f = IntVar()#判断路径是否在目标文件夹内
f.set(0)

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
        originalname = re.findall(namere, html)[0]
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
    imgstr = re.findall(imgnamere,html)[0]
    if r.get() == 0:
        imgname.set(imgstr)#设定图片名称
    else:
        exnamere = re.compile(r'\.(?:jpg|png)')#匹配扩展名
        exnamestr = re.findall(exnamere,imgstr)[0]
        imagenumberre = re.compile(r'><span>(\d+)</span>')#匹配图片序号
        imagenumberstr = re.findall(imagenumberre,html)[0]
        imgname.set(imagenumberstr + exnamestr)#图片名称设为序号

    imgurlre = re.compile(r'<img id="img" src="(.+)" style="')#匹配图片地址
    imgurl.set(re.findall(imgurlre,html)[0])#设定图片地址

    originalimgurlre = re.compile(r'<a href="([^>]+)">Download')#匹配原图地址
    originalimgurl.set("".join(re.findall(originalimgurlre,html)))#设定原图地址
        
    urlre = re.compile(r'load_image.\d+.{15}" href="([^>]+)"><img id')#匹配下一页链接
    nexturl.set(re.findall(urlre,html)[0])#设定链接

    newurlre = re.compile(r'"return nl\(\'(\d{5}-\d{6})\'\)"')#匹配新链接
    newurl.set(re.findall(newurlre,html)[0])#设定新链接
    newurl.set(url.get() + "#?nl=" + newurl.get())


def downloadall(html):#下载所有图片
    status.set("开始下载...")
    judgmenturl = str(url.get())
    galleryre = re.compile(r'exhentai.org/s/')#检查地址是图集还是图片
    judgment = "".join(re.findall(galleryre,judgmenturl))
    if judgment == "":#是图集
        j.set(0)
        imgpath.set(address.get()+"/"+name.get())
        path = str(imgpath.get())
        os.makedirs(path)
        firstre = re.compile(r'<a href="([^>]+)"><img alt="0*1"')#匹配首张图片的链接
        url.set(re.findall(firstre,html)[0])
    else:#是图片
        j.set(1)
        f.set(1)
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

        if a.get() == 3:#有图片下载失败就停止下载
            if j.get() == 0 and f.get() == 0:#如果正下载的是图集且未失败过
                address.set(address.get()+"/"+name.get())#向路径中添加正在下载的文件夹
                f.set(1)
            a.set(1)
            status.set(imgname.get()+"下载失败")
            try:
                os.remove(address.get()+"/"+imgname.get())
            except:
                pass
            active()
            break
        else:
            a.set(1)

        if url.get() == nexturl.get():#如果下一页链接与当前页链接相同则完成下载
            status.set("下载完成")
            if f.get() == 1:#如果路径在目标文件夹内，将路径设定为上一层
                f.set(0)
                address.set(re.findall(re.compile(r'(.*)(?=/.*)'),str(address.get()))[0])
            url.set("")
            name.set("未知")
            number.set("未知")
            active()
            break
        else:#设定新的链接
            url.set(nexturl.get())
        

def imgsave(saveimgurl,saveimgname):#下载这张图片
    url = str(saveimgurl)
    path = str(imgpath.get())
    while a.get() < 3:#服务器无响应的异常处理
        try:
            status.set("第"+str(a.get())+"次下载"+saveimgname+"...")
            urllib.request.urlretrieve(url, path+"/"+saveimgname)#下载图片
        except:
            a.set(a.get() + 1)
            time.sleep(1)#若失败则将a加一并等待一秒
        else:
            a.set(1)
            break#若成功则跳出循环
    if a.get() != 3:
        a.set(1)
        return
    a.set(1)
    pagere(newurl.get())
    url = str(imgurl.get())
    while a.get() < 3:#从新链接下载图片
        try:
            status.set("第"+a.get()+"次下载新"+saveimgname+"...")
            urllib.request.urlretrieve(url, path+"/"+saveimgname)
        except:
            a.set(a.get() + 1)
            time.sleep(1)
        else:
            a.set(1)
            break


def originalimgsave(saveoriginalimgurl,saveimgname):#下载这张图片的原始大小
    path = str(imgpath.get())
    while 1:#服务器无响应的异常处理
        try:#获取服务器响应
            status.set("获取原图地址...")
            response = requests.get(saveoriginalimgurl, headers=headers, allow_redirects=False)#获取原图真实地址
        except:
            time.sleep(1)
        else:
            break
    realurl = response.headers["Location"]
    while a.get() < 3:#服务器无响应的异常处理
        try:
            status.set("第"+str(a.get())+"次下载原图"+saveimgname+"...")
            urllib.request.urlretrieve(realurl, path+"/"+saveimgname)
        except:
            a.set(a.get() + 1)
            time.sleep(1)
        else:
            a.set(1)
            break


def disable():
    for i in widget:
        i['state']='disabled'


def active():
    for i in widget:
        i['state']='normal'


def download():
    disable()
    html = gethtml(url.get())
    downloadall(html)


t = threading.Thread(target = download)
def down():
    global t
    if not t.is_alive():
        t = threading.Thread(target = download)
        t.start()


def stop():
    sys.exit(0)#如果没有这句，在下载过程中关闭窗口后下载进程仍会运行


urlframe = Frame()
urlentry = Entry(urlframe, textvariable=url)#网址输入框
urlentry.pack(side=LEFT)
inquirebutton = Button(urlframe, text="查询", command=inquire)#查询按钮
inquirebutton.pack(side=RIGHT)
urlframe.pack()

nameframe = Frame()
namelabel = Label(nameframe, text="名称：")
namelabel.pack(side=LEFT)
namelabel_show = Label(nameframe, textvariable=name)#名称框
namelabel_show.pack(side=RIGHT)
nameframe.pack()

nunberframe = Frame()
numberlabel = Label(nunberframe, text="图片数：")
numberlabel.pack(side=LEFT)
numberlabel_show = Label(nunberframe, textvariable=number)#图片数框
numberlabel_show.pack(side=RIGHT)
nunberframe.pack()

addressframe = Frame()
addresslabel_show = Label(addressframe, textvariable=address)#地址框
addresslabel_show.pack(side=LEFT)
addressbutton = Button(addressframe, text="保存", command=getaddress)#保存按钮
addressbutton.pack(side=RIGHT)
addressframe.pack()

downloadframe = Frame()
rename = Checkbutton(downloadframe, text="重命名", variable=r)
rename.pack(side=LEFT)
downloadoriginal = Checkbutton(downloadframe, text="原图", variable=v)#下载原图选择按钮
downloadoriginal.pack(side=LEFT)
downloadbutton = Button(downloadframe, text="下载", command=down)#下载按钮
downloadbutton.pack(side=RIGHT)
downloadframe.pack()

status_show = Entry(root, textvariable=status, state='readonly').pack()

widget = [
urlentry,
inquirebutton,
namelabel,
namelabel_show,
numberlabel,
numberlabel_show,
addresslabel_show,
addressbutton,
rename,
downloadoriginal,
downloadbutton]

root.protocol('WM_DELETE_WINDOW', stop)
root.mainloop()
