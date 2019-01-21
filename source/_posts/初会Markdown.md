title: Markdown初会
date: 2016-01-06 16:47:39
tags: Markdown
MathJax: true
---
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default">
</script>
# 简介
Markdown是一种轻量级标记语言，能将文本转换成XHTML（或者HTML）文档，它的目标是实现易读易写，成为一种适用于网络的书写语言。
用途：Github的Readme.md
<!-- more -->
# 强调
*我是斜体*
**我是加粗**
***我是粗斜体***

# 列表
* 无序列表
* 子项
* 子项

有序列表
1. 第一行
2. 第二行

# 链接
内嵌方式：
[Google](https://www.google.com)

引用方式：
[kiro weibo][id]
[id]: https://www.weibo.com/kirosummer "kiro's weibo"

# 代码和语法高亮
我是用来介绍`Markdown`的
```
	python
	s = "Python syntax highlighting"
```
# 数学公式
## forkosh服务器
使用forkosh服务器<img src="http://www.forkosh.com/mathtex.cgi? $$x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$$">
```
	<img src="http://www.forkosh.com/mathtex.cgi? $$x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$$">
```
## MathJax方式
Simple inline $a = b + c$.
$ \frac{|ax + by + c|}{\sqrt{a^{2}+b^{2}}} $
