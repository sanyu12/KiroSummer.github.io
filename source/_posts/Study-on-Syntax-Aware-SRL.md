---
title: Study-on-Syntax-Aware-SRL
date: 2018-09-19 14:27:18
password: suda_kiro
tags:
---
# 简介
记录一下 Syntax-aware SRL的之后一些工作
<!--more-->
## Sub-word for SRL 2018-10-3
### extract data 
* Extract data from bllip.MIRA.DuDu.FULL.conll.out and generate sentences in a line format.
* Merge the CoNLL-05 SRL Train data into the bllip data, and employ the subword-nmt to generate the bpt.vocab
* Employ the subword-nmt to generate the CoNLL-05 train, dev, and test data's bpe format word sentences.

bllip corpus contains 1796379 sentences
```bash
subword-nmt learn-bpe -s 32000 < merge.bllip.conll05srl-train.txt > bpe.vocab.txt
subword-nmt apply-bpe -c bpe.vocab.txt < conll05.train.txt.srl.sen.txt > conll05.train.bpe.txt
```

## GCN相关 2018-9-19
今天发现了一个非常奇怪的问题，在 GCN加入 gate之后，速度一下子由 24s -> 46s（同样的数据跑了 20次）。感觉很奇怪，记录一下这个问题，看看能不能找到原因。
__ 原因__: 因为 gate需要 h进行计算，然而，最原始的输出也需要 h进行计算，最后的输出是由 gate*输出 因为反向传播，所以更新会非常慢。
*告诉为父，主语孩儿你的语义标签是什么？告诉自己，我的语义标签是什么？告诉孩儿，父亲你的语义标签是什么？*

记录一下关于 GCN的一些实验：

| __Path__| __说明__| __Dev FScore__| __iter__|
|---------|---------|---------------|---------|
|n126:...exp-GCN-on-top-of-BiLSTM| 第一个版本的 GCN，采用 syn label num个 W*x + b| 76.78%| 245 kill| 
|n126:...exp-GCN-w-dropout-on-top-of-BiLSTM|在 line1 模型的基础上加上了 dropout| 79.69%| 456 done(79.10 / 245 iter)| 
|n126:...exp-GCN-w-simplified-weights-on-top-of-BiLSTM| 在 line2基础上，采用 3 个w, syn label num个 + b| 80.12%| 432 done| 
|n126:...exp-GCN-w-Gating-on-top-of-BiLSTM |在 line1 模型的基础上加上了 Gating | 77.04%| 246 done(76.68 / 245 iter)| 

## Tree-GRU相关 2018-9-28
记录一下关于 Tree-GRU的一些实验：

| __Path__| __说明__| __Dev FScore__| __iter__|
|---------|---------|---------------|---------|
|n141:...exp-TreeGRU-on-top-of-BiLSTM| 第一个版本的 Tree-GRU， 直接将 BiLSTM Output作为 Tree-GRU的输入，无任何其他操作 |75.55 | 443 kill|
|n126:...exp-TreeGRU-v1-on-top-of-BiLSTM|将 BiLSTM Output以树的形式相加作为 Softmax的输入|78.69 | 475 done|
|n141:...exp-TreeGRU-v2-on-top-of-BiLSTM|将 BiLSTM Output和 Tree-GRU Output作为 Softmax的输入|78.24 | 475 kill|
|n141:...exp-TreeGRU-v3-on-top-of-BiLSTM|将 BiLSTM Output, Tree-GRU Output和 syn label embedding作为 Softmax的输入|77.54 |366 done|

## SDP related 2018-10-11
Some experiments about the SDPs

| __Path__| __说明__| __Dev FScore__| __iter__|
|---------|---------|---------------|---------|
|n141:...exp-SDP| fix the bug: concate(left, left) | 80.71%| 484 |


## 研究了一下模型的计算时间
### 数据的预处理时间
__改进前__
台式机1080Ti: 1000次 所花时间大约在 40s左右，可以接受
服务器1080Ti: 1000次 1min31s (90s)，时间是否太长？
__改进后__
无需数据预处理
### 模型的运行时间
__改进前__
台式机1080Ti: 100次 所花时间大约在 44s左右(45% ~ 90% Util)；1000次也就是 440s，大约8min；400 steps: 4min13s; *一次迭代*：9min07s, 500次迭代大约3天多一点点跑完
服务器1080Ti: 100次 1min28s（88s）(39% Util)；
__改进后__
台式机1080Ti: *一次迭代*：7min31s 500次迭代大约2天半跑完

### 同样的程序，为什么服务器的 GPU Util会这么低？
是否如网上所言，数据的预处理影响到了模型的速度？

