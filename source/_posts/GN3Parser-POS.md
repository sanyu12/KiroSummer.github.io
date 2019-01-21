title: GN3Parser-POS
date: 2017-05-09 09:35:27
tags: [work]
---
# 简介
这个工作是做的POS Tagging。因为在词性句法联合模型中，遇到了阻力。从模型输出的结果来看，词性的Accuracy明显低于我们在GN3Parser中利用的自动词性的Accuracy。所以，我们暂停了Joint-GN3Parser的工作，暂时全面的重现Google论文的词性结果。
<!--more-->
# 确定模型的输入
1. 在Google论文中，提到了一些输入： word，cluster，character n-gram up to length 3，the tag predicted for the previous 4 tokens
2. 我们目前使用的输入：word，character n-gram up to lenght 2，the tag predicted for the previous 4 tokens.

# 实验结果
目前我们最好的实验结果在Greedy过程中比Google论文中的结果(94.56%)还差0.3%.
__Dev数据集__

|__comments__|__POS__|__position__|
|------------|-------|------------|
|w/o previous 4 predicted tags    |94.62%  |gpu-no-1:~/GN3Parser-POS/debug-v0.2    |
|w previous 4 predicted tags    |94.60%  |gpu-no-1:~/GN3Parser-POS/debug-v0.3    |

__Test数据集__

|__comments__|__POS__|__position__|
|------------|-------|------------|
|w/o previous 4 predicted tags    |94.21%  |gpu-no-1:~/GN3Parser-POS/debug-v0.2    |
|w previous 4 predicted tags    |94.28%  |gpu-no-1:~/GN3Parser-POS/debug-v0.3    |

![POS-Accuracy](/images/GN3Parser-POS/gn3parser-pos.bmp)

目前的Global实验我已经跑过，beam大小设置成和Google论文中一样8，但是实验结果一直不可以，不论怎样调参，差不多收敛的时候，POS Accuracy都是只能够达到94.2%左右，完全赶不上Greedy的效果；已经确认过代码，目前看不到什么问题。

# 5-fold实验
跑了POS的5-fold的实验：gpu-no-1:~/n-fold/n-fold
train: 95.01%  |dev: 94.60%  |test: 94.29%
