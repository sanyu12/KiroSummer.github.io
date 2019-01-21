---
title: AMR
date: 2017-07-10 21:29:22
tags: [AMR]
---
# 概述
从现在开始，开启我的新方向、新征程！AMR Parsing！
# 问题的一些基本概念
<!--more-->
## AMR Graph
AMR Graph is a __rooted__, __directed__, __acyclic__ graph.
### 数据样例
![amr data file](/images/amr/GraphStructureFile.png)
![amr graph](/images/amr/sample.bmp)
### 为什么需要alignment
因为在AMR的数据中，我们仅仅只有一个pair，一个sentence以及其对应的AMR Graph。所以，从第一个任务(concept identification)来看，我们需要知道which span of words invoke which concept fragments in the amr graph。这个时候，就需要一个AMR Aligner的存在。
[Alignment的格式](https://github.com/jflanigan/jamr/blob/Semeval-2016/docs/Alignment_Format.md)
alignment是以AMR graph为基准的(顺序什么的，重要吗？)
评价alignment是需要人工的Gold alignment的，JAMR的Aligner也不能够得到100%的F值。
### 利用stanford pos tagger进行词性标注
```
    java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -sentenceDelimiter newline -tokenize false -textFile ../../full-w-pos/amr-release-1.0-training-alignment-one-sentence-a-line.txt > amr-release-1.0-training-alignment-w-pos.txt
```
在处理词性的时候，发现stanford-postagger，会过度分词，例如
```
    Freedom_NN of_IN speech_NN \_CD thought_NN ,_, if_IN people_NNS express_VBP a_DT view_NN somewhat_RB different_JJ than_IN the_DT traditional_JJ view_NN
```
1. 其中的 speech\thought 就被分析成了 speech \ thought 三个词，然后标成了三个词性。
2. etc._NN ._. ,多分析出来了一个英文句号。。。

人工修复
#### 记录MKL的有时候没有使用
在敲完代码后，使用和GN3Parser同样的Makefile进行编译，发现eigen居然利用不了MKL，后来有相当一段长的时间使用不了MKL。到后来发现新的服务器（126.172, 126.173）都不能够利用MKL，最后实在没办法，讲代码copy到m175上进行编译和运行，发现可以完美的运行和利用MKL；然后再将m175上面的代码和实验copy到新服务器上，make clean + make，发现同样可以使用MKL，玄学！
### KAMR可能需要继续进行修改的一些地方
1. agenda的初始化长度，设置太小可能导致内存错误
2. 特征部分仍然需要继续修改

### JAMR的一些明显错误
#### concept的分割重复
句子id：nw.wsj_0003.17，node：0.1.0.2.0.1.0.0.0.1.0.0
12-30 和 29-30 重复
这个问题将会导致两个问题：
1. 在给定“正确”的concept用以产生AMR Graph的时候，会出现重复的node。
2. 在做Concept Identification的时候，会产生一些标签上的错误！对于标签上面的错误，将错就错？

## 实验结果
初步smath F值:50%
#### 第一阶段代码的初步说明：
1. v1.4.4， Concept Identification，利用Train进行训练，并且进行测试，产生predicted concepts。
2. v1.3.2， Relation Identification，利用Train以及正确的Concept进行模型的训练，产生模型。
3. v1.3.3， 在v1.3.2的基础之上修改了读取文件的格式，利用1.3.2训练好的模型进行Relation Identification。
