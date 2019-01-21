title: LSTM
date: 2016-5-18 19:52:21
tags: [neural-network]
mathjax: true
---
# 简介
长短时间记忆神经网络（LSTM），适用于序列标注问题。
# 公式推导
[我的公式推导](/documents/lstm.pdf)
<!--more-->
# 损失函数
在LSTM中，我使用的损失函数是max margin损失函数：

定义得分函数：
$$s(sentence^{(1:n)}, y^{(1:n)}, \\theta)=\\sum\_{t=1}^n\\mathbf{A}\_{y^{t-1}y^{t}}+\\mathbf{y}\_{y^t}^{t}$$

其中，$sentence^{(1:n)}$是输入的句子，$y^{(1:n)}$是相对应的词性序列，$\\mathbf{A}\_{iy}$是从词性$i\\in T$到词性$j\\in T$的转移概率。$\\mathbf{y}\_{y^t}^{t}$是词性$y^t$的得分、其中$\\mathbf{y}^t$是从神经网络里面计算出的得分，$\\theta$表示所有的超参。

定义margin：
$$\\Delta(y\_i, \\hat{y})=\sum\_t^n\\eta\mathbf{1}\\left [{y\_i^{(t)}\\neq\\hat{y}^{(t)}}\\right ]$$
$n$是这个句子的长度，$\\eta$是margin loss discount。

定义margin loss function：
$$loss(o^n)=max\_{\\hat{y}\_1^n}(s({\\hat{y}}\_1^n)+\\Delta(\\hat{y}\_i^n, y\_1^n))-s(y\_1^n)$$
其中，$\\hat{y}\_1^n$是一个预测出来的词性序列。
# 实验过程记录
今天在本机调试程序的时候，发现了一个很好玩的现象：
![multi-cpu.png](/images/lstm/multi-cpu.png)
这里面的cpu竟然是那么多！不是服务器上面的100%，不明觉厉！记录现象，目前无解。
## 张梅山老师的代码研究
[张梅山老师的LSTMPOSTagging](https://github.com/SUTDNLP/NNPOSTagging)
张梅山老师的代码使用的是ctb5数据，与我平常使用的conll格式的数据不同，里面包含了char feature, sparse feature。以下的数据都是从epoch = 0开始，均是使用的默认参数。
### 默认工程的准确率
|__epoch__|__best accuracy__|
|---------|-----------------|
|5        |93.95%           |
[日志文件](/documents/lstm/log.txt)
### 去除tanh layre的准确率
|__epoch__|__best accuracy__|
|---------|-----------------|
|3        |94.24%           |
[日志文件](/documents/lstm/log_no_tanh_layer.txt)
准确率咋还上来了呢？随机化的影响？不能这么大吧。。
### 再去掉right lstm的准确率
|__epoch__|__best accuracy__|
|---------|-----------------|
|3        |94.12%           |
[日志文件](/documents/lstm/log_no_right_lstm.txt)
准确率也还可以，貌似双向的lstm并没有很大的提升。
### 再去掉char embedding的准确率
|__epoch__|__best accuracy__|
|---------|-----------------|
|7        |92.07%           |
[日志文件](/documents/lstm/log_no_right_tanh_char.txt)
## 使用LSTM对ctb7数据进行词性标注准确率记录
### 使用双向的lstm进行词性标注，使用char embedding，tanh layer
|__epoch__|__best accuracy__|
|---------|-----------------|
|4        |94.33%           |
[log文件](/documents/lstm/log_ctb7.txt)
### 仅仅使用char embedding的准确率
|__epoch__|__best accuracy__|
|---------|-----------------|
|5        |94.50%           |
[log文件](/documents/lstm/log_just_with_char.txt)
### 不使用char embedding的准确率
|__epoch__|__best accuracy__|
|---------|-----------------|
|7        |92.69%           |
[log文件](/documents/lstm/log_no_tanh_right_char_ctb7.txt)
### 使用word2vec训练得到的word embedding进行模型的训练
|__epoch__|__best aacuracy__|
|---------|-----------------|
|4        |94.66%           |
[log文件](/documents/lstm/log_with_word_embedding.txt)
### 使用训练好的模型进行test数据集的测试
#### 使用word2vec训练得到Word Embedding
|__epoch__|__Accuracy(dev/test)__|
|---------|----------------------|
|3        |94.66%/94.31%         |
[log文件](/documents/lstm/log_with_word_embedding.txt)
#### 使用随机初始化得到Word Embedding
|__epoch__|__Accuracy(dev/test)__|
|---------|----------------------|
|5        |94.50%/94.33%         |
[log文件](/documents/lstm/log_with_test.txt)
