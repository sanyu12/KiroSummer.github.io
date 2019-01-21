title: RNN学习
date: 2016-5-31 21:09:34
tags: [neural-network, RNN]
mathjax: true
---
# RNN学习记录
因为RNN比较适合序列标注的问题，所以在以前我已经将普通的NN应用到词性标注的问题上，最近一段时间打算应用一下RNN，看看效果如何。ANN的最好的效果是93.19%，比线性模型好了一点点，希望应用RNN会得到更好的结果。
# Forward Pass过程分析
<!--more-->
因为我目前使用的神经网络只有三层：input layer, hidden layer, output layer。根据我所看的资料，RNN的cycle只需要应用到hidden layer上。因此前向传播的公式会有所变化：
ANN的hidden layer的公式：
$$
z^l = w^l\* a^{l-1} + b^l \\\
a^l = \sigma(z^l)
$$
RNN的hidden layer的公式有所变化：
$$
z\_t^l = w^l\* a^{l-1} + b^l + w^{r}\* a\_{t-1}^{l} \\\
a\_t^l = \sigma(z\_t^l)
$$
在这里，我们使用$w^{r}$表示从前一个时间传播过来的weight，$a\_{t-1}^l$表示前一个时间的hidden layer的激活值。
output layer的相关公式不变化。
# Backward Pass过程分析
## output layer
输出层的错误值：$\sigma^L=a^L-y$
输出层的biases梯度：$\frac{\partial C}{\partial b^L}=\sigma^L=a^L-y$
输出层的weights梯度：$\frac{\partial C}{\partial w^L}=\sigma^L\times {a^{L-1}}^T=(a^L-y)\times {a^{L-1}}^T$ *这里的* $\times$ *操作是两个矩阵相乘*
## hidden layer
隐藏层的错误值：$\sigma^l=\left({w^l}^T\times\sigma^{l+1} + {w^{r}}^T\times\sigma^{l, t+1}\right)\odot \tanh ({z^l})'$  *这里的* $\odot$ *表示的是按位乘法*
隐藏层的biases梯度：$\frac{\partial C}{\partial b^l}=\sigma^l$
隐藏层的weights梯度：$\frac{\partial C}{\partial w^l}=\sigma^l\times {a^{l-1}}^T$
隐藏层的recurrent\_weights梯度：$\frac{\partial C}{\partial w^r}=\sigma^l\times {a^{l, t-l}}^T$
## input layer
输入层的x的梯度:$\frac{\partial C}{\partial x}={w^1}^T\times \sigma^1$
# RNN词性标注数据记录
## 步长eta的调参
hidden layer neuron number = 150, mini batch size = 2, lambda = 1e-2, oov-rato = 0.2

|__eta__|__best accuracy/best epoch__|
|-------|----------|
|0.05   |92.57%/34 |
|0.01   |93.08%/36 |
|0.005  |93.10%/86 |
|0.001  |92.77%/470|
## 正则化因子的调参lambda
hidden layer neuron number = 150, mini batch size = 2, eta = 1e-2, oov-ratio = 0.2

|__lambda__|__best accuracy/best epoch__|
|----------|------------|
|1e-1      |93.00%/52   |
|1e-2      |93.04%/54   |
|1e-3      |93.04%/44   |
|1e-4      |93.11%/62   |
|1e-5      |93.10%/64   |
|1e-6      |93.01%/80   |
|1e-7      |93.13%/62   |
## mini batch size的调参
hidden layer neuron number = 150, eta = 1e-2, lambda = 1e-7, oov-ratio = 0.2

|__mini batch size__|__best accuracy/best epoch__|
|-----------|---------------|
|1          |93.21%/72      |
|2          |93.07%/66      |
|5          |93.07%/52      |
|10         |93.06%/44      |
## hidden layer neuron number的调参
eta = 1e-2, lambda = 1e-7, mini batch size = 1, oov-ratio = 0.2

|__hidden neuron number__|__best accuracy/best epoch__|
|---------|--------------|
|100      |93.05%/74     |
|150      |93.00%/62     |
|160      |93.07%/36     |
|200      |93.14%/60     |
|250      |93.16%/34     |
|300      |93.31%/60     |
|350      |93.20%/50     |
|400      |93.28%/40     |
## oov ratio的调参
eta = 1e-2, lambda = 1e-7, mini batch size = 1, hidden neuron number = 300

|__oov ratio__|__best accuracy/best epoch__|
|-------|---------------|
|0.1    |93.25%/50      |
|0.2    |93.28%/60      |
|0.3    |93.22%/46      |
|1.0    |92.98%/28      |
