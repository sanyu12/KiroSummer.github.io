title: neural-network-tag-all-data
date: 2016-01-01 16:47:39
tags: [neural-network, python]
---
# 概述
因为要使用所有的数据进行神经网络词性标注工作，正好也是新的一年的开始，以前的东西难免有一点遗忘，所以我现在就乘这个机会重新开始工作，做好数据的记录，方便以后查找。

# 语料库的处理
## Corpus.conll转换成word2vec所需要的格式文件
我们将train.conll加在大数据量的conll数据后面，形成我们所需要的语料库Corpus.conll，使用*process-corpus.py*进行处理，生成word2vec所需要的文件Corpus.txt。
![process-corpus.py处理结果](/images/neural-network-all-data/process-corpus.png)
<!-- more -->
## 生成corpus embeddings
使用得到的Corpus.txt，利用word2vec工具，我们生成corpus embeddings文件（train-embedding.sh）。
![train-embedding.sh的处理结果](/images/neural-network-all-data/train-embedding.png)
然后我们根据得到的corpus embedding文件和corpus.conll文件，使用corpus中出现频率为1的词的向量的平均值作为我们的oov，但是在具体的实施过程中，我发现并不是每一个词都会出现再embedding中，具体的是频率大于等于5的才会出现，上网查找具体的原因，发现word2vec中默认的设置的最低频率就是5，有一个参数__-min-count__设置成5就可以，这样，出现次数小于5的就不会被舍弃掉。
从下图中，我们可以看到，corpus中不同的词有1948986个。
![corpus中一共有这么多个不同的词](/images/neural-network-all-data/different-words-in-corpus.png)
所以，我们重新处理了一下数据，用符号__\*\*\*__代表句子的开始，__$$$__代表句子的结束，每个词对应的vector的size=50，处理结果如下：
![coerpus-embeddings](/images/neural-network-all-data/corpus-embeddings-size50.png)
## 提取tag
为了以后方便和相对节约程序运行的时间，我们把train.conll，dev.conll，test.conll中的tag提取出来，单独放置在一个文件当中。
![tag.png](/images/neural-network-all-data/tag.png)
## 提取不同的word
同样为了以后的工作，需要将train、dev、test三个文件中的word都提取出来，单独放置在一个文件中。
![word.png](/images/neural-network-all-data/word.png)
## 根据corpus embeddings生成oov
根据Corpus.conll中出现次数为1的词，对应相应的vector，然后将所有的vector相加之后取其平均值，就能够得到oov。
但是有一个问题是：程序跑的很慢，原因一直没有想通，今天早晨突然想明白了，为了方便实验结果，我在程序中使用了大量的__刷新显示__,每读取一个单词就刷新一次显示，这样子能够非常清晰的看到程序跑到了什么地步。昨天夜里后台跑的程序一直没有出结果，这让我很纠结，没有办法，今天早上还把程序放在了前台来跑，我稍微修改了一下程序，每一个sentence我刷新显示一下，然后发现程序很快就将7.9G的Corpus.conll读取完成了，现在正在抽取词频为1的vector做oov。
### 使用shell抽取出Corpus.conll中词频为1的词
此间过程很复杂,我开始用小数据量dev.conll进行测试,发现使用shell脚本输出的词频为1的个数是5051,但是使用python程序计算出来的词频为1的个数是5187,这让我百思不得其解.后来,我依次排查所使用的awk、sed、sort、uniq，发现就是在uniq这一步的时候，出了问题，我写了个python程序，将5187个word和5051个word依次比对，有136个数据在使用uniq的时候出现了问题！然后我上网查找问题，果然，在使用__uniq__处理全角字符的时候是有问题的！
uniq命令在判断两个字符串是否相等的时候，和LC\_ALL这个环境变量是有很大的关系的，如果将其设置成UTF8，那么有可能一些不同的字符被判断为相同的。那么如何解决？我们可以把环境变量的值设置成C，这样的话uniq就会一个一个字节的对两个字符串进行比较，这样子得到的结果就是对的了。
附上我的shell脚本：
```
	#!/bin/bash
	export LC_ALL=C
	awk < $1 '{print $2}' > temp.awk
	sed '/^$/d' temp.awk > temp.sed
	sort temp.sed > temp.sort
	uniq -c temp.sort > temp.uniq
	sort -k1 -n temp.uniq > temp.sort2.0
	egrep '^      1 ' temp.sort2.0 > temp.word
	awk < temp.word '{print $2}' > temp.txt
	export LC_ALL=zh_CN.utf8
	rm temp.awk temp.sed temp.sort temp.uniq temp.sort2.0 temp.word
```
这样子我就能够得到词频为1的Corpus文件corpus-one-time-word.txt，然后根据这个里面的词再训练oov，可能会快一点。但是今天早上我来实验室，发现程序还没有跑完。。。
总共有1123613个词频为1的word，1948989个embedding
![corpus-one-time-word.png](/images/neural-network-all-data/corpus-one-time-word.png)
### Ubuntu14.04崩了
昨天晚上系统好好地，然后突然告诉我系统发生了错误，我没多想，重启了一下，然后发现系统在登陆界面的时候彻底卡死！键盘鼠标都不能用，经过一番折腾，我在ubunut的引导界面的时候选择了__advanced ubuntu__，然后选择了某一个版本内核的系统，不是*recover mode*，然后系统就好了！
### 使用corpus-embedding的最后10000个词作为语料来训练oov
因为如果使用全部的数据来训练oov，过程实在太慢，所以我们决定使用embedding的最后10000个word embedding来训练oov。
```
	tail -n 10000 corpus-embeddings.txt > oov-embeddings.txt
```
当我打开文件准备看看结果如何的时候，我惊呆了！什么鬼啊，怎么乱码了？我又看了一下corput-embeddings.txt，怎么也乱码了？怎么变成latin1的编码了？怎么什么奇怪的事情都会发生！我又看了一下corpus.txt还好，是好的，于是我又重新训练了一遍corpus-embeddiing.txt
结果还是乱码啊，中午还是好的，怎么出去一趟就乱码了呢？！上网上找了各种方法，结果有一种是好的，在.vimrc中加入：
```
	:set fencs=utf8
```
这样子，稍微修改以下get-oov.py的代码，oov的embedding就训练好了。
![oov-embedding](/images/neural-network-all-data/oov-embedding.png)
然后将oov的embedding加入到base-embeddings.txt中去，已经查明，没有"UNKNOWN"，可以放心的加入。同时也已经验证完毕，最后10000个词的词频都是1
## 线性模型测试结果
为了一定程度上监控神经网络的结果，我用线性模型测试了，结果如下，大约93.17：
![linear-model-all-data](/images/neural-network-all-data/linear-model-all-data.png)
## 使用小数据量进行测试
train数据量选取2000句子，dev选取200句子
### 使用线性模型进行测试
使用线性模型对小数据量进行测试，结果如下：最好的准确率92.78%
![s-linear-model](/images/neural-network-all-data/s-linear-model.png)
### 对hidden layer neuron number进行调参
epoch = 500, eta = 0.05, lmbda = 1e-2, mini\_batch\_size = 50, 激活函数 = tanh, 使用adagrad

|__hidden layer neuron number__|__best precision/epoch__|
|--------------|--------------------|
|50            |86.29%/7            |
|80            |87.47%/7            |
|100           |86.89%/4            |
|130           |87.69%/2            |
|150           |87.69%/6            |
|180           |87.96%/2            |

从以上的数据，我们可以看出来，最好的正确率在hidden neuron number=180的时候，不过这些数据的差别不大，所以暂定使用150
### 对eta步长进行调参
epoch = 500, hidden layer neuron number = 150, lmbda = 1e-2, mini\_batch\_size = 50, 激活函数 = tanh，使用adagrad

|__eta__|__best precision/epoch__|
|-------|------------------------|
|0.0001 |30.03%/2中断            |
|0.0005 |55.23%/12中断           |
|0.001  |69.17%/11中断           |
|0.005  |85.40%/5中断            |
|0.01   |87.43%/5                |
|0.05   |87.45%/3                |
|0.1    |87.58%/5                |
|0.5    |80.34%/9                |
|1      |58.59%/8                |
|5      |0/0??                   |

从上面的数据我们可以看出来，准确率最高的是当eta = 0.1的时候

### 对mini batch size进行调参
epoch = 500, hidden layer neuron number = 150, eta = 0.05, lmbda = 1e-2, 激活函数 = tanh， 使用adagrad

|__mini batch size__|__best precision/epoch__|
|-----------|---------------|
|1          |86.79%/8       |
|5          |87.45%/3       |
|20         |87.26%/5       |
|50         |87.26%/4       |
|60         |88.28%/3       |
|70         |87.60%/3       |
|80         |87.54%/2       |
|100        |87.56%/3       |

从上面的数据我们可以看到最好的正确率在mini batch size = 60的时候，在88.28%左右

### 对lmbda进行调参
epoch = 500, hidden layer neuron number = 150, eta = 0.05, mini batch size = 60, 激活函数 = tanh, 使用adagrad

|__lambda__|__best precision/epoch__|
|----------|----------------|
|1e-6      |87.37%/4        |
|1e-5      |87.73%/4        |
|1e-4      |87.16%/3        |
|1e-3      |87.30%/5        |
|1e-2      |87.85%/7        |
|1e-1      |87.66%/5        |
|1         |87.77%/3        |
|5         |87.87%/2        |

从以上数据我们可以看到，好像lambda的取值没什么差别。
### 总结
我的代码应该有问题！





