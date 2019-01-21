title: python-assistance
date: 2016-08-12 18:42:58
tags: [python]
---
本篇博客记录一下本学期的Python助教工作
[windows下安装Python教程](/documents/python/windows下安装python教程.pdf)
<!--more-->

## 时间相关的模块
### time
Python的time模块下有很多函数可以转换常见日期格式。如函数time.time()用于获取当前时间。
#### 时间元组
许多Python时间函数将时间处理为9个数字的元组.
```python
import time
print(time.localtime())
>>> time.struct_time(tm_year=2017, tm_mon=11, tm_mday=2, tm_hour=16, tm_min=42, tm_sec=36, tm_wday=3, tm_yday=306, tm_isdst=0)
```
```bash
time.strftime(fmt[,tupletime])  # 接受在本地时间表示为时间元组的瞬间，并返回一个表示由字符串fmt指定的时间的字符串。
```
```python
import time

if __name__ == "__main__":
	print("当前时间是：" + time.strftime("%H:%M:%S", time.localtime()))

>>>当前时间是：16:27:41

import time

if __name__ == "__main__":
	t = time.time()  # 格林治时间，比北京时间晚8h
	d = t / (24 * 60 * 60)
	s = (t - int(d) * 24 * 60 * 60) / (60 * 60)
	print(str(int(d)) + " day " + str(s) + " hour")

>>>17472 day 8.500231066611079 hour
```


![更加详细的内容](http://www.runoob.com/python/python-date-time.html)
### datetime
