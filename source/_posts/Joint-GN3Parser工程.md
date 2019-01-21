title: Joint-GN3Parser工程
date: 2017-04-05 14:10:53
tags: [work]
---
# Joint-GN3Parser工程
## 简介
Joint-GN3Parser是GN3Parser的一个变种,基于GN3Parser做的一个联合词性句法分析的项目.
<!--more-->
## 相关实验的记录
### 加入了Load pretrained Model的功能 (2017-5-27)
因为Joint-GN3Parser的效果一直不是很好，所以考虑，利用训练好的GN3Parser-POS和GN3Parser的两个模型，作为pretrained model，初始化Joint-GN3Parser。看看效果如何？同时也发现了Joint-GN3Parser中的一个bug，在Shift动作之后，在POS动作的情况下，获取当前的标注的词性的word index的时候，获取的还是State.\_j所以，是存在着问题的，因为\_j始终都是队列中queue0的位置，而现在需要进行词性标注的是stack0的位置。在修正了这个bug，之后，我发现UAS还是没有什么变化。以下便是这一版本代码的效果记录：
__Greedy__

|__comments__|__Corpus__|__POS__|__UAS__|__LAS__|__Position__|
|------------|----------|-------|-------|-------|------------|
|without pretrained model|Dev   |94.15% |80.22% |75.98% |gpu-no-1:~/Joint-GN3Parser/debug-v1.9  |
|without pretrained model|Test  |94.08% |80.12% |76.07% |gpu-no-1:~/Joint-GN3Parser/debug-v1.9  |
|with pretrained model  |Dev    |94.33% |80.71% |76.79% |gpu-no-1:~/Joint-GN3Parser/1.9-w-pretrained-model |
|with pretrained model  |Test   |94.07% |80.76% |76.69% |gpu-no-1:~/Joint-GN3Parser/1.9-w-pretrained-model |
__Global__

|__comments__|__Corpus__|__POS__|__UAS__|__LAS__|__Position__|
|------------|----------|-------|-------|-------|------------|
|without pretrained model |Dev  |94.54% |83.63% |79.92%  |gpu-no-1:~/Joint-GN3Parser/debug-v1.9 |
|without pretrained model |Test |94.36% |83.56% |79.76%  |gpu-no-1:~/Joint-GN3Parser/debug-v1.9 |
|with pretrained model    |Dev  |94.50% |83.55% |79.88%  |gpu-no-1:~/Joint-GN3Parser/1.9-w-pretrained-model |
|with pretrained model    |Test |94.09% |83.43% |79.66%  |gpu-no-1:~/Joint-GN3Parser/1.9-w-pretrained-model |
### 修正了抽取Left\_Label时的错误 (2017-5-15)
因为在GN3Parser中，抽取Left\_arc 和 Left\_label的特征是一样的，这两个action是同时执行的，所以这两个动作的特征模板时一样的；但是在联合模型中，将Left\_arc 和Left\_label两个动作拆开了，首先执行Left\_arc，那么栈里面的元素就会有变化，所以Left\_label抽取出来的特征就和原来的不一样了。所以需要修正。
（<font color='red'>log已经覆盖</font>）

|__comments__|__eta__|__POS__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|-------|------------|
|Dev         |0.05   |93.89% |79.87% |75.82% |gpu-no-1:~/Joint-GN3Parser/debug-v1.8       |
|Test        |0.05   |93.63% |79.69% |75.42% |gpu-no-1:~/Joint-GN3Parser/debug-v1.8       |
从实验结果来看，非但Parsing的结果没有得到很好的提升，连POS的准确率都下降了不少，觉着与预想的不合，很奇怪；应该不是代码的问题，就修改了一点点代码。需要验证一下抽取特征的代码和predict的时候代码。
在写GN3Parser分为三个模型的时候，发现了一个bug，在right\_label的操作：
```c++
	next->action = action
```
这一部分的代码错误，应当是ac！这样子就把right\_arc这一个动作直接复制到了action里面，以后所有的动作都会是right\_label！！！但是这个bug好像没有影响？因为在Joint模型中，有奇数步和偶数步的作用。
我们看对应的Global的实验结果。（在正确的Feature List的结果下）(2017-5-17)

|__comments__|__eta__|__POS__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|-------|------------|
|Dev         |0.03   |94.26% |83.46% |79.92% |gpu-no-1:~/Joint-GN3Parser/debug-v1.8       |
|Test        |0.03   |93.95% |83.69% |79.76% |gpu-no-1:~/Joint-GN3Parser/debug-v1.8       |
### 增加了prefix和suffix, length=1的特征用作POS(2017-5-10)
因为在GN3Parser-POS中，POS准确率达到了94.2%在test数据集上，所以，尝试将POS特征集合(__Greedy__)。

|__comments__|__eta__|__POS__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|-------|------------|
|Dev         |0.03   |94.16% |79.59% |75.25% |gpu-no-1:~/Joint-GN3Parser/v1.7-greedy-eta-0.03            |
|Dev         |0.05   |94.08% |79.91% |75.48% |gpu-no-1:~/Joint-GN3Parser/v1.7-greedy-eta-0.05            |
|Dev         |0.08   |93.98% |79.16% |74.66% |gpu-no-1:~/Joint-GN3Parser/debug-v1.7            |
|Test        |0.03   |94.00% |79.79% |75.31% |gpu-no-1:~/Joint-GN3Parser/v1.7-greedy-eta-0.03            |
|Test        |0.05   |93.92% |__80.06%__ |75.59% |gpu-no-1:~/Joint-GN3Parser/v1.7-greedy-eta-0.05            |
|Test        |0.08   |93.94% |79.72% |75.18% |gpu-no-1:~/Joint-GN3Parser/debug-v1.7            |

### 修改POS的相关特征(2017-4-30)
再次调研SyntaxNet的词性标注的特征模板，发现其不仅仅使用了Word Embedding，还使用了Char Embedding，使用了前缀和后缀，length=2
另外，我貌似发现了为什么GPU服务器上面编译就不能使用MKL加速，乃是因为不知道为什么在GPU服务器上面编译的时候，main总不是最有一个编译的，编译顺序有点不对。

|__comments__|__eta__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|------------|
|Dev   (64;8;8-128)      |0.08       |79.91% |75.27% |gpu-no-1:~/Joint-GN3Parser/debug-v1.5.3    |
|Test  (64;8;8-128)      |0.08       |80.19% |75.49% |gpu-no-1:~/Joint-GN3Parser/debug-v1.5.3　  |
|Dev   (64;50;50-200;200)|0.08       |80.12% |75.49% |gpu-no-1:~/Joint-GN3Parser/debug-v1.5.4    |
|Test  (64;50;50-200;200)|0.08       |80.32% |75.63% |gpu-no-1:~/Joint-GN3Parser/debug-v1.5.4    |
### 修改词性Embedding的使用(2017-4-29)
一个想法：将模型预测出来的词性和1-best词性使用同一套embedding，测试这样子的模型效果如何(实验完)

|__comments__|__eta__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|------------|
|Dev         |0.05   |79.91% |75.35% |m175 ~/Joint-GN3Parser/v1.5.2-greedy-eta-0.05  |
|Dev         |0.08   |79.85% |75.34% |gpu-no-1:~/Joint-GN3Parser/v1.5.2-greedy-eta-0.08  |
|Dev(Bad hyper parameter)         |0.12   |30%    |       |gpu-no-1:~/Joint-GN3Parser/v1.5.2-greedy-eta-0.12  |
|Test        |0.05   |__80.36%__ |__75.61%__ |m175 ~/Joint-GN3Parser/v1.5.2-greedy-eta-0.05  |
|Test        |0.08   |80.10% |75.40% |gpu-no-1:~/Joint-GN3Parser/v1.5.2-greedy-eta-0.08  |
|Test                             |0.12   |       |       |gpu-no-1:~/Joint-GN3Parser/v1.5.2-greedy-eta-0.12  |

在v1.5.2-greedy-eta-0.05得到的Greedy模型的前提下，我们进行了Global的实验，实验结果如下：(2017-5-2)

|__comments__|__eta__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|------------|
|Dev         |0.01   |82.09% |78.05% |gpu-no-1:~/Joint-GN3Parser/v1.5.2-global-eta-0.01 |
|Test        |0.01   |82.51% |78.23% |gpu-no-1:~/Joint-GN3Parser/v1.5.2-global-eta-0.01 |
|Dev         |0.03   |82.80% |78.65% |gpu-no-1:~/Joint-GN3Parser/v1.5.2-global-eta-0.03 |
|Test        |0.03   |83.26% |79.02% |gpu-no-1:~/Joint-GN3Parser/v1.5.2-global-eta-0.03 |
从实验结果来看，在将1-best词性添加到特征模板里面，又使用同一套词性Embedding，Global的结果并没有得到很好的改善。反而没有原先的来得高（UAS：84.10%，不使用1-best词性，不知道是什么的原因）
### 再添加预测POS的相关特征 (2017-4-26)
用于POS预测的特征模板如下图所示：
![FeatureTemplates](/images/Joint-GN3Parser/FeatureTemplates-POS.bmp)

首先记录一下加入了额外特征用作POS的效果，Greedy(现在模型跑得越来越慢)
__结论__:在添加了State里面的相关特征之后，模型的效果反而变差了，一定程度上面可以说明我们添加的这几个特征是无效的、或者说是效果更差的(2017-4-30)

|__comments__|__eta__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|------------|
|Dev         |0.05   |78.00% |73.06% |m175 ~/Joint-GN3Parser/v1.5.1-greedy-eta-0.08  |
|Test        |0.05   |78.61% |73.65% |m175 ~/Joint-GN3Parser/v1.5.1-greedy-eta-0.08  |
|Dev         |0.08   |77.04% |71.98% |gpu-no-1:~/Joint-GN3Parser/v1.5.1-greedy-eta-0.08  |
|Test        |0.08   |77.79% |72.62% |gpu-no-1:~/Joint-GN3Parser/v1.5.1-greedy-eta-0.08  |
从目前的结果来看，我们添加的几个用于POS的特征，反而起到了反作用。UAS反而降低了，可能是超参没有调整好，也有可能添加的几个特征就是不会有很好的效果。。

### 添加了1-best 词性特征的效果 (2017-4-25)
在尝试了将Joint-GN3Parser的模型按照功能分隔开之后，我们还尝试了将1-best tags词性加入到模型中，分别在Atomic Model, Left Label, Right Label抽取特征的时候，在词性特征的里面加上1-best tags的信息。所以，总共的磁性特征的总数为15 + 18 = 33.使用的Atomic、Left Label、Right Label的特征模板如下图所示：

![FeatureTemplates](/images/Joint-GN3Parser/FeatureTemplates-w-auto-tags-features.bmp)
记录一下在Greedy训练过程中，相关结果。

|__comments__|__eta__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|------------|
|Dev Corpus  |0.03   |79.41% |75.11% |m175 ~/Joint-GN3Parser/v1.5-greedy-eta-0.03  |
|Dev Corpus  |0.05   |79.95% |75.34% |m175 ~/Joint-GN3Parser/v1.5-greedy-eta-0.05  |
|Dev Corpus  |0.08   |79.46% |75.12% |m175 ~/Joint-GN3Parser/v1.5-greedy  |
|Test Corpus |0.03   |79.93% |75.44% |m175 ~/Joint-GN3Parser/v1.5-greedy-eta-0.03  |
|Test Corpus |0.05   |80.00% |75.42% |m175 ~/Joint-GN3Parser/v1.5-greedy-eta-0.05  |
|Test Corpus |0.08   |__80.12%__ |__75.57%__ |m175 ~/Joint-GN3Parser/v1.5-greedy  |
|eta设置不对，实验直接kill   |0.12   |30%    |3%     |m175 ~/Joint-GN3Parser/v1.5-greedy-eta-0.12  |

暂时使用了Test数据集80.03%那个模型、进行Global的实验。(2017-4-29)

|__comments__|__eta__|__UAS__|__LAS__|__Position__|
|------------|-------|-------|-------|------------|
|Dev Corpus 文件夹名字忘记修改了～ |0.01   |82.70%  |78.66%  |gpu-no-1:~/Joint-GN3Parser/v1.5-global-eta-0.03|
|Test Corpus |0.01                         |83.20%  |79.10%  |gpu-no-1:~/Joint-GN3Parser/v1.5-global-eta-0.03|
|Dev Corpus  |0.03   |83.07% |78.99% |m175 ~/Joint-GN3Parser/v1.5-global-eta-0.03    |
|Test Corpus |0.03   |83.53% |79.32% |m175 ~/Joint-GN3Parser/v1.5-global-eta-0.03    |
### Joint-GN3Parser beam size的影响
因为现在想起来现在Global的实验beam size = 32，但是先前GN3Parser得到最好的效果的beam size = 64

|__Comments__|__Beam Size__|__UAS__|__LAS__|__Position__|
|------------|-------------|-------|-------|------------|
|GN3Parser   |32           |84.31% |80.70% |m175 ~/GN3Parser-beta/chinese-global-beam-32-fix-save-model  |
|GN3Parser移除3个queue POS特征|32   |83.73%  |79.94%  |m175 ~/GN3Parser-beta/3.8-debug    |
|Joint-GN3Parser  |32    |83.61%    |79.56%    |m175 ~/Joint-GN3Parser/v1.3.1-global-eta-0.03  |
|GN3Parser   |64           |84.60% |81.02% |gpu-no-1:~/GN3Parser-beta/global\_v\_3.5  |
|GN3Parser移除3个queue POS特征（没有该实验）|64   |  |  |    |
|Joint-GN3Parser  |64    |84.10%    | 80.03%   |m175 ~/Joint-GN3Parser/v1.3.1-global-eta-0.03-beam-64  |

### Joint-GN3Parser的情况说明(2017-4-14)
在确定的新的架构之后,着手改变原先的架构,新的架构的代码的Greedy部分已经编写完成,进行了初步的实验.
有一些实验数据,记录如下:
1. 统计了在Conll09的Chinese的数据当中,通过依存句法分析,得到的各种的States的数量,其中,我将POP\_ROOT, SHIFT, LEFT\_ARC, RIGHT\_ARC 统称为Atomic States.

|__Atomic States__|__POS States__|__Left Label__|__Right Label__|
|-----------------|--------------|--------------|---------------|
|1240397          |609060        |361100        |247960         |
2. 现在我阐述一下我几个Classifier的简单实现情况:atomic, left label, right label classifier的模型、抽取的特征等内容与GN3Parser完全一致，采取48个特征。但是POS classifier有所区别，在预测词性的时候，我们目前采用window size = 3的特征，所以在POS classifier中，我们的输入是7个word embedding的组合，模型的 hidden layer size和前面提到的atomic等模型一致，激活函数等都是一样的。

3. 几个实验记录（汇报的均是Test数据集的结果）：

|__comments__|__POS__|__UAS__|__LAS__|__position__|
|------------|-------|-------|-------|------------|
|a batch:20\10\6\4 除以state总数 *Greedy* 没有加greedy 非法操作排除 |92.93% |79.49%  |71.95% |m175 ~/Joint-GN3Parser/v1.3-greedy-eta-0.12 |
|a batch:20\10\6\4 除以state总数 *Greedy* 没有加greedy 非法操作排除 eta = 0.16|92.71% |79.08%|71.52% |m175 ~/Joint-GN3Parser/v1.3-greedy-eta-0.16 |
|a batch:20\10\6\4 除以state总数 *Greedy*|92.85% |79.28% | 74.78%     |m175 ~/Joint-GN3Parser/v1.3.2-greedy-eta-0.12  |
|a batch:32\32\32\32 除以single state bath=32 *Greedy* |92.89%   | 79.76% |75.22%   |m175 ~/Joint-GN3Parser/v1.3.3-greedy-eta-0.12  |
|<font color=blue>*Global*</font>    |93.77%  |83.64%  |79.59%  |m175 ~/Joint-GN3Parser/v1.3.1-global-eta-0.01   |

(一下有关Joint-GN3Parser的实验中，全部都是使用的老的架构)记录最初的几个实验(这里只汇报dev的结果，如果test的结果有明显的提升，单独汇报)：
在这几个试验中，超参都没有调试，都是沿用的原来的GN3Parser中的参数，除了batch有所调整外。

|__position__|__comments__|__UAS__|__LAS__|
|------------|------------|-------|-------|
|m175 ~/Joint-GN3Parser/debug-v1.0 |该版本的实验的测试windown size=2的特征for POS，并且，batch为100\50\30\20|77.70%  |69.76%  |
|m175 ~/Joint-GN3Parser/1.0-test-batch |该版本的实验window size=2， batch为20\10\6\4  |77.52% |69.79% |
|m175 ~/Joint-GN3Parser/debug-v1.1    |window size=3, batch=20\10\6\4  |77.81%   |70.11%  |
|m175 ~/Joint-GN3Parser/debug-1.2  |window size=3, batch=20\10\6\4, 还使用了前面三个word 的tag |52.40% |37.36%  |

从上面的几个实验来看，我发现了几个很奇怪的现象：
1. batch的调整几乎没有带来任何的影响？连速度的影响都没有？已经确定不是代码的问题。我想可能的几个原因是：
	1. 其实模型的计算，在Greedy过程的时间消耗中，占用的时间比例很少；
	2. MKL的处理速度都快，仅仅5倍的数据根本体现不出来速度的差别
2. 为什么添加了词性特征后，UAS变得低得离谱？参数问题？还是词性的错误传递效果更大了？

### 初步调参（以下说明的实验结果都是老的架构的结果，将POS和其他的一些操作全部放在了同一个模型中）
因为baseline的结果不是很好,考虑到是不是参数的问题,现在做一个初步的调参,从实验结果来看,eta = 0.01的收敛过程和最终的效果要比 eta = 0.03 好很多.
__Global Dev__

|__comments__|__POS__|__UAS__|__LAS__|__position__|
|------------|-------|-------|-------|------------|
|eta = 0.03  |93.71% |81.86% |78.28% |m175 ~/Joint-GN3Parser/debug-v0.3.1-global |
|eta = 0.01  |93.89% |82.26% |78.67% |m175 ~/Joint-GN3Parser/debug-v0.3.1-global-eta-0.01 |

__Global Test__

|__comments__|__POS__|__UAS__|__LAS__|__position__|
|------------|-------|-------|-------|------------|
|eta = 0.03  |93.59% |82.34% |78.65% |m175 ~/Joint-GN3Parser/debug-v0.3.1-global |
|eta = 0.01  |93.78% |__82.84%__ |79.08% |m175 ~/Joint-GN3Parser/debug-v0.3.1-global-eta-0.01 |

### baseline
这里的baseline如下描述:
基于GN3Parser的一个词性句法联合模型,在GN3Parser的基础之上,去掉了48个特征中,queue的4个特征;修改了抽取特征的相关情况,在有关POS的特征,都是使用的模型预测出来(SHIFT\_T)的词性.在评价中,我们还给出了POS的Accuracy.
__Greedy__

|__comments__|__POS__|__UAS__|__LAS__|__position__|
|------------|-------|-------|-------|------------|
|baseline development|93.24% |79.48% |75.76% |m175 ~/Joint-GN3Parser/debug-v0.3.1  |
|baseline test       |93.28% |79.68% |75.85% |m175 ~/Joint-GN3Parser/debug-v0.3.1  |
|GN3Parser移除了3个词性特征 development|--  |80.46% |76.68%  |m175 ~/GN3Parser-beta/3.8-debug  |
|GN3Parser移除了3个词性特征 test|--         |80.33% |76.45%  |m175 ~/GN3Parser-beta/3.8-debug  |

__Global__

|__comments__|__POS__|__UAS__|__LAS__|__position__|
|------------|-------|-------|-------|------------|
|baseline development|93.71% |81.86% |78.28% |m175 ~/Joint-GN3Parser/debug-v0.3.1-global |
|baseline test       |93.59% |82.34% |78.65% |m175 ~/Joint-GN3Parser/debug-v0.3.1-global |
|GN3Parser移除了3个词性特征 development| --  |83.59% |79.98% |m175 ~/GN3Parser-beta/3.8-debug   |
|GN3Parser移除了3个词性特征 test       | --  |83.73% |79.94% |m175 ~/GN3Parser-beta/3.8-debug   |

## 一些比较容易忘记的代码部分
1. 需要确保ROOT,UNKNOWN,NULL这三个在抽取词典的时候在最后.
2. 如何将id 和 相对应的POS or Label对应起来?应用第一条规则,因为在抽词典的时候,会在词典的后面人为的加上"ROOT,UNKNOWN,NULL"(抽取特征的时候,会用到),所以在进行神经网络输出层的相关判断以及转换的时候,需要把最后几个开除掉,这个通过\_g\_num\_null实现,很容易可以从代码中看出来.
