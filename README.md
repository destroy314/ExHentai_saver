# ExHentai_saver
一个简单的Ex站图片批量下载工具，可用于没有提供BT下载的画廊。

## 特点
+ 具有图形界面
+ 短小
+ 比较不完善

## 使用方法
1. 使用开发者模式访问任意一个ExHentai页面，复制`Network`中`Request Headers`中的`Cookie`项，粘贴至第15行的双引号中。示例：  
```
'Cookie':
"ipb_member_id=XXXXXXX; ipb_pass_hash=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX; igneous=XXXXXXXXX; s=XXXXXXXXX;lv=XXXXXXXXXX-XXXXXXXXXX"
}
```

2. 对于形如 https://exhentai.org/g/XXXXXXX/XXXXXXXXXX/ 的画廊链接，粘贴至文本框中后依次点击**查询**、**保存**与**下载**。程序会在选择的文件夹中创建一个新文件夹，命名为画廊的原名，然后从第一张图片开始向其中下载图片，直到全部下载完成。如果选中了**下载原图**复选框，程序会优先下载原图。

3. 由于某些原因，可能会出现某张图片无法下载的情况。此时程序将在此图片处停止下载。可以等待片刻或手动输入另一张图片的链接后点击**下载**。

## 注意事项
+ 在遇到无法下载的图片时自动停止下载。
+ 正常运行时，程序也会被识别为未响应状态。
+ 与科学上网配合使用效果更佳。
+ 注意身体。
