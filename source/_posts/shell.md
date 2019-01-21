title: shell
date: 2015-12-25 16:47:39
tags: [linux, shell]
---
# shell中常用的命令总结
## tee
tee:在将终端上的信息重定向到文件中的同时能在终端上看到输出信息
例子：
```
	ls | tee ls.txt
```
<!-- more -->
## 程序的后台运行
nohup:不挂起，将程序直接放在后台运行
今天老夫发现了一个坑爹的事情，好像这么写不能够看到程序的输出，要等到程序运行完成才能够看到输出，异常倒是能够看到
如果需要，加上sys.stdout.flush()
例子：
```
	nohup ./program >program.log 2>&1 &	
```
## scp相关用法
上传文件到服务器：
```
    scp -r -P 55555 ./conditional-random-field/ qrxia@192.168.131.172:~/nlp/experiment
```
-P：指定端口号为55555
## 删除文件夹下所有的出txt之外的所有文件
```
	find . -type f ! -name "*.cpp"
```
## 根据相关信息批量删除进行
```
	ps -ef | egrep 'test_network' | awk '{print $2}' | xargs kill
```
## 查看自己所占用的空间
```
	du -sh .
```
## 格式化硬盘
```
	sudo umount /dev/sdb1  # 先将硬盘挂载
	sudo mkfs.ext4 -m 0.1 /dev/sdb1  # 将硬盘格式化成ext4，-m 0.1 表示给sudo用户留0.1%的空间
	df -lhT  # 查看一下硬盘的文件系统格式
	>>>/dev/sdb1      ext4      3.6T   68M  3.6T   1%  # 文件系统如下
```
