---
title: Pytorch-DeepATT
date: 2018-06-25 18:02:57
password: suda_kiro
message: Contact Kiro to get the key.
tags: [SRL]
toc: true
---
# 简介
DeepSRL 这一篇工作将停滞了十年的 SRL工作往前推了一下，我已经在之前的工作中，将其重现了出来，并且在这个基础之上做了一些工作，探索如何应用句法信息来继续提升 SRL的效果，并以此写了一篇论文，虽然不知道能不能中；
在 DeepSRL这一个基于 Highway LSTM的工作之后，DeepATT这一个利用 Self-Attention的工作又一次大幅度的推进了 SRL的效果。所以为了补全我们的工作，我最近有花了近一个月的时间重现了 tensorflow版本的 DeepATT，最终的效果基本一致，虽然模型上有所区别。

# Baseline重现的结果
实验的数据是 CoNLL-2005

| __Model__    | __Dev P__| __Dev R__| __Dev F1__| __Test WSJ P__| __Test WSJ R__| __Test WSJ F1__|  __Test Brown P__| __Test Brown R__| __Test Brown F1__| __Test Both F1__|
|--------------|----------|----------|-----------|---------------|---------------|----------------|------------------|-----------------|------------------|-----------------|
| __DeepATT(论文结果)__  |82.6      |83.6     |83.1       |84.5           |85.2           |84.8            |73.5              |74.6             |74.1              |83.4             |
| Our(re-impl) |82.8      |83.2		 |83.3      |84.7           |85.1           |84.9            |72.7              |73.1             |72.9              |83.3             |
| Our(re-impl timing) |82.6    |83.8	|83.2      |84.9     |85.5           |85.2            |72.8         |73.6           |73.2         |83.6             |
关于我们重现的一些细节：
1. batching的策略应该有所不同，源码是使用的 tensorflow的函数 bucket_by_sequence_length，因为我对 tensorflow并不熟悉，所以只能按照源码的输出日志写一个类似的 batching模块
2. 论文采用的 timing，而我采用的 position encoding，而且该 embedding在模型中的位置和 DeepATT是不同的。
3. 我采用保存在 Dev上最好的结果，最后发现是 __Layer=8__在 Dev上的表现是最好的，而不是 Layer=10。（此处的表现指的是加入了 Viter Decoding，而论文则指出 Viter Decoding是没有作用的;虽然在未加入 Viterbi的时候，Layer=10层的效果更好）

# 记录利用句法进行实验的具体效果
| __Model__    | __Dev P__| __Dev R__| __Dev F1__| __Test WSJ P__| __Test WSJ R__| __Test WSJ F1__|  __Test Brown P__| __Test Brown R__| __Test Brown F1__| __Test Both F1__|
|--------------|----------|----------|-----------|---------------|---------------|----------------|------------------|-----------------|------------------|-----------------|
|syntactic label (hidden layer=8) |83.0      |83.4      |83.2       |84.2           |84.7           |84.4          |73.2              |72.5             |72.8              |82.9             |
|syntactic label (hidden layer=10) kiro@ubuntu:~/Work/SRL/Pytorch-DeepATT/exp-w-syntactic-label|83.3     |83.7      |83.5      |84.6    |84.9     |84.7       |73.2              |72.9             |73.0              |83.2             |
|syntactic label (hidden layer=10, label embedding=100, head=6, timing) qrxia@n141:/data/qrxia/Pytorch-DeepATT/exp-w-syntactic-label-6-head-timing |83.2 |83.8 |83.5 |85.0 |85.4 |85.2 |74.3 |73.4 |73.8 |83.7 |
|syntactic label (hidden layer=10, label embedding=100, head=12) qrxia@n141:/data/qrxia/Pytorch-DeepATT/exp-w-syntactic-label-12-head |82.4 |82.9 |82.6 |84.1 |84.5 |84.5 |73.6 |72.5 |73.1 |82.9 |
|syntactic label (hidden layer=10, label embedding=120) qrxia@n141:/data/qrxia/Pytorch-DeepATT/exp-w-syntactic-label-120 |82.7      |83.5      |83.1      |84.8    |85.0     |84.9     |72.7             |72.4              |72.6              |83.3             |
|syntactic label (hidden layer=10, label embedding=120, FFN hidden=320*4) qrxia@n171:~/Pytorch-DeepATT/exp-w-syntactic-label-120/ |83.3 |83.4 |83.4 |85.1 |85.0 |85.1 |73.2 |72.4 |72.8 |83.4 |
|syntactic label (hidden layer=10, label embedding=120, gold syntax) qrxia@n141:/data/qrxia/Pytorch-DeepATT/exp-w-syntactic-label-120-gold-syntax |84.0      |84.7      |84.3      |85.8    |86.2     |86.0     |76.7    |76.3   |76.5      |84.7             |
|syntactic label (hidden layer=10, TPF) kiro@ubuntu:~/Work/SRL/Pytorch-DeepATT/exp-w-tpf/  |82.9  |83.4 |83.2 |84.6 |84.8 |84.7 |73.8 |73.9 |73.9 |83.2 |
