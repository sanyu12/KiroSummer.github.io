title: tips
date: 2016-01-01 09:36:38
tags: [tips]
---
# 简要
本篇博客主要记录一些比较杂的小知识，主要解决在工作中遇到的一些问题(要学会使用Google，Google大法好)

<!--more-->
## pip install
pip install在国内非常不好用，该死的GFW
解决方案，加上源(我使用的豆瓣源)：-i http://pypi.douban.com/simple
例如：
```
    sudo pip install --no-use-wheel --upgrade distribute -i http://pypi.douban.com/simple pyflakes
```
如果遇到下面的问题：
![pip错误](/images/pip/pip-error1.png)
记得要加上__--no-use-wheel --upgrade distribute__

## sublime更新冲突
```
	sudo dpkg -r sublime-text-installer
```
然后点击deb文件即可。

## Ubuntu搜狗输入法崩了怎么办？
```
	fcitx &
	sogou-qimpanel &
```
这个过程中可能要你不时的敲回车
## /boot满了
```
uname -a
Linux kiro-OptiPlex-3020 3.19.0-51-generic #58~14.04.1-Ubuntu SMP Fri Feb 26 22:02:58 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
```
查看系统目前使用的是哪一个内核，我的目前是3.19.0-51
紧接着查看有哪些linux内核
```
dpkg --get-selections | grep linux-image
linux-image-3.19.0-37-generic			deinstall
linux-image-3.19.0-39-generic			deinstall
linux-image-3.19.0-41-generic			deinstall
linux-image-3.19.0-42-generic			install
linux-image-3.19.0-43-generic			install
linux-image-3.19.0-47-generic			install
linux-image-3.19.0-51-generic			install
linux-image-extra-3.19.0-37-generic		deinstall
linux-image-extra-3.19.0-39-generic		deinstall
linux-image-extra-3.19.0-41-generic		deinstall
linux-image-extra-3.19.0-42-generic		install
linux-image-extra-3.19.0-43-generic		install
linux-image-extra-3.19.0-47-generic		install
linux-image-extra-3.19.0-51-generic		install
linux-image-generic-lts-vivid			install
```
然后删除一些我们不在需要的
```
udo apt-get remove linux-image-3.19.0-42-generic
```
## no valid OpenPGP data found.
```shell
wget --no-check-certificate -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
```
注意，重要的是要加上__--no-check-certificate__

## 安装特定版本的 numpy
```
sudo pip install numpy==1.14.0
```

## 因为一些乱七八糟的原因，Ubuntu14.04 进入不了系统了？WTF！
描述：grub正常，就是在进入系统的时候，死活到不了登陆界面，纯文本界面页打不开，一个光标在屏幕左上角停在那边，不闪烁？！
解决方案: 看日志，我的是因为intel的显卡驱动不知道怎么没了？可能因为昨天倒腾电脑弄成这个样子的。。
[链接](https://ubuntuforums.org/showthread.php?t=2298218&page=3)
重要收获，要学会看系统的日志，会给出非常重要的提示信息！我以前就是一个非常不喜欢看日志的人！
### 还有一点
/tmp 文件夹不要随便删除，不要随便更改权限！Linux还在途中啊。。
