# ExHentai_saver
一个简单的Ex站图片批量下载工具，可用于没有提供洪流下载的画廊。

##特点
+ 具有图形界面
+ 短小
+ 不完善

##使用方法
1. 访问任意一个ExHentai的页面，复制`Request Headers`中的`Cookie`项，粘贴至第17行的双引号中。示例：  
```
'Cookie':
"ipb_member_id=XXXXXXX; ipb_pass_hash=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX; igneous=XXXXXXXXX; s=XXXXXXXXX;lv=XXXXXXXXXX-XXXXXXXXXX"
}
```

2. 对于形如 https://exhentai.org/g/XXXXXXX/XXXXXXXXXX/ 的画廊链接，粘贴至文本框中后依次点击**查询**、**保存**与**下载**。程序会在选择的文件夹中创建一个新文件夹，命名为画廊的原名，然后从第一张图片开始向其中下载图片，直到全部下载完成。程序会优先下载原图。

3. 由于某些原因，可能会出现某张图片无法下载的情况。此时程序将不断尝试下载无法下载的图片。应重启程序，并在画廊页面中寻找一张新的图片作为开始。将形如 https://exhentai.org/s/XXXXXXXXXX/XXXXXXX-X 的图片链接粘贴至文本框后，点击**保存**选择原先创建的文件夹，然后点击**下载**。下载逻辑不会改变，而下载时不再创建文件夹。

##注意事项
+ 为防止在一张无法下载的图片上浪费时间，应不时查看下载进度。
+ 正常运行时，程序也会被识别为未响应状态。
+ 如需打包成.exe文件，可以使用提供的图标。
+ 注意身体。
