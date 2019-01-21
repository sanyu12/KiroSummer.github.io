title: word2vec
date: 2015-12-20 22:22:55
tags: [word2vec]
---
# word2vec简介
这个工具能够将词转换为向量，这种向量可以应用于很多自然语言处理的应用以及深入的研究
<!-- more -->
# word2vec入门
* 下载代码：svn checkout [http://word2vec.googlecode.com/svn/trunk/](http://word2vec.googlecode.com/svn/trunk/)(如果没有svn或者不想安装svn，我们可以把代码导入到github上面进行下载)
* 运行"make"，编译生成word2vec工具
* 运行demo脚本："./demo-word.sh"和"./demo-phrases.sh"
* 如果你对改工具集有什么问题，查看[论坛](http://groups.google.com/group/word2vec-toolkit)

# word2vec是如何工作的
该word2vec工具将语料库为输入，并产生字向量作为输出。它首先构从训练文本数据中构建词汇，然后学习单词的向量表示。所得字向量文件可以作为特征应用在许多自然语言处理和机器学习应用。
一个简单的方法来调查了解学习到的表示是找到与用户指定的字最接近的字。distance工具就是用于这一目的。
demo-word.sh运行结果
![demo-word.sh运行结果](/images/demo-word.png)
demo-phrases.sh运行结果
![demo-phrases.sh运行结果](/images/demo-phrases.png)
demo-phrases.sh中对hello world的测试结果
![demo-phrases.sh中对hello world的测试结果](/images/demo-phrases-hello-world.png)
我们可以看到，在两个demo中"hello world"的位置是不一样的，产生的vector也是不一样的
demo-phrases.sh中对其他一些内容的测试结果
![demo-phrases.sh中对其他一些内容的测试结果](/images/demo-phrases-error.png)
我们可以看出来，好像并不能够测试某一些情况下的句子和中文。。
我使用手头上有的语料库，训练了一个train-word-vectors.bin，应用./distance train-word-vectors.bin，测试结果如下：
![./distance train-word-vectors.bin测试结果](/images/train-vector-test.png)

# 如何评价单词向量的质量
有如下几种因素影响单词向量的质量
* 训练数据的质量和数量
* 向量的大小
* 训练算法
demo-word-accuracy.sh的测试结果
![demo-word-accuracy.sh的测试结果](/images/demo-word-accuracy.png)
demo-phrase-accuracy.sh的测试结果，测试所消耗时间真的很长
![demo-phrase-accuracy.sh的测试结果](/images/demo-phrase-accuracy.png)

# word聚集
demo-classes.sh的测试结果
![demo-classes.sh的测试结果](/images/demo-classes.png)
输出文件classes.sorted.txt部分内容
![classes.sorted.txt部分内容](/images/classes-sorted.png)

# 后记，训练大文本纪实
今天要在一个约8G的文本预料训练出vector文件，在服务器上运行程序，还没跑出来，暂时的情况如下，11810728条句子、272298831个词，等明天早上再来看结果吧：
![bigdata训练](/images/bigdata-corpus.png)
还有一个问题就是，我应该在写文本的时候就加上"start"，"end"符号吗？我觉得是应该的
昨天晚上离开实验室的时候，在服务器上跑了加上"start"，"end"符号的程序，今天早上来的时候，程序跑好了，但是当我准备运行word2vec程序的时候，出现了如下的问题：
```
    time ./word2vec -train train-word-symbol.txt -output train-word-vectors.bin -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
    Illegal instruction (core dumped)

    real	0m0.337s
    user	0m0.000s
    sys	0m0.004s
```
*What happened!?*这个程序命令肯定是对的啊，下的我赶紧谷歌了了原因，未果，正当我不知道怎么办的时候，师姐在群里说了一句，“173下面的服务器崩了”
```
    致命错误：关闭/tmp/cclVujZK.s　时出错：设备上没有空间
```
哦，原来不是我的错误，怎么办呢？等待中。。
解决了，但是不知道是怎么解决的，管理员的事情吧。正在跑我的程序中用了60个线程，看样子速度应该还行
训练完成了，我们现在能够进行distance测试了，测试结果如下：
![bigdata测试](/images/bigdata-bin.png)

更多内容请查看谷歌官网[word2vec](https://code.google.com/p/word2vec/)
