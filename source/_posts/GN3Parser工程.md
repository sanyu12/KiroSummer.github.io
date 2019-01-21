title: GN3Parser工程
date: 2017-2-18 09:20:20
tags: [work, depparser]
mathjax: true
---
# 概述
开此博客记录在开发GN3Parser(重现SyntaxNet)过程中的一些问题(已经重现成功！！！)

<!--more-->
## 中文实验的一些说明
### 中文embedding：
中文的embedding，利用Giga数据、word2vec，15次迭代，300dim，进行训练，训练完成的embedding位于：
qrxia@m172 ~/data/giga/giga-300-dim
### 实验总结(2017-5-10)
已经重现了SyntaxNet，GN3Parser的实验数据总结如下：
![ExperimentResults](/images/GN3Parser/GN3Parser实验数据.png)

可能是我们英文的Beam Size大小设置小了，所以英文效果才不行
补充的英文实验 (beam size = 64): (2017-5-12)

|__model__|__method__|__UAS__|__LAS__|__comments__|__position__|
|---------|----------|-------|-------|------------|------------|
|GN3Parser|Global    |       |       |Dev         |m173 ~/GN3Parser-beta/baidu-1024-beam-size-64 |
|GN3Parser|Global    |       |       |Test        |m173 ~/GN3Parser-beta/baidu-1024-beam-size-64 |
### 利用GN3Parser-POS 5-fold实验的数据进行GN3Parser的实验(2017-5-22)

|__model__|__method__|__UAS__|__LAS__|__comments__|__position__|
|---------|----------|-------|-------|------------|------------|
|GN3Parser|Greedy    |80.48%|76.66% |Dev with NN autoPOS |gpu-no-1:~/GN3Parser-beta/3.9.9-w-NN-autoPOS  |
|GN3Parser|Greedy    |80.32%|76.34% |Test with NN autoPOS |gpu-no-1:~/GN3Parser-beta/3.9.9-w-NN-autoPOS  |
|GN3Parser|Global    |82.77%|78.95% |Dev          |gpu-no-1:~/GN3Parser-beta/3.9.9-w-NN-autoPOS  |
|GN3Parser|Global    |83.11%|79.12% |Test         |gpu-no-1:~/GN3Parser-beta/3.9.9-w-NN-autoPOS  |

### 查看百度方面提供的POS的准确率(2017-5-17)
Train: 94.78% | Dev: 94.33% | Test: 94.23%
### 验证NN POS Tagger的词性是否真的不好使(2017-6-3)
因为在GN3Parser的后来的版本代码中，GN3Parser-POS输出的词性在Parsing效果中并不是很好。我怀疑是代码中可能存在着bug，所以，跑一个验证实验。利用v3.9.5版本代码（该版本代码在百度提供的数据上面效果是正常的），处理了相关的数据，看一下是否我的词性真的不行？！（明明我的词性效果要好于百度提供的词性）

|__model__|__method__|__UAS__|__LAS__|__comments__|__position__|
|---------|----------|-------|-------|------------|------------|
|GN3Parser|Greedy    |80.99% |77.31% |Dev         |m175 ~/GN3Parser-beta/3.9.5-w-NN-POS |
|GN3Parser|Greedy    |80.90% |77.01% |Test        |m175 ~/GN3Parser-beta/3.9.5-w-NN-POS |
|GN3Parser|Global    |84.35% |80.91% |Dev         |m175 ~/GN3Parser-beta/3.9.5-w-NN-POS |
|GN3Parser|Global    |84.33% |80.72% |Test        |m175 ~/GN3Parser-beta/3.9.5-w-NN-POS |
src-v3.9.8的代码应该都是可以的。因为从下面的试验中，我们可以看出来，效果还是在预想中的。
经过查看相关的代码，我发现，src-v3.9.9的代码还是沿用的“精简”Label的特征，但是应该不会造成这么严重的影响。正在做相关的实验进行验证。(2017-6-5)

|__Corpus__|__method__|__UAS__|__LAS__|__comments__|__position__|
|---------|----------|-------|-------|------------|------------|
|Dev      |Greedy    |80.99% |77.31% |baidu data  |m175 ~/GN3Parser-beta/3.9.5-w-NN-POS  |
|Test     |Greedy    |80.90% |77.01% |baidu data  |m175 ~/GN3Parser-beta/3.9.5-w-NN-POS  |
|Dev      |Global    |84.35% |80.91% |baidu data  |m175 ~/GN3Parser-beta/3.9.5-w-NN-POS  |
|Test     |Global    |84.33% |80.72% |baidu data  |m175 ~/GN3Parser-beta/3.9.5-w-NN-POS  |
|Dev      |Greedy    |79.22% |75.25% |3.9.9 baidu data  |gpu-no-1:~/GN3Parser-beta/3.9.9-w-baidu-data  |
|Test     |Greedy    |80.34% |76.24% |3.9.9 baidu data  |gpu-no-1:~/GN3Parser-beta/3.9.9-w-baidu-data  |
|Dev      |Greedy    |79.24% |75.36% |3.9.9.1 baidu data  |m175 ~/GN3Parser-beta/3.9.9.1-w-baidu-data  |
|Test     |Greedy    |79.81% |75.80% |3.9.9.1 baidu data  |m175 ~/GN3Parser-beta/3.9.9.1-w-baidu-data  |
|Dev      |Greedy    |79.24% |75.36% |3.9.9.2 baidu data  |m175 ~/GN3Parser-beta/3.9.9.2-w-baidu-data  |
|Test     |Greedy    |79.80% |75.80% |3.9.9.2 baidu data  |m175 ~/GN3Parser-beta/3.9.9.2-w-baidu-data  |

### 将GN3Parser修改成3个模型(2017-5-16)
因为联合模型的需要，我们尝试将原先的GN3Parser拆分为3个模型，分别进行Action的预测，总计分为以下三个模型：Atomic Model (POP\_ROOT, SHIFT, LEFT\_ARC, RIGHT\_ARC), Left\_label Model, Right\_label Model.

|__model__|__method__|__UAS__|__LAS__|__comments__|__position__|
|---------|----------|-------|-------|------------|------------|
|GN3Parser|Greedy    |--     |--     |Dev w correct feature list |m175 ~/GN3Parser-beta/debug-3.9.5 |
|GN3Parser|Greedy    |80.90% |76.94% |Dev w error feature list   |m175 ~/GN3Parser-beta/debug-3.9.6 |
|GN3Parser|Greedy    |--     |--     |Test w correct feature list|m175 ~/GN3Parser-beta/debug-3.9.5 |
|GN3Parser|Greedy    |81.00% |77.00% |Test w error feature list  |m175 ~/GN3Parser-beta/debug-3.9.6 |
|GN3Parser|Global    |84.45% |80.91% |Dev w correct feature list |m175 ~/GN3Parser-beta/debug-3.9.5 |
|GN3Parser|Global    |__84.76%__ |__81.12%__ |Test w correct feature list|m175 ~/GN3Parser-beta/debug-3.9.5 |
上面的打上横线的实验结果log被覆盖掉了～
### 对Label的特征模板的测试(2017-5-19)
在以前的实验中，我们发现一个貌似“错误”的现象：在我们将GN3Parser拆分成三个模型的过程中，因为没有考虑到Arc的影响，即在做完Arc操作之后(Left Arc, Right Arc)，栈里面的位置已经发生了变化，但是我们没有考虑到这个情况，如果还是沿用原来的特征抽取函数，那么就会出现抽取的特征并不是我们原来想要使用的特征。但是，结果表明，即便我们抽取“错误”的Label 特征模板，Parser的效果并没有很大的下降 (Greedy)。于是，我们便思考，这是为何？最有可能的就是，无论是“正确”的Label的特征模板，还是“错误”的特征模板，都包含了必要的信息for Label action，于是，我们尝试了精简特征模板，尝试了下列的实验：
![LabelFeatureTemplates](/images/GN3Parser/FeatureTemplates-Label.bmp)

|__model__|__method__|__UAS__|__LAS__|__comments__|__Position__|
|---------|----------|-------|-------|------------|------------|
|GN3Parser|Greedy    |80.72% |76.92% |Dev 1024\*1024 |m175 ~/GN3Parser-beta/3.9.7-1024  |
|GN3Parser|Greedy    |81.11% |77.30% |Test 1024\*1024 |m175 ~/GN3Parser-beta/3.9.7-1024  |
|GN3Parser|Greedy    |80.37% |76.57% |Dev 200\*200 |m175 ~/GN3Parser-beta/3.9.8-200  |
|GN3Parser|Greedy    |80.70% |76.76% |Test 200\*200 |m175 ~/GN3Parser-beta/3.9.8-200  |
|GN3Parser|Global    |84.10% |80.47% |Dev 1024\*1024 |gpu-no-1:~/GN3Parser-beta/3.9.8-1024  |
|GN3Parser|Global    |84.42% |80.71% |Test 1024\*1024 |gpu-no-1:~/GN3Parser-beta/3.9.8-1024  |
从实验的结果来看，我们“精简”之后的Label特征并没有导致明显的效果下降；但是，仍旧没有达到之前的水平！(2017-5-24)

### 特征的使用
特征的使用如下图所示,总计有48个特征.
![FeatureTemplates](/images/GN3Parser/FeatureTemplates.bmp)
### 统一的实验汇报
中文:(__已经达到了Google论文的结果__)
中文的全部数据都是projective的,因为在SyntaxNet上面,并没有能够重现Google论文结果,所以下面中文的数据中,并没有SyntaxNet的相关信息:
__Dev__:

|__model__|__method__|__position__|__UAS__|__LAS__|__comments__|
|---------|----------|------------|-------|-------|------------|
|GN3Parser |Greedy  |m175 ~/GN3Parser-beta/baidu-conll-09-chinese  |81.32%  |77.68%  |Greedy Dev w/o k best tags |
|GN3Parser |Greedy  |gpu-no-1:~/GN3Parser-beta/greedy\_v\_3.5      |81.24%  |77.10%  |Greedy Dev w k best tags   |
|GN3Parser |Global  |m175 ~/GN3Parser-beta/chinese-global-beam-32-fix-save-model  |84.07%  |80.54%  |Global Dev w/o k best tags     |
|GN3Parser |Global  |gpu-no-1:~/GN3Parser-beta/global\_v\_3.5                     |84.58%  |81.07%  |Global Dev w k best tags       |
__Test__:

|__model__|__method__|__position__|__UAS__|__LAS__|__comments__|
|---------|----------|------------|-------|-------|------------|
|GN3Parser|Greedy    |m175 ~/GN3Parser-beta/chinese-global-beam-32-fix-save-model |81.31%    |77.60%  |Greedy Test w/o k best tags      |
|GN3Parser|Greedy    |gpu-no-1:~/GN3Parser-beta/greedy\_v\_3.5                    |__81.72%__    |__78.14%__  |Greedy Test w/ k best tags       |
|Google论文|Greedy   |                                        |81.29%    |77.29%  |Greedy Test w/ k best tags       |
|GN3Parser|Global    |m175 ~/GN3Parser-beta/chinese-global-beam-32-fix-save-model |84.31%    |80.70%  |Global Test w/o k best tags      |
|GN3Parser|Global    |gpu-no-1:~/GN3Parser-beta/global\_v\_3.5                    |__84.60%__    |__81.02%__  |Global Test w/ k best tags       |
|Google论文|Global   |                                                            |__84.72%__    |80.85%  |Global Test w/ k best tags       |
中文补充的几个实验, beam size的影响
__w/o k best tags__

|__model__|__method__|__position__|__UAS__|__LAS__|__comments__|
|---------|----------|------------|-------|-------|------------|
|GN3Parser |Global  |m175 ~/GN3Parser-beta/chinese-global-beam-32-fix-save-model  |84.07%  |80.54%  |Global __Dev__ w/o k best tags     |
|GN3Parser |Global  |m172 ~/GN3Parser-beta/3.7-chinese-beam-__64__                |__84.33%__  |__80.82%__  |Global __Dev__ w/o k best tags     |
|GN3Parser |Global  |m175 ~/GN3Parser-beta/chinese-global-beam-32-fix-save-model  |84.31%  |80.70%  |Global __Test__ w/o k best tags    |
|GN3Parser |Global  |m172 ~/GN3Parser-beta/3.7-chinese-beam-__64__                |__84.87%__  |__81.17%__  |Global __Test__ w/o k best tags     |

__w k best tags__

|__model__|__method__|__position__|__UAS__|__LAS__|__comments__|
|---------|----------|------------|-------|-------|------------|
|GN3Parser|Global    |gpu-no-1:~/GN3Parser-beta/global\_v\_3.5                     |84.58%  |81.07%  |Global __Dev__ w k best tags, beam size=32      |
|GN3Parser|Global    |gpu-no-1:~/GN3Parser-beta/global\_v\_3.5                     |__84.60%__    |__81.02%__  |Global __Test__ w/ k best tags, beam size=32      |
|GN3Parser|Global    |gpu-no-1:~/GN3Parser-beta/global\_v\_3.5\_beam\_64           |84.45%  |81.04%  |Global __Dev__ w/ k best tags, beam size=64      |
|GN3Parser|Global    |gpu-no-1:~/GN3Parser-beta/global\_v\_3.5\_beam\_64           |__84.78%__    |__81.16%__  |Global __Test__ w/ k best tags, beam size=64      |

#### 探究正交分布初始化weight的影响(2017-4-12)
从下面的实验结果可以看出来, orthogonality weight于我们的GN3Parser并没有什么用处.因为Global过程已经和parameter没有什么关系,所以,这里,我们仅仅跑了Greedy的实验.

|__model__|__method__|__position__|__UAS__|__LAS__|__comments__|
|---------|----------|------------|-------|-------|------------|
|GN3Parser|Greedy    |m175 ~/GN3Parser-beta/orthogonality-3.9 |80.99% |77.40% |greedy __dev__ w/o k best tags  |
|GN3Parser|Greedy    |m175 ~/GN3Parser-beta/baidu-conll-09-chinese  |81.32%  |77.68%  |Greedy Dev w/o k best tags |
|GN3Parser|Greedy    |m175 ~/GN3Parser-beta/orthogonality-3.9 |81.16% |77.42% |greedy __test__ w/o k best tags |
|GN3Parser|Greedy    |m175 ~/GN3Parser-beta/chinese-global-beam-32-fix-save-model |81.31%    |77.60%  |Greedy Test w/o k best tags      |

英文:
英文数据:

|                       |__train__|__dev__|__test__|
|-----------------------|---------|-------|--------|
|Total sentences        |39832    |1700   |2416    |
|Projective sentences   |39793    |1697   |2415    |
|NonProjective sentences|39       |3      |1       |
下面的数据中,train,dev 采用projective部分; test 采用total数据
__Dev数据集的效果__:

|__position__|__UAS__|__LAS__|__comments__|
|------------|-------|-------|------------|
|m173 ~/GN3Parser-beta/baidu-1024-div-batch-size-eta-0.01  |93.10%  |90.90%  |Greedy Dev    |
|gpu-no-1:~/SyntaxNet/models/syntaxnet/nndep\_baidu\_data\_1024\_w\_embedding\_baidu\_config |92.90% |--  |Greedy Dev |
|m173 ~/GN3Parser-beta/baidu-1024-div-batch-size-eta-0.01  |94.22%  |92.05%  |Global Dev    |
|gpu-no-1:~/SyntaxNet/models/syntaxnet/nndep\_baidu\_data\_1024\_w\_embedding\_baidu\_config |94.19% |--  |Global Dev |
__Test数据集的效果__:

|__position__|__UAS__|__LAS__|__comments__|
|------------|-------|-------|------------|
|gpu-no-1:~/GN3Parser-beta/baidu-1024-div-batch-size-eta-0.01        |92.78%  |90.64%  |Greedy Test; 代码,模型copy from 173上述目录,173太挤了! |
|gpu-no-1:~/SyntaxNet/models/syntaxnet/nndep\_baidu\_data\_1024\_w\_embedding\_baidu\_config |92.59% |--  |Greedy Test |
|Google论文                                                |92.95%  |91.02%  |       |
|gpu-no-1:~/GN3Parser-beta/baidu-1024-div-batch-size-eta-0.01        |93.79%  |91.74%  |Global Test; 代码,模型copy from 173上述目录,173太挤了! |
|gpu-no-1:~/SyntaxNet/models/syntaxnet/nndep\_baidu\_data\_1024\_w\_embedding\_baidu\_config |93.76% |--  |Global Test |
|Google论文                                                |94.61%  |92.79%  |       |

### 实验数据记录
在工程的进行过程中，会记录实验数据
important: *SyntaxNet的测试数据都是不包含标点的*
有些实验已经移到当前目录的bak文件夹下面了!
#### 2017-3-28
除了昨日发现的config文件中的一个毛病,我们还发现了数据中的一个问题,虽说是使用k best tags, 但是语料中的CRF模型给出句子的TOP-K词性序列中,每一个word可能含有5个k best tags,但是它们的POS是一样的.也就是说,在原来我写的代码里面,在最后面的prob会覆盖掉最前面的prob,也就是prob最大的那一个,昨天修正了这个错误,在提取k best tags的时候,仅仅保留相同POS的第一个prob,也就是score最高的那一个.并且做了Greedy的实验;但是由此也会产生一些问题,如"5 best tags",如果当前word包含相同的POS,那么也就不能满足"5"这个条件.

|__position__|__UAS__|__comments__|
|------------|-------|------------|
|gpu-no-1:~/GN3Parser-beta/greedy\_v\_3.5  |81.24%  |with SyntaxNet config and option|

#### 2017-3-27
SyntaxNet英文实验: decay\_steps: 4500(greedy); 150(global)

GN3Parser:在修复了bug(config文件中没有配置decay steps)之后,貌似k best tags还是没有什么用啊...

|__w/l best tags__|__w/o k best tags__|
|-----------------|-------------------|
|83.80%           |83.94%             |

目前最好的两个Global实验,分别为包含k best tags和不包含k best tags

|__position__|__UAS__|__use k best tags__|__comments__|
|------------|-------|-------------------|------------|
|m175 ~/GN3Parser-beta/exp-src-3.0-global-83.94  |83.94%  |No  |   |
|m175 ~/GN3Parser-beta/test-version-3.4-global   |83.80%  |Yes |   |

#### 2017-3-26
应该找到bug,在什么地方了.一个很小的,几乎被忽略的地方,decay\_steps的初始化,因为decay\_steps被初始化为-1,需要从config文件中读取相对应的配置(应该为300, 或者4400);但是,没有初始化的话,就会在模拟退火部分,只要一个batch结束,就会更新eta = eta * 0.96,因为一次迭代,大约需要5000个batch,而1000个batch之后,eta就只剩下__1.49e-19__这么多了,几乎等于0,所以到后面,UAS就不会变化了!
#### 2017-3-24
使用百度提供的配置,尝试进行GN3Parser中文 *greedy*的调参

eta=0.15

|__position__|__batch size__|__UAS__|__comment__|
|------------|--------------|-------|-----------|
|gpu-no-1:~/GN3Parser-beta/test-src-v3.4  |20  |77.52%   |    |
|gpu-no-1:~/GN3Parser-beta/test-src-v3.4-batch-5 |5   |0.55%  |17次epoch都是0.55,应该涨不上去了 |
|gpu-no-1:~/GN3Parser-beta/test-src-v3.4-batch-10  |10   |30.37% |6次epoch都是30.37%   |
|gpu-no-1:~/GN3Parser-beta/test-src-v3.4-batch-40  |40   |80.07% |     |
|gpu-no-1:~/GN3Parser-beta/test-src-v3.4-batch-50  |50   |80.07% |30次迭代无增长结束     |



#### 2017-3-23
记录一下最近的一个bug的调试过程(UAS一直保持不变)
1. debug1, 一次batch之后就evaluate 10个sentence, UAS是变化的.
2. debug2, 一次batch之后就evaluate all sentences, UAS也是变化的.
3. 在将use k best放到config的过程中,发现了一个bug,就顺便又找到了一个bug,get\_k\_best\_tag\_id 中漏掉了return id???,利用bug找bug!~
#### 2017-3-22
总结一下最近做的实验:

GN3Parser 有无k best tags 特征的UAS对比, 所有的word都包含,包括标点.

|__w/ k best tags__|__w/o k best tags__|
|------------------|-------------------|
|81.25%            |81.32%             |

#### 2017-3-21
昨儿个拿到了百度提供的二进制word embedding,今儿个便在SyntaxNet上跑个对比试验,看看实验结果如何.

__SyntaxNet__

|__position__|__UAS__|__commments__|
|------------|-------|-------------|
|gpu-no-1:~/SyntaxNet/models/syntaxnet/nndep\_baidu\_chinese |79.08%   |local, without embedding     |
|gpu-no-1:~/SyntaxNet/models/syntaxnet/nndep\_baidu\_chinese\_w\_embedding |79.67%   |local, with embedding     |
奇怪的是,即使SyntaxNet没有使用k best tags,UAS是不是也有点低了.

__GN3Parser__

|__position__|__UAS__|__comments__|
|------------|-------|------------|
|m175 ~/GN3Parser-beta/test-src-v3.0 |81.25%  |greedy w k best tags  |
|m175 ~/GN3Parser-beta/test-src-v3.2 |        |global w k best tags  |

#### 2017-3-16
今天的主要事情就是折騰我这Linux系统了.
首先汇报一下GN3Parser的进展:(__以下的有关中文实验的数据都是不准确的,排除了label为UNK的word__)
__Greedy__

|__position__|__UAS__|
|------------|-------|
|m175 ~/GN3Parser-beta/baidu-conll-09-chinese  |__81.32%__   |
|论文的结果                                    |81.29%   |
greedy的结果目前来看就没有问题了,等待global的结果,没有添加k-best tags.

greedy结果已经出来了,目前结果都不行:

|__position__|__eta__|__UAS__|__comment__|
|------------|-------|-------|-----------|
|m175 ~/GN3Parser-beta/baidu-conll-09-chinese-global-eta-0.01 |0.01  |83.39%  |  |
|m175 ~/GN3Parser-beta/baidu-conll-09-chinese-global  |0.03 |__83.72%__  |   |
|m175 ~/GN3Parser-beta/baidu-conll-09-chinese-global-eta-0.05 |0.05  |83.07% |  |

现在来讨论一下今天折腾系统的事情:
1. 早上来的时候,就发现Linux系统的搜狗输入法崩掉了,没法输入中文了,这个对于我来说是致命的.必须把它修好
2. 因为搜狗输入法和fcitix有关系,于是我就重新安装了fciti和搜狗输入法,悲剧的是,输入法没有安装好,还把系统的System setting给弄没了.
3. 不能忍,继续到网上查找资料尝试解决问题,但是已经不记得自己干了什么,系统就重新启动了,然后就登录不进去了,报错"failed to start session"!根本登录不了系统.
4. 中午到~,一上午白费了,打算放弃了,都在往服务器上面备份数据了;打算再尝试一会,尝试失败就重新安装系统.
5. 于是乎,又查找了大量的资料,绝大数的网上的东西我都试过了,根本没有用;就连最基本的"apt-get update"都会报错:"error 'nodata'"的错误;后来看到网上说,可能是proxy的问题啥的,最后,我的解决方案是,换源,换成教育网的源,这样居然就能update了?再把ubuntu-desktop,ubuntu-session等软件给安装回来.心累
6. 晚上顺便就重新倒腾了一下Linux的主题,给自己一点新鲜感.最后,重新安装了搜狗输入法,居然一下子就好了?不明觉厉!还安装了QQ.  :)
#### 2017-3-14
*从3-10到现在的所有实验,数据,全部是错误的!!!*
原因如下:
1. 因为一开始拿到百度的数据,我就首先测试了一下包不包含none projective的数据(因为之前英文数据包含),但是,貌似因为编码的问题,我发现数据拿到linux上面显示全部都是乱码;
2. 于是便在windows上面的"记事本"软件打开,并且保存为UTF-8编码格式的,再上传到服务器进行进一步的处理;
3. 可是,后来发现,虽然中文显示正常了,在处理id 和 head的时候,编写的脚本会出错,显示不能将得到的字符串转换成int类型;
4. 于是,后来想办法解决,什么添加decode('utf-8')全部没有用,后来我就把int()给去掉了,不要求强制转换为int类型,程序正常执行,心想着以为程序就ok了.同时输出了很多的projective数据和None projective数据,如下表格所示.
5. 鬼使神差的是,我今天还拿了一个none projective的句子进行人工检查,居然还被我看成了none projective的??可能是因为看得比较急躁.
6. 但是,结果明显是不对的,李老师也说应该全部都是projective的!
7. 又到师姐那边去拿了以前的旧代码进行测试;发现李老师给的数据,全部都是projective的.发现目前的代码就和旧代码几乎一样,除了"__int()__";但是李老师给的数据和百度提供的数据明显label和head都是一样的?可能因为李老师的数据是UTF8编码格式的,而百度的数据是由ANSI转换成UTF-8的,可能有不同,所以脚本才不能处理百度的数据
8. 最后,师姐想到,会不会是转换格式的问题?于是就用Notepad进行了格式转换,"UTF-8",发现还是那个问题,int()这一步骤过不了!,于是,在转换为"无BOM"的UTF-8,代码就可以了,因为编码问题,浪费了我三天时间..


今天做实验的时候,突然发现,当初提取句子的时候,用的脚本没有提示有多少句是projective,多少句是non projective,今天添加了几行代码,发现了很严重的事情,百度提供的数据中含有大量的non projective数据:

|__Corpus__|__Total__|__Projective__|__Non projective__|
|----------|---------|--------------|------------------|
|train     |22277    |4003          |18274             |
|dev       |1762     |300           |1462              |
|test      |2556     |445           |2111              |

受到之前实验的影响,以为Global实验的第一次结果一定会比greedy的来的高,所以之前kill掉了很多实验.事实证明,这一次的中文实验并不是这样,之后会增加的比较快的.

batch: 10

|__position__|__eta__|__UAS in epoch 1__|__UAS__|__comment__|
|------------|---------|------------------|-------|-----------|
|m175 ~/GN3Parser-beta/baidu-chinese-global-eta-0.05      |0.05     |80.53%    |83.18%  |        |
|gpu-no-1:~/GN3Parser-beta/baidu-chinese-global-eta-0.03  |0.03     |81.93%    |83.88%  |        |
|gpu-no-1:~/GN3Parser-beta/baidu-chinese-global-eta-0.01  |0.01     |80.48%    |83.43%  |        |
|m175 ~/GN3Parser-beta/baidu-chinese-global-eta-0.008     |0.008    |79.98%    |82.83%  |        |

eta: 0.03

|__position__|__batch__|__UAS in epoch 1__|__UAS__|__comment__|
|------------|---------|------------------|-------|-----------|
|m175 ~/GN3Parser-beta/baidu-chinese-global-batch-5    |5        |80.93%            |82.68% |                            |
|gpu-no-1:~/GN3Parser-beta/baidu-chinese-global        |10       |81.53%            |83.88% |高峰过后,稳定在83           |
|m175 ~/GN3Parser-beta/baidu-chinese-global-batch-20   |20       |80.93%            |83.23% |                            |
|m175 ~/GN3Parser-beta/baidu-chinese-global            |30       |81.08%            |83.88% |高峰过后,稳定在82           |

#### 2017-3-13
中文的数据已经过来了,正在做一些数据准备的工作:
1. embedding的准备,从百度提供的embedding,形成我们Parser所需要使用的embedding
2. 判断中文数据是否包含交叉,全部都不包含;ANSI to utf-8
3. SytaxNet的评价包含标点

先看看Greedy的效果,包含标点

|__model__|__eta__|__batch__|__decay__|__momentum__|__UAS__|__comment__|
|---------|-------|---------|---------|------------|-------|-----------|
|SyntaxNet|0.08   |32       |4500     |0.9         |73.92% |其他的都是12.56%,明显这个参数不对,后来全部都是12.56% |
|SyntaxNet|0.15   |5        |300      |0.9         |13.86% |几乎还有其他的都是12.56%,很奇怪?*百度提供的配置选择之一* |
|GN3Parser|0.08   |32       |4400     |0.9         |82.48% |           |

Global, GN3Parser, 1 epoch:

|__model__|__hyper parameters__|__UAS in epoch 1__|__UAS__|__comment__|
|---------|--------------------|------------------|-------|-----------|
|GN3Parser|eta=0.03            |81.38%            |       |killed     |
|GN3Parser|eta=0.1             |33.1%             |       |killed     |
|GN3Parser|eta=0.01            |81.93%            |       |killed partial hot started|
|GN3Parser|eta=0.008           |80.78%            |       |killed parital hot started|
|GN3Parser|eta=0.03            |82.68%            |       |killed partial hot started|
|GN3Parser|eta=0.07            |17.76%            |       |killed parital hot started|
|GN3Parser|eta=0.05            |80.53%            |       |killed parital hot started|
|GN3Parser|eta=0.03, batch=3   |77.03%            |       |killed parital hot started|
|GN3Parser|eta=0.03, batch=8   |82.68%            |       |killed partial hot started|
|GN3Parser|eta=0.03, batch=20  |82.83%            |       |killed parital hot started|
|GN3Parser|eta=0.03, batch=30  |81.08%            |83.88% |                          |

#### 2017-3-10
今天完成了GN3Parser添加MKL.
完成MKL的过程略有曲折,稍加记录:
MKL的工作其实在之前就已经进行了,当时仅仅是从intel的[相关网址](https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor/)上,填写相应的信息,配置需要的编译信息.配置完成之后,尝试过直接加到Makefile里面,就当时来看,确实速度进步了不少.但是最近发现,好像greedy的时候,CPU的占用率一直就只是100%,按道理不应该只有这么一点CPU,于是尝试了各种方法,尝试正确配置MKL,直接的效果就是CPU占用率能够达到500%(人为设定的5个线程).
1. 因为接触MKL,因为dynet里面配置了MKL,效果挺好,而dynet使用的CMake,而不是Makefile;于是我又修改GN3Parser代码结构,编写相应的CMakeLists,折腾了一些时间,无果.
2. 后来怀疑是不是LibN3L的问题,于是自己写了一个小的测试程序test.h,结果是可以的,可以利用MKL进行加速.
3. 再后来就怀疑是不是多线程的问题,于是去掉Greedy里面的多线程,发现还是不行,无果.
4. 后来没办法,釜底抽薪.copy一份GN3Parser,注释掉main.cpp里面的所有的include,加入test.一步步放出里面的include,一步步加入test进行测试.后来在BatchState里面的forward里面也加入test,发现程序居然可以跑了,greedy显示的是500%CPU,很兴奋(OK)
5. 需要查找原因,于是就尝试将include进来的test进行注释,删除编译,发现,通不过了,再后来重新加回test,可是!!!居然MKL又没有用了,又只剩下了100%CPU.很奇怪
6. 最后,将代码copy到m175里面,发现可以编译,MKL可以使用.......GPU服务器有点问题啊再后来,加回多线程仍旧可以跑,任务完成.但是test模块暂时还要保留.不想深究原因,应该编译顺序的原因.头疼

现在将GN3Parser各版本的速度和SyntaxNet进行对比.

|__model__|__greedy speed__|__global speed__|__comment__|
|---------|----------------|----------------|-----------|
|GN3Parser|5000 batch/ 45min|1w sentence / 9h                |greedy多线程,300%CPU vs global多线程,800%CPU      |
|GN3Parser-w-BatchedComputing|5000 batch/ 30min    |1w sentence / 2.5h |greedy单线程, 100%CPU vs global多线程, 800%CPU     |
|GN3Parser-w-BatchedComputing-w-MKL|5000 batch / 23min  |1w sentence / 1h |greedy单线程, 500%CPU vs global多线程, 2700%CPU   |
|SyntaxNet |5000 batch / 2min        |1w sentence / 12.5min        |greedy多线程1500%CPU vs global多线程2600%CPU          |

*备注:GN3Parser的CPU数均为峰值*
#### 2017-3-7
Softmax Layer加上了bias
大矩阵计算的代码已经修改出来了,现在做实验验证UAS以及速度的变化

|__position__|__UAS__|__comment__|
|------------|-------|-----------|
|m173 ~/GN3Parser-beta/baidu-test-v2.5  |93.04%       |speed: 6min/1000batch |

Global: 全部热启动 and 部分热启动

|__position__|__UAS__|__comment__|
|------------|-------|-----------|
|m175 ~/GN3Parser-beta/baidu-test-v2.5         |93.91%       |param来自于93.01% Greedy    |
|m175 ~/GN3Parser-beta/baidu-test-v2.5-eta-0.02|5%           |eta设置0.02,UAS直接崩掉了?      |
|m173 ~/GN3Parser-beta/baidu-test-v2.5-without-softmax-param  |94.24%     |部分热启动        |
大矩阵重现了,没有问题.
#### 2017-3-1
祝自己新的一个月快乐!
今天晚间终于搞定了大矩阵的计算.有两个原因,有一个乌龙~
1. 今天午间调试程序的时候,发现有的word id居然是小于1的,然后经过排查,发现,vector &lt; state\_instance &gt;的指针使用的不对,这一点C++基本知识还需加强,头疼.
2. 但是虽然找到了一个这个原因,跑实验的时候,发现结果还是不对.然后就试着不将一个batch的input组合成大矩阵,试着就使用一个input来进行实验,这样子就和原来的v1版本的代码一致了,但是结果仍然不好.
3. 所以我干脆重新回到v1版本的代码,从v1版本一点一点修改.首先,我去掉了precomputation,ok,试验没有问题!,但是当我尝试去掉原来因为precomputation用的各种LinearLookupNode,BNode的时候,需要直接使用一个UniNode作为hidden layer1,但是,问题来了,实验仍然通不过!我就找师姐来看代码,发现改动的地方很少,就修改了hidden layer1的实现方式,结果确实相差很大.排查bug,失败~
4. 纠结了挺长一段时间,无果.尝试调参吧,后来发现,调参有用!(eta = 0.01)即可?我表示很矛盾,不应该相同的网络,需要使用不同的参数啊.后来,只能想到一个原因,v1版本的h1实现的时候,每一个w的维度是[word\_dim, hidden layer size], 但是改成大矩阵的时候,就是[all\_word\_dim, hidden layer size],虽然使用的是相同的初始化值,但是矩阵的大小不一样,随机初始化初来的矩阵相差也比较大??
5. 正在跑1024的实验!从目前来看,速度确实有点变快,30分钟应该就能跑完一次迭代.5000batch.没有多线程,没有MKL(结果正常!开心~)
真的觉得,每次看实验结果之前需要拜个佛:)

#### 2017-2-28
找出了尝试大矩阵运算中的一个bug,因为原先使用precomputation的原因,evaluate的时候,使用的还是原来的parameters,第一个隐含层的参数和现在Uniparams不同,不能混合使用,需要修改.
又出现了UAS不更新的问题!
#### 2017-2-27
SyntaxNet尝试使用全部greedy parameter参数失败,会报错,出现inf错误
#### 2017-2-25
Global结果已经出来,最好的一个__94.22%__,已经和SyntaxNet齐平.(完工!)
:)
#### 2017-2-24
1. 统一了老版本的pre computation和新版本的实现方式:
> * 老版本,传入的是一个batch中,应该被计算pre computation的word idx
> * 新版本,根据word idx来选择是否需要进行计算
2. 根据实验表明,pre computation计算出来的值val(0, 0)会出现 < 1e-3 的情况,故修改pre computation中判断条件为1e-5.
3. 在evaluate函数里面,将greedy和global的分别测试融合了.

#### 2017-2-23
每天早晨来实验室看实验结果就跟拜佛似得,怀着无比虔诚的心,诶,实验结果好了~GN3Parser的Global效果第一次迭代挺好的,__93.99%__,这个实验用的是 / batch\_size .
还有几点比较奇怪的:

> * 我们的GPU服务器竟然跑的比173要慢,173已经跑完1次epoch又17000句子,GPU服务器竟然只跑了22000句子?!
> * mkl优化又大约1000句子1h20min,优化前大约1.7h

#### 2017-2-22
因为GN3Parser实在是太慢,so,探究加速方面的事情.对*Eigen进行加速*(打开OMP: 两个1024\*1024的矩阵进行相乘10次,未加速*86.75s*, 加速*25.23s*)
__OMP__
此种方式通过打开OMP,从而打开Eigen的多线程运算.但是,如果服务器的CPU核数太少,则不能用这种方法,会导致GN3Parser多线程出问题!(libgomp: Thread creation failed: Resource temporarily unavailable)
*其实可以设置线程数:)*
目前在171服务器上面测试GN3Parser加速后的greedy水准!
未加速:7s   10个batch
加速后:32s  10个batch  <font color='green'>???what?</font>
__MKL__
没法从dynet配置中获取经验!!!
矩阵的乘法编译通不过??(Google了很多资料,头疼~)
编译完成之后,运行程序又出现了新的bug:

> * parameter 13 was incorrect on entry to dgemm

解决之后:
*OpenMP threading* 5s 10个batch 10个线程 | 4s 10个batch 20个线程 | 5s或者4s 10个batch __5个线程__ (实际上用不了这么多),可能是我们的GPU服务器不行?!
*Sequential threading* 5s或者4s(较多) 10个batch __5个线程__
*TBB threading* 编译不成功:/usr/bin/ld: cannot find -ltbb

#### 2017-2-21
既然Greedy达到了SyntaxNet的水平,下面就开始Global的实验

|__position__|__hyper parameters__|__Global__|__comment__|
|------------|--------------------|----------|-----------|
|gpu-no-1:~/GN3Parser-beta/baidu-1024-baidu-config-div-t-beam-16            |eta=0.03            |          |baidu config, div total \_t, beam=16 |
|gpu-no-1:~/GN3Parser-beta/baidu-1024-baidu-config-div-t-beam-64            |eta=0.03            |          |baidu config, div total \_t, beam=64 |
|gpu-no-1:~/GN3Parser-beta/baidu-1024-baidu-config-div-t-beam-16-eta-0.2    |eta=0.2             |          |baidu config, div total \_t, beam=16 |
|m173 ~/GN3Parser-beta/baidu-1024-div-batch-size-eta-0.01            |eta=0.01            |__94.22%__ |baidu config, div batch size(8), beam=16|
|m173 ~/GN3Parser-beta/baidu-1024-div-batch-size-eta-0.02            |eta=0.02            |__94.18%__ |baidu config, div batch size(8), beam=16|
|m173 ~/GN3Parser-beta/baidu-1024-div-batch-size-eta-0.03            |eta=0.03            |kill |baidu config, div batch size(8), beam=16|

#### 2017-2-20
下午发现,原来的实验都是200\*200的......补充了一个实验,首先跑Greedy,1024\*1024

|__position__|__hyper parameters__|__greedy__|__global__|__comment__|
|------------|--------------------|----------|----------|-----------|
|m175 ~/GN3Parser-beta/baidu-hidden-size-1024-baidu-config|eta=0.08, |93.09% | |baidu config |
|m175 ~/GN3Parser-beta/baidu-hidden-size-1024       |eta=0.1,    |93.10%    |    |    |

#### 2017-2-19
Global div \_t

|__hyper parameters__|__global uas in epoch 1__|__end__|
|--------------------|-------------------------|-------|
|eta=0.03, reg=1e-5, |92.46%                   |don't care~       |
|eta=0.2, reg=1e-5   |93.43%                   |93.65% |

#### 2017-2-18
补充的几个实验

|__hyper parameter__|__global UAS in epoch 1__|
|-------------------|-------------------------|
|eta=0.08, reg=1e-5, momen=0.9, beam=64|93.07%|
|eta=0.1                               |93.19%|
|eta=0.15                              |93.32%|
|eta=0.2                               |__93.34%__|

one\_batch\_state\_count那边可能有问题,state\_count是指的一串state呢?还是beam里面所有的state?更新的时候是否都是beam里面最后一个State?!
#### 2017-2-17
从epoch 1的实验结果来看,百度的数据在Global上可能需要调参,不能够直接沿用百度的配置

Baidu config(greedy-model.bin form 92.58%)

|__hyper parameter__|__global uas in first epoch__|
|-------------------|-----------------------------|
|eta=0.03, reg=1e-4, momen=0.9, beam=64|92.22%    |
|eta=0.03, reg=1e-5, momen=0.9, beam=64|92.55%    |
|eta=0.03, reg=1e-7, momen=0.9,        |92.48%    |
|eta=0.005, reg=1e-5,                  |91.16%    |

My config(greedy-model.bin from 92.64%)

|__hyper parameter__|__global uas in first epoch__|
|-------------------|-----------------------------|
|eta=0.03, reg=1e-4, momen=0.9, beam=64|92.58%    |
|eta=0.02, reg=1e-5, momen=0.9, beam=64|92.22%    |
|eta=0.02,                     beam=128|92.37%    |
|eta=0.1,                              |__93.19%__|
|eta=0.001,                            |89.45%    |
个人认为有可能是beam的大小的问题,当初调试周浩数据的时候,就是增加beam从16到64,UAS一下子就增加上去了.所以又增加了一组实验.
Get!应该调整eta的大小,往大的调整

#### 2017-2-16
GN3Parser的一些最新实验
python处理了embedding,将oov使用正态分布随机化了embedding.(baidu.embedding.total.for.train)

|__position__|__greedy__|__global__|__comment__|
|------------|----------|----------|-----------|
|m172 ~/GN3Parser-beta/baidu-momentum-0.9         |92.51%  |    |eta=0.1, regularization=1e-5, momentum=0.9|
|m173 ~/GN3Parser-beta/baidu-momentum-0.9-w-total-train-embedding|__92.64%__  |   |配置同上,但是用了python处理过的embedding    |
|m172 ~/GN3Parser-beta/baidu-data-baidu-config    |92.40%  |    |eta=0.08, 1e-5, 0.9|
|m173 ~/GN3Parser-beta/baidu-data-baidu-config-w-total-train-embedding|92.58%  |   |配置同上,但是用了python处理过的embedding   |

从下面的这个图片我们可以看出来,GN3Parser的收敛速度和SyntaxNet几乎差不多.且SyntaxNet有一个比较奇怪的地方,开始几次迭代的UAS都在16.3%
![GN3Parser vs SyntaxNet](/images/GN3Parser/greedy)

就目前看,GN3Parser的global过程进展并不顺利,可能参数又没有设置得好?7h一次迭代完成(时间有点长)
#### 2017-2-15
SyntaxNet终于复现了Google的结果

|__Eval__|__greedy__|__global__|__comment__|
|--------|----------|----------|-----------|
|SyntaxNet|92.90%   |94.21%    |SyntaxNet自带的评价, eval\_global的时候, syntaxnet显示eval metric只有94.19?|
|eval-UAS.py|92.97% |94.26%    |完全按照label列的punct来计算的           |
|eval.pl |92.66%    |93.99%    |eval.pl应该是识别不了-LRB-之类的word的       |

words.gz里面的"##"代表ROOT
#### 2017-2-14
GN3Parser实现的eval过程中是否包含标点有问题:
 eval.pl分母:35368
 GN3Parser(c自带的接口ispunct)分母:35363;且GN3Parser测试出来的结果比eval.pl测试出来的结果少0.3%
 Python实现(自己写的)分母:35363
 GN3Parser词性列表的实现方法,分母:36152
 SyntaxNet分母:35431
#### 2017-2-13
今天比较了周浩的数据和百度的数据,发现words有如下差别.
有1585个单词,百度的数据是"\*/\*",而周浩包含了转义符"\"
实现了GN3Prarser中,可以通过配置文件,要求评价包含不包含标点.现在默认不包含

做了几个实验,看看正则化因子GN3Parser的影响

|__position__|__greedy__|
|------------|-----------|
|m175 ~/GN3Parser-beta/baidu-regularization-1e-2 |kill  |
|m175 ~/GN3Parser-beta/baidu-regularization-1e-3 |kill  |
|m175 ~/GN3Parser-beta/baidu-regularization-1e-4 |91.43%  |
|m172 ~/GN3Parser-beta/baidu-regularization-1e-5 |91.40%  |
|m172 ~/GN3Parser-beta/baidu-regularization-1e-6 |90.73%  |

上面的结果都是GN3Parser测试出来的结果
#### 2017-2-11
最近在使用百度的数据尝试重现Google的结果
SyntaxNet:

|__position__|__greedy__|__global__|__comment__|
|------------|----------|----------|-----------|
|gpu-no-1:~/SyntaxNet/models/syntaxnet/nndep\_baidu\_data\_1024\_w\_embedding |92.64% | 93.89%| 使用了embedding,但是这一版本并没有修改百度说的embedding bug|
|gpu-no-1:~/SyntaxNet/models/syntaxnet/nndep\_baidu\_data\_1024\_w\_embedding\_baidu\_config |__92.90%__  |  |  |

GN3Parser:
鉴于GN3Parser的Greedy在百度的数据上效果并没有那么好(90.68%,包含标点,UAS,没有使用embedding),现在尝试调参,看看是不是参数的问题.
和SyntaxNet相比,GN3Parser在没有使用embedding的情况下,最起码要达到91.00%才行.

|__position__|__greedy__|__comment__|
|------------|----------|-----------|
|m175 ~/GN3Parser-beta/baidu-eta-0.2|90.52%  |        |
|m175 ~/GN3Parser-beta/baidu-eta-0.15|?       |超过20次:26%|
|m175 ~/GN3Parser-beta/baidu-eta-0.1|__90.73%__   |         |
|m175 ~/GN3Parser-beta/baidu-eta-0.05|90.50%  |         |
|m175 ~/GN3Parser-beta/baidu-eta-0.03|90.49%  |         |
|m175 ~/GN3Parser-beta/baidu-eta-0.01|89.34%  |         |
|m172 ~/GN3Parser-beta/baidu-eta-0.1-embedding |90.74%  | |
|m172 ~/GN3Parser-beta/baidu-eta-0.08-embedding|90.58%  | |
|m172 ~/GN3Parser-beta/baidu-eta-0.05-embedding|90.61%  | |

> * 今天发现了一个问题,百度的数据拿我们的embedding来跑实验,竟然还有141个OOV,也就是说,和周浩的数据又有不同!连words都不同?
> * 我们发现加了embedding,并没有明显让UAS上升,有如下猜想解释:embedding只有2/3的数据有,其他的只不过是随机初始化的,跟百度提供的没法比

#### 2017-2-10
今天主要完成了两项工作:

> * 搞明白了为啥当hidden layer size为1024\*1024的时候,SyntaxNet的结果一直都是16.33%?为啥呢,因为SyntaxNet可能训练的比较慢,等上差不多9次迭代之后,eval metric就增加了.可是很奇怪的是,GN3Parser就没有这个问题
> * 解决了global训练的时候,存在着内存问题.经过排查,是State.h里面new了一个can\_apply\_idx,但是忘记delete了:),一个教训,谨记!

#### 2017-2-9
尝试在SyntaxNet中加入embedding,复现Google的论文结果.
根据百度提供的bug,修改reader\_ops.cc中"+ 3" -> "+ 2"(修改之后,从日志上并不能看出什么差别)
UAS:

|__position__|__greedy__|__global__|
|------------|----------|----------|
|SyntaxNet amax:~/TensorFlow/models/syntaxnet/nndep\_baidu\_data |91.94  |  |
|SyntaxNet amax:~/TensorFlow/models/syntaxnet/nndep\_baidu\_data\_w\_embedding|92.38  |93.70  |
|GN3Parser    |   |   |

如果,单纯的修改hidden layer neuron number为1024的话,SyntaxNet的greedy效果奇差:16.33%

#### 2017-2-8
年后第一天来实验室,首先整理一下前几天的工作:
采用百度的数据,分别采用SyntaxNet & GN3Parser进行测试比较,结果如下:

|__position(已经舍弃)__|__greedy__|__global__|
|------------|-------------|-------------|
|amax:~/TensorFlow/models/syntaxnet/nndep\_baidu\_data(SyntaxNet)|92.05%            |93.39          |
|m175 ~/GN3Parser-beta/merge-globally-data-baidu    |90.55%(实验已经被覆盖,因为此数据包含交叉弧数据)            |?          |
几点说明:

> * 都没有使用pretrained embedding
> * 其中,syntaxnet中,百度的数据会产生一个projectivized-training-corpus,而且不能够被替换为百度提供的training-corpus,替换的化,SyntaxNet的global过程会报错,无法完成?是否因为百度的数据是包含交叉的?
> * 我们的GN3Parser在global过程中会报错!(use-all-pre-trained-embeddings版本代码)

*经过验证,百度提供的数据确实存在着包含交叉弧的数据,总计1160行(包含空白行)*

#### 2017-1-22
zhouhao-data: SyntaxNet, global, UAS:__93.37%__(不含标点)
#### 2017-1-20这一次为什么又会是26%呢?
今天尝试用src-r10跑一下beam search,突然就想起来,relu的双隐层从来就没有好过!
于是我就采用tanh激活函数,代替了relu,发现是可以的,没有问题.努力调参中...

#### 2017-1-18-融合greedy和global的功能
从昨天晚间开始融合两部分的代码,遇到了如下问题:
1. greedy和global的pre computation的初始化方式以及使用方式不一致
#### 2017-1-17-完善Parameter averaging功能

> * 添加保存averaging parameter功能(完成)
> * 添加是否在eval的采用parameter averaging功能,选项(完成)
> * 优化SparseParam的update功能,不再使用整个矩阵的更新,更新成update哪一row,就只计算哪一row


#### 2017-1-16-加入了parameter averaging功能
在昨天的工作基础上,加入了parameter averaging功能,基于谷歌的第一篇论文:
中心思想就是eval的时候,使用的是averaging parameter
公式如下:
$$
\overline{\theta\_{t}} = \alpha\_t\overline{\theta\_{t-1}} + (1 - \alpha\_t) \theta\_t
$$
这里的$\overline{\theta\_{t}}$是t步update之后的shadow\_variable,即averaging parameter
我们看了tensorflow的实现,加入了min操作:
min(decay, (1 + num\_steps) / (10 + num\_steps))

实验:

|__position__|__best UAS__|__commments__|
|------------|------------|-------------|
|m172 ~/GN3Parser-beta/greedy-state-parameter-averaging-eta-0.1|  91.42|参数设置和下面的91.55一致   |
|m172 ~/GN3Parser-beta/greedy-state-parameter-averaging-eta-0.08-mo-0.85|__91.51__  |eta 0.08 momentum 0.85, SyntaxNet的默认配置|
|m172 ~/GN3Parser-beta/greedy-state-parameter-averaging-eta-0.08-91.51-verify|__91.64__|参数同91.51,为了查看随机化的影响|
|m172 ~/GN3Parser-beta/greedy-state-parameter-averaging-eta-verify-91.51|90.91|参数同91.51,使用的是fix-bug代码|

*结论*:(2017-1-19)
已经各跑了两组实验,发现fix-bug之后的实验结果普遍低于没有fix-bug之后的,经排查,可能的原因有如下两种情况:
1. SparseParam更新gradient的时候,就不能够做优化(已经确认,是这个原因2017-1-20)
2. 是不是\_g\_global\_label\_num\_no\_null这个参数的问题,can\_apply\_idx?的长度原因?(不是这个原因)

*解释*:因为使用的Momentum Optimizer,accum的存在,使得SparseParam就是不能使用indexer来进行优化!(2017-1-20)


利用__百度__提供的数据进行的实验(train:open)(2017-1-17)

|__position__|__best UAS__|__comments__|
|------------|------------|------------|
|m175 ~/GN3Parser-beta/greedy-state-parameter-averaging-eta-0.08-mo-0.85 |90.67  |使用了parameter averaging, 参数配置同上91.51|
|m175 ~/GN3Parser-beta/greedy-state-greedy-eta-0.1-baidu  |90.64  |没有使用parameter averaging,参数配置同下91.55,(91.65, no punct) |
|m175 ~/GN3Parser-beta/greedy-state-greedy-eta-0.08-baidu |90.71  |没有使用parameter averaging,参数配置同上91.51,(91.69, no punct) |

遇到的问题:
1. 今天在做百度实验的时候,以上的三个实验发现UAS一直都是26%,是以前经常遇到的一个错误,经过排查代码发现.
我们在FeatureConfig.h的文件中写死了LABEL\_NUM=12,为了做百度的实验,暂时就修改为45.以后就修改这一参数,根据目标语料来动态赋值.
2. 不能测试parameter averaging的UAS,因为averaging parameter没有保存.

#### 使用syntaxnet以及Github上推荐的参数配置,跑了一遍baidu提供数据的代码
实验:

|__position__|__best UAS__|__comments__|
|------------|------------|------------|
|amax:~/TensorFlow/models/syntaxnet/nndep\_baidu\_data | 91.99|m171  |

#### 2017-1-15-实验整理
SyntaxNet在周浩的数据上,greedy,使用默认参数配置,eval metric:92.48%
修正了GN3Parser,放弃了融合beam的功能,实现了基于state的batch的train过程.记录实验数据如下:

|__position__|__best UAS__|__comments__|
|------------|------------|------------|
|m175 ~/GN3Parser-beta/greedy-state-greedy-eta-0.1 |__91.55__  |eta=0.1, lambda=1e-4, momentum=0.9|
|m175 ~/GN3Parser-beta/greedy-state-greedy-eta-0.05|91.25  |eta=0.05, ...同上 |
|m175 ~/GN3Parser-beta/greedy-state-greedy-eta-0.05-lambda-1e-6|90.64 |eta=0.05, lamdba=1e-6, 同上|
|m175 ~/GN3Parser-beta/greedy-state-greedy-eta-0.01|90.61  |eta=0.01, ...同上 |

#### 正则化实验整理
正则化的实验：参数的更新方式选择Momentum Optimizer, tensorflow 实现方式;三个Embedding的初始化方式还都是LibN3L自带的,暂时没有切换到正态分布

|__position__|__best UAS__|__comments__|
|------------|------------|------------|
|gpu-no-1:~/GN3Parser-beta/greedy-no-regularization  |90.26        |No regularization            |
|gpu-no-1:~/GN3Parser-beta/greedy-w-regularization-reg-1e-4 |__90.65__   |with regularization;lambda 1e-4     |
|gpu-no-1:~/GN3Parser-beta/greedy-w-regularization-reg-1e-4-batch-1|85.30  |parameter same with 90.65, batch is 1|
|gpu-no-1:~/GN3Parser-beta/greedy-w-regularization   |90.22        |with regularization;lambda 1e-5     |
|gpu-no-1:~/GN3Parser-beta/greedy-w-regularization-reg-1e-7 |90.11 |with regularization;lambda 1e-7     |
|gpu-no-1:~/GN3Parser-beta/greedy-w-regularization-normalization-embedding|90.03|with regularization;normal embedding|

#### Momentum Optimizer实验整理
Momentum Optimizer: 梯度更新方式的实验,本组实验总共探究了两个实现方式
tensorflow实现方式:
Sebastian博客给出的方式:

|__position__|__best UAS__|__comments__|
|------------|------------|------------|
|gpu-no-1:~/GN3Parser-beta/greedy-momentum-from-sebbastian      |90.22         |Momentum Optimizer, From sebastian |
|gpu-no-1:~/GN3Parser-beta/greedy-w-regularization   |90.22        |with regularization;lambda 1e-5     |

#### Words POS Labels Embedding 初始化方式比较
word pos labels embedding的初始化方法比较:
uniform分布:(使用了norm2one)
normalization分布:(没有使用norm2one)

|__position__|__best UAS__|__comments__|
|------------|------------|------------|
|gpu-no-1:~/GN3Parser-beta/greedy-normalization-embedding-words-pos-label |89.79|参数设置和90.65那个一样 |
|gpu-no-1:~/GN3Parser-beta/greedy-normalization-embedding-words-pos-label-w-norm2one | 89.82|使用了norm2one,其他参数一样|
|gpu-no-1:~/GN3Parser-beta/greedy-normalization-embedding-words-pos-label-w-norm2one-eta-0.4| 88.98 |使用了norm2one,eta=0.4|
|gpu-no-1:~/GN3Parser-beta/greedy-normalization-embedding-words-pos-label-eta-0.4 |90.06 |eta=0.4,其他参数一样|
|gpu-no-1:~/GN3Parser-beta/greedy-uniform-embedding-words-pos-label   |90.15   |参数设置和90.65模型一样   |

从结果中,可以看出来,当使用了normalization分布的时候,还测试了eta为0.4的情况

#### 2016-10-30-实验整理
|__position__|__parameters__|__current best accuracy/epoch__|
|-------------------------------------------------------------|----------------|------------------|
|m176:~/GN3Parser-beta/experiment-ml-batch-1        |max likelihood beam 16 batch 1|88.56(iter 11) |
|m176:~/GN3Parser-beta/experiment-ml-beam-32-batch-20|ml beam 32 batch 20          |90.66(iter 12) |
|m176:~/GN3Parser-beta/experiment-ml-h-500-batch-20-beam-16|ml beam 16 hidden 500 batch 20|89.09(iter 7) |

*跑了一个第一版本的precomputation实验，ml，用来对比实现第二版本的速度以及准确率*
m176:~/GN3Parser-pre-computation/example-maxlikelihood-beam-32-batch-20
Accuracy:__90.99(iter 19)__
可能因为是batch设置为20的原因，进一步的优化并没有明显的速度优势，第一次迭代的速度都是13min左右。
以前有过一次实验，当batch设置为200的时候，就能够看出明显的优势，第二版本的速度比第一版本快2倍左右。

#### 2016-10-29-实验整理
目前最新的代码，融合了greedy search，可供选择的loss：max margin, max likelihood损耗函数。GN3Parser-beta
#####LN3Parser: greedy search
parameters: beam size=##, dropout=0.0, hidden layer neuron number=200, embedding dim=50, thread num=30

batch size=5: m172 /home/yzhang/GN3Parser-greedy-search/example-dim50-batch5 第10次迭代所用时间：<font color=blue>22:31:22 - 22:39:46 = 8min24s</font>
batch size=20: m172 /home/yzhang/GN3Parser-greedy-search/example-dim50-batch20 第10次迭代所用时间：<font color=blue>10:42:38 - 10:46:29 = 3min51s</font>
batch size=200: m172 /home/yzhang/GN3Parser-greedy-search/example-dim50-batch200 第10次迭代所用时间：<font color=blue>23:08:48 - 23:10:06 = 1min18s</font>

|__epoch__|__batch size=5 Accuracy__|__batch size=20 Accuracy__|__batch size=200 Accuracy__|
|---------|-------------------------|--------------------------|---------------------------|
|1        |84.54                    |82.56                     |64.51                      |
|10       |88.85                    |88.49                     |84.69                      |
|20       |88.78/89.18(iter 16)     |88.42/88.82(iter 16)      |87.01                      |
|STOP     |89.18(iter 16)           |88.82(iter 16)            |88.15(iter 39)             |

#####GN3Parser: max likelihood
parameters: beam size=16, dropout=0.0, hidden layer neuron number=200, embedding dim=50, thread num=30

batch size=5: m175 ~/GN3Parser-pre-computation/example-maxlikelihood-batch-5 第10次迭代所用时间：<font color=blue>17:42:55 - 16:53:00 = 49min55s</font>
batch size=20: m175 ~/GN3Parser-pre-computation/example-maxlikelihood-batch-20 第10次迭代所用时间：<font color=blue>12:15:20 - 12:30:46 = 15min26s</font>
batch size=200: m172 ~/GN3Parser-pre-computation/example-maxlikelihood-batch-200 第10次迭代所用时间：<font color=blue>15:48:40 - 15:58:29 = 9min49s</font>

|__epoch__|__batch size=5 Accuracy__|__batch size=20 Accuracy__|__batch size=200 Accuracy__|
|---------|-------------------------|--------------------------|---------------------------|
|1        |81.70                    |80.07                     |54.78                      |
|10       |89.02                    |88.52                     |85.55                      |
|20       |88.51/89.43(iter 14)     |87.90/88.70(iter 19)      |86.54/87.50(iter 18)       |
|STOP     |89.43(iter 14)           |88.70(iter 19)            |87.71(iter 26)             |

##### GN3Parser MM VS ML
parameters: beam size=16, dropout=0.0, hidden layer neuron number=200, embedding dim=50, thread num=30

MM: m173 ~/GN3Parser-pre-computation/example-maxmargin-batch-5 第10次迭代所用时间：<font color=blue>03:01:07 - 03:16:46 = 15min39s</font>
ML: m175 ~/GN3Parser-pre-computation/example-maxlikelihood-batch-5 第10次迭代所用时间：<font color=blue>17:42:55 - 16:53:00 = 49min55s</font>

|__epoch__|__ML Accuracy__|__MM Accuracy__|
|---------|---------------|---------------|
|1        |81.70          |74.21          |
|10       |89.02          |79.55          |
|20       |88.51/89.43(iter 14)|80.00/80.65(iter 19)|
|STOP     |89.43(iter 14) |83.53(iter 122)     |

#### 加了pre computation 和不加pre computation的速度对比
统一查看第10次迭代的时间
参数配置：beam size=16,

|__method__|__thread num__|__batch__|__word embedding size__|__hidden layer neuron number__|
|----------|--------------|---------|-----------------------|------------------------------|
|pre computation|15       |200      |50                     |200                           |
|no pre computation|15    |200      |50                     |200                           |

|__method__|__begin time__|__end time__|__UAS__|__end UAS__|
|----------|--------------|------------|-------|-----------|
|pre computation|09:04:33 |09:09:31    |81.46% |84.47%/113 |
|no pre computation|11:21:11|11:43:12  |59.46% |--         |
总的来说速度快了: 5min/22min = 4
准确率差这么多？

#### 利用目前的代码实现greedy search，with pre computation
#### 加了pre computation 和不加pre computation的速度对比
统一查看第10次迭代的时间
参数配置：beam size=16,

|__method__|__thread num__|__batch__|__word embedding size__|__hidden layer neuron number__|
|----------|--------------|---------|-----------------------|------------------------------|
|pre computation|15       |200      |50                     |200                           |
|no pre computation|15    |200      |50                     |200                           |

|__method__|__begin time__|__end time__|__UAS__|__end UAS__|
|----------|--------------|------------|-------|-----------|
|pre computation|09:04:33 |09:09:31    |81.46% |84.47%/113 |
|no pre computation|11:21:11|11:43:12  |59.46% |--         |
总的来说速度快了: 5min/22min = 4
准确率差这么多？

#### 利用目前的代码实现greedy search，with pre computation
|__epoch__|__UAS__|
|---------|-------|
|19       |88.15  |

#### 中文实验数据
beam\_size=16, batch\_size=20, threads=15, word embedding dim=50, dropout=0.2
##### max margin loss:
|__epoch__|__Accuracy__|
|---------|------------|
|1        |60.02       |
|10       |68.01       |
|19       |70.45       |
|23       |71.16       |
|46       |72.38       |
|64       |73.02       |
|91       |73.21       |
|112      |72.36/73.21 |
|156      |74.01       |
|168      |74.16       |
|182      |72.59/73.16 |
|240      |74.61       |
第10次迭代所花时间：59min

##### max log likelihood:
|__epoch__|__Accuracy__|
|---------|------------|
|1        |33.86       |
|9        |50.78       |
|17       |51.63       |
|22       |52.69       |
|41       |54.06       |
|70       |54.92       |
|75       |55.33       |
|139      |53.48/55.33 |
|159      |53.48/55.33 |
|176 STOP |50.07/55.33 |
第10次迭代所花时间：24min

#### 英文实验数据
##### dropout = 0.2, threads=15
|__epoch__|__beam size__|__hidden layer neuron number__|__batch size__|__word embedding dim__|__Accuracy/Best Accuracy__|
|---------|-------------|------------------------------|--------------|----------------------|--------------------------|
|1        |16           |200                           |15            |300                   |75.65                     |
|10       |             |                              |              |                      |82.52                     |
|19       |             |                              |              |                      |82.82                     |
|24       |             |                              |              |                      |83.29                     |
|28       |             |                              |              |                      |82.47/83.29               |
|29       |             |                              |              |                      |83.44                     |
|36       |             |                              |              |                      |83.04/83.44               |
|48       |             |                              |              |                      |82.15/83.44               |
第10次迭代所花时间：6h20min


|__epoch__|__beam size__|__hidden layer neuron number__|__batch size__|__word embedding dim__|__Accuracy/Best Accuracy__|
|---------|-------------|------------------------------|--------------|----------------------|--------------------------|
|1        |16           |1024                          |15            |300                   |79.05                     |
|6        |             |                              |              |                      |83.39/83.45               |
|7        |             |                              |              |                      |84.49                     |
|9        |             |                              |              |                      |84.80                     |
|10       |             |                              |              |                      |84.87                     |
|12       |             |                              |              |                      |85.59                     |
|15       |             |                              |              |                      |85.89                     |
第9次迭代所花时间：24h...
第10次迭代结果还没有出来


server: 172, threads=30

|__epoch__|__beam size__|__hidden layer neuron number__|__batch size__|__word embedding dim__|__Accuracy/Best Accuracy__|
|---------|-------------|------------------------------|--------------|----------------------|--------------------------|
|1        |64           |200                           |2000          |50                    |26.67                     |
|20       |             |                              |              |                      |62.53/67.77               |
|32       |             |                              |              |                      |79.53                     |
|38       |             |                              |              |                      |81.48                     |
|51       |             |                              |              |                      |82.52                     |
|58       |             |                              |              |                      |80.87/82.52               |
|60       |             |                              |              |                      |82.53                     |
|68       |             |                              |              |                      |82.73                     |
人为掐断
第10次迭代所花时间：50min

##### google loss
dropout = 0.0， 时间：2016-10-20 07:30:22，（纯属猜测，batch设置为1试玩的）, threads=30

|__epoch__|__beam size__|__hidden layer neuron number__|__batch size__|__word embedding dim__|__Accuracy/Best Accuracy__|
|---------|-------------|------------------------------|--------------|----------------------|--------------------------|
|1        |16           |200                           |1             |50                    |54.25                     |
|6        |             |                              |              |                      |63.08                     |
|24       |             |                              |              |                      |67.39                     |
|31       |             |                              |              |                      |67.88                     |
|48       |             |                              |              |                      |61.67/67.88               |
|76       |             |                              |              |                      |58.30/67.88               |
|94       |             |                              |              |                      |59.28/67.88               |
|97       |             |                              |              |                      |68.31                     |
|179      |             |                              |              |                      |53.42/68.31               |
STOP
第10次迭代所花时间：53min

dropout = 0.2， 时间：2016-10-19 18:18:32, threads=30

|__epoch__|__beam size__|__hidden layer neuron number__|__batch size__|__word embedding dim__|__Accuracy/Best Accuracy__|
|---------|-------------|------------------------------|--------------|----------------------|--------------------------|
|1        |16           |200                           |50            |50                    |56.79                     |
|64       |             |                              |              |                      |72.45                     |
|78       |             |                              |              |                      |72.67                     |
|111      |             |                              |              |                      |72.78                     |
|168      |             |                              |              |                      |69.69/72.78               |
|212 STOP |             |                              |              |                      |68.18/72.78               |
第10次迭代所花时间：20min

### bug
#### 为什么Node的lock都是50？而不是0？
因为在函数中声明定义了PAddNode，在函数中将这个PAddNode加入到了Graph中，当函数结束的时候，PAddNode会被释放掉。
所以lock才会是一个乱七八糟的数字.

#### 找到了为什么精度只有0.1了
因为有一段代码设置了输出的时候的precision，实际上的精度是没有问题的。
```
basic-features/FeatureDictionary.cpp:73:				<< "\" " << fixed << setprecision(1) << endl;>>>>>>>>
```
