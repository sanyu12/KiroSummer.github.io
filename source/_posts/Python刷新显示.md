title: Python刷新显示
date: 2015-12-25 09:44:23
tags: [python, flush]
---
# Python刷新显示的示例代码
```
	#!/usr/bin/python

	import sys
	from time import sleep

	for i in range(0, 5):
		print "\rhello kiro ", i,
		sys.stdout.flush()
		sleep(1)
```
