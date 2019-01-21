title: Git简介
date: 2016-01-14 16:47:39
tags: [git]
---
# Git
## Git简介
首先：我为什么要写这篇文章呢？因为今天我写conditional random field的代码的时候，把其中一个函数直接覆盖掉了，然后想改回来，没办法，保存过了，修改不回来了。其实，Git我使用过，只不过很少使用，一是因为我总觉得git命令太难记得了，因为一段时间按不用就会忘记。所以，我今天写下这篇使用指南，防止我以后记不住，看看自己的博客就行了。
Git，世界上最先进的、流行的分布式版本控制系统。
<!--more-->
## Git安装
我的系统是Ubuntu，so
```
    sudo apt-get install git
```
其他系统的安装方法，自行google

安装完成之后，需要进一步的配置：
```
	git config --global user.name "your Name"
	git config --global user.email "email@example.com"
```

## Git创建版本库repository
这里面我已我的global lienar model举个例子，正好这个项目我还没有上传Git

首先，切换到工程目录：
```
	kiro@kiro-OptiPlex-3020:~/NLP/experiment/globallinearmodel$
```
上面的路径就是我的工程目录

__git init__可以将当前目录变成Git管理的版本库repository
```
	kiro@kiro-OptiPlex-3020:~/NLP/experiment/globallinearmodel$ git init
	Initialized empty Git repository in /home/kiro/NLP/experiment/globallinearmodel/.git/
```
## 将相关文件添加到版本库
因为并不是我需要将所有的文件都添加到版本库当中，一般情况下，我只需要添加代码文件即可，个人习惯。
```
 	git add globallinearmodel_optimized.py globallinearmodel.py
```
在这里，我添加了两个代码文件，是目前写的实现的global lienar model的代码文件，同样的功能，实现方法有点差别

## 将文件添加到仓库
```
	>>>>git commit -m "global linear model"
	[master (root-commit) 3b0036d] global linear model
	2 files changed, 851 insertions(+)
	create mode 100755 globallinearmodel.py
	create mode 100755 globallinearmodel_optimized.py
```
从上面的结果我们可以看到，相关文件添加到版本库成功。

## 添加远程库
如下图所示，我们创建远程库，填写相关信息
![git远程库](/images/git/git.png)

根据提示，我们选择将我们本地的库推送到远程库
![git push](/images/git/git_push.png)
```
	git remote add origin https://github.com/KiroSummer/global-linear-model.git
	git push -u origin master
```
global linear model的相关库创建完毕！

## 利用 hexo实现的多台电脑博客
![链接](http://chown-jane-y.coding.me/2017/03/15/%E5%A6%82%E4%BD%95%E5%9C%A8%E4%B8%8D%E5%90%8C%E7%94%B5%E8%84%91%E4%B8%8A%E5%90%8C%E6%97%B6%E5%86%99hexo%E5%8D%9A%E5%AE%A2%EF%BC%9F/)
