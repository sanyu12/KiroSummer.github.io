title: Python调用C语言程序
date: 2015-12-23 21:16:17
tags: [python, c]
---
#C语言部分的编写规则
<!-- more -->
C语言部分没有什么改变，和往常一样即可：
```
	#include<stdlib.h>
	#include<stdio.h>

	int foo(int a, int b)
	{
		printf("Your input %i and %i\n", a, b);
		return a + b;
	}
```
编译的时候需要注意：gcc编译：gcc -o c.so -shared -fPIC c.c

#Python部分的编写规则
需要引入ctypes包
```
	import ctypes  
	ll = ctypes.cdll.LoadLibrary 
	lib = ll("./test.so")  
	lib.foo(1, 3)  
```

