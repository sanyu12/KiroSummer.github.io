title: Python多线程
date: 2016-01-05 16:47:39
tags: [python]
---
# Python多线程
## 线程or进程
多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。
<!-- more -->
## threading代码举例
```
    #!/tools/anaconda/bin/python2.7
    #coding=utf-8

    import sys
    import threading
    from time import ctime, sleep

    class fun:
        def __init__(self):
           self.count = 0

        def music(self, func):
            for i in range(2):
                print "I was listening to %s. %s" %(func, ctime())
                self.count += 1
                sleep(1)

        def movie(self, func):
            for i in range(2):
                print "I was watching at %s! %s" %(func, ctime())
                self.count += 5
                sleep(5)

        def execute(self):
            threads = []
            t1 = threading.Thread(target=self.music, args=(u'Star Sky',))
            threads.append(t1)
            t2 = threading.Thread(target=self.movie, args=(u'阿凡达',))
            threads.append(t2)
            for t in threads:
                t.setDaemon(True)
                t.start()
            t.join()  #在子线程完成之前，父线程就会一直阻塞

    if __name__ == "__main__":
        object = fun()
        object.execute()
        print "all over %s" %ctime()
```
这段代码的运行结果如下：
![多线程运行结果](/images/python/multi_thread.png)
我们可以看到，在这结果输出是有一点点问题的，第二行的输出前面为什么会有一个空格？
