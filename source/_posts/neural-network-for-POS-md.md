title: neural-network-for-POS.md
date: 2016-5-19 09:17:20
tags: [neural-network, python]
---
# 使用神经网络进行词性标注的相关调参数据记录
## 概述
因为针对所有的数据所编写的神经网络已经完成，目前的工作就是对相关的超参进行调参，以求达到一个比较好的正确率，现在将相关的调试记录下来，以便以后使用。
为了有比较，我们分别使用了linear model, global linear model, CRF进行了测试，所得的结果如下：
__linear model:93.17%/9__
__global linear model:94.18%/18__
__CRF: 93.5819%/13__

## 对oov-ratio调参
oov-ratio的使用如下：
```
	np.random.binomial(1, p) == 1:
```
如果当p == 0的时候，这个条件永远为False；当p == 1的时候，这个条件永远为真，所有的词频为1的word就会使用oov embedding。
<!-- more -->
hidden layer neuron number = 150, eta = 0.05, lambda = 1e-2, oov-ratio = ?, mini\_batch\_size = 60

|__oov-ratio__|__best accuracy/epoch__|
|-------|--------------|
|0      |92.30%/11     |
|0.1    |92.59%/19     |
|0.2    |92.60%/24     |
|0.3    |92.65%/12     |
|0.4    |92.60%/20     |
|0.5    |92.56%/13     |
|1.0    |92.36%/27     |

## 是否更新embedding
hidden layer neuron number = 150, eta = 0.05, lambda = 1e-2, oov-ratio = 0.2, mini\_batch\_size = 60

|__update embedding ?__|__best accuracy/epoch__|
|-----|----------------------|
|YES  |92.56%/16             |
|NO   |89.80%/41             |

## 对步长eta调参
hidden layer neuron number = 150, lambda = 1e-2, oov-ratio = 0.2, mini\_batch\_size = 60， 使用update embedding

|__eta__|__best accuracy/epoch__|
|-------|-----------------------|
|1      |91.48%/169             |
|0.5    |92.33%/59              |
|0.1    |92.34%/10              |
|0.05   |92.70%/13              |
|0.01   |93.19%/50              |
|0.005  |93.17%/106             |

*准确率突然上来了*

## 对正则化因子lambda调参
hidden layer neuron number = 150, eta = 0.01, oov\_ratio = 0.1, mini\_batch\_size = 60, 使用update embedding

|__lambda__|__best accuracy/epoch__|
|----------|-----------------------|
|1         |93.04%/64                       |
|1e-1      |93.20%/73              |
|1e-2      |93.05%/52              |
|1e-3      |93.09%/61              |
|1e-4      |93.08%/47              |
|1e-5      |93.01%/49              |
在这边准确率达到了93.20%/73

## 对hidden layer neuron number调参
hidden layer neuron number = ?, eta = 0.01, lambda = 1e-1, oov\_ratio = 0.2, mini\_batch\_size = 60, 使用update embedding

|__hidden layer neuron number__|__best accuracy/epoch__|
|-------|-------------|
|60     |92.71%/39    |
|80     |93.00%/80    |
|100    |92.94%/43    |
|150    |93.08%/72    |
|200    |93.14%/65    |

## 对mini batch size调参
hidden layer neuron number = 150, eta = 0.01, lambda = 1e-1, oov\_ratio = 0.2, mini\_batch\_size = ?, 使用update embedding

|__mini batch size__|__best accuracy/epoch__|
|----------|-------------------|
|1         |93.07%/54          |
|50        |93.06%/54          |
|60        |93.11%/63          |
|100       |93.10%/52          |
|500       |93.12%/59          |
|1000      |93.18%/84          |

## 总结
至此，我们的调试超参的工作就都已经完成了。我们发现，因为神经网络的初始化weight和biases都是随机的，所以得到的准确率有一点点的浮动。

## CTB7数据集的test测试
使用已经训练好的模型进行test数据集的测试，结果如下：

|__epoch__|__Accuracy(dev/test)__|
|---------|----------------------|
|45       |93.22%/92.99%         |
[log文件](/documents/mlnn/log_test.txt)













<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="http://music.163.com/outchain/player?type=2&id=31654479&auto=1&height=66"></iframe>

