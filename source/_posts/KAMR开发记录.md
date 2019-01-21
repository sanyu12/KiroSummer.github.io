---
title: KAMR开发记录
date: 2018-1-31 13:42:52
tags: [amr]
---
# 简述
新开一篇博客记录一下AMR Parser (KAMR)的开发经过
<!--more-->
# FCL相关工作
## AMR LDC2014T12近几年来的实验结果
整理一下 AMR最近几年来的实验结果：

|__Data__|__Parser__|__Dev__|__Test__|
|--------|----------|-------|--------|
|LDC2014T12|JAMR    |--     |58.2%   |
|LDC2014T12|CAMR    |--     |66.5%   |
|LDC2014T12|Zhou et al., 2016 EMNLP  |--     |66%   |
|LDC2014T12|Wang et al., 2017 EMNLP  |--     |68.07%   |
|LDC2014T12|SBMT (Pust, 2015 ACL)    |--     |67%   |

## 2-18-2-5
有一个很奇怪的现象, 利用 Biaffine LSTM Output充当上下文信息和利用产自于 Concept Identification LSTM Output, 虽然在给定 JAMR的 Concepts的基础之上, 两者的效果相差无几, 但是当使用预测得到的 Concepts的时候, 利用 Concept LSTM的效果要明显优于 Biaffine的 LSTM的结果.
## 2018-2-3
结论: 发现, 预测 Concept Label和 Concept共享参数是不会有什么明显的影响的. 试一试换一下梯度更新的算法? Adam?
## 2018-2-2
通过实验发现，Biaffine LSTM Output还是有作用的

|____|__Concept Label Precision Compared w JAMR__|__Concept Precision Compared w JAMR__|__Path__|
|----|-------------------------------------------|-------------------------------------|--------|
|w/o Biaffine|27089 / 29269 = 92.552             |13214 / 16499 = 80.09                |                        |
|w Biaffine (Concept Label)  |27115 / 29269 = 92.641             |13294 / 16337 = 81.374               |n174:~/KAMR/v1.4.28.7.3-exp  |
|w Biaffine (Concept Label + Identification)| 27089 / 29269 = 92.552|13374 / 16517 = 80.971            |                |
|w Biaffine (Concept Label + Identification + concept table window 5) |27060 / 29269 = 92.453 |13278 / 16432 = 80.806 |           |

__结论:__我们可以看到:
1. Biaffine的结果对于 Concept Label的预测是有效果的, 但是对于之后的 Concept Identification并没有明显的提升的效果.
2. 对于试图扩展 conceptTable, 从理论上来讲是可行的的, 但是从实际的效果来看, 反而有所下降, 感觉是很奇怪的一个现象.

## 2018-1-31
自从发现了Bug，到现在，终于又有了一点的起色。
方法：对__未在__ Concept Table中的 PREDICATE 进行 规则+FCL 处理，能够有所作用，最新的实验结果如下：

|____|__Smatch FScore Dev__|__Smatch FScore Test__|
|----|---------------------|----------------------|
|Baseline|64.00%            |63.69%                |
|规则+FCL|64.22%            |64.10%                |
## 2018-1-21
发现了一个比较严重的Bug，concept identification部分的时候，使用了 JAMR的concept label，所以原来的实验结果都偏高。现在就在原来的实验结果之上，重新跑一遍测试。

|____|__Smatch FScore Dev__|__Smatch FScore Test__|
|----|---------------------|----------------------|
|before |66.64%            |66.83%                |
|Fix Bug|64.00%            |63.69%                |

### 加入 Biaffine LSTM Representation
考虑了一下，还是决定加入 Biaffine LSTM Representation，因为明显的发现，在 concept identification这一步骤中，concept label的预测是十分重要的，也可以是看做之后的工作的基础，而这一步的结果也并没有很理想。从之前的实验结果来看，实验结果相对于 JAMR略去了很多类似于主语 i的内容，将之识别为__N__。猜想，如果加入 Biaffine的信息，能够识别出来这是一个主语，应当就能够保留这一部分的内容，具体的效果还要从实验结果来看。

|__Ideas__|__Concept FScore__|
|---------|------------------|
|在 concept label部分加入 biaffine lstm output|78.65%    |
|在 concept identification部分加入 biaffine lstm output|  |

## 2018-1-18
在融合代码的时候，出现了一个问题，为什么对 concept进行测试的时候，准确率等指标会和训练的时候不一致？同样的代码，同样的环境，居然能够跑出相差挺大的实验结果？有随机的成份？可是哪里会有随机的成分？
## 2018-1-9
在修正了融合的代码之后，跑了几个实验：

|____|__Smatch FScore Dev__|
|----|---------------------|
|merged, max pooling, update relation lstm loss   |       |
|merged, max pooling, no update relation lstm loss|       |
|merged, minus, update relation lstm loss         |       |
|merged, minus, no update relation lstm loss      |       |
|no merged, minus, biaffine lstm                  |       |
## 2018-1-8
记录一些代码中，容易出现前后不一致的情况：
1. BatchState中，使用的是 SumPooling还是 MaxPooling
2. Relation 中，一定要首先 sort concepts再进行后续的操作，抽取 states等等

## 2018-1-4
记录一下最近发现的一些Bug：
1. 因为在 Relation Identification这一步骤需要首先对 JAMR识别出来的 concepts进行排序，而我先前写的排序算法是根据每一个 concept的 begin_index进行的，但是现在发现，在语聊中存在着2个 concepts的 begin_index是同一个的情况，这就导致了排序之后，同一个 concept会出现两次！所以在 delete的时候会出现内存错误的情况。这个 Bug对之前跑的实验都有一定的影响，正在重新跑实验进行验证!不需要验证，原来 Relation Identification步骤使用的函数的实现不一样，是对的。

## 2018-1-2
测试一下在__v1.4.25__ (加入了update the loss of the concept lstm in the other two models)模型的 concept lstm output的__v1.3.2-train-max-pooling__实验结果：

|__KAMR iter__|__Smtach FScore Dev__|__Smatch FScore Test__|
|-------------|---------------------|----------------------|
|5            |65.95%               |66.02%                |
|10           |66.61%               |66.65%                |
|20           |66.64%               |66.83%                |
## 2017-12-27
将 concept identification stage's lstm output得到两个模型 (concept identification, fcl)的 loss，并且更新， 直接在 Biaffine的 lstm output的实验来验证效果。

|__KAMR__|__Smatch Fscore Dev__|__Smatch Fscore Test__|
|--------|---------------------|----------------------|
|v1.4.24 |66.34%               |                      |
|同上+lstm loss update|66.66%  |66.59%                |
## 2017-12-26
处理一些可以使用规则处理的部分事情：date, time, person...

|__KAMR__|__Smatch Fscore Dev__|
|--------|---------------------|
|v1.4.22.2|66.14%              |
|同上+date (Dev里面差不多有36个 date)|66.34%              |
## 2017-12-25
Relation Identification w JAMR concepts and v1.4.22.2 concept lstm output on LDC2014T12的实验结果:
![relation](/images/kamr/relationIdentification.bmp)
比较奇怪的是，从上面的结果中，并没有发现与之前的结论一致的地方（之前发现，iter=20(74.5%)与iter=40(77.8%)有明显的差距）。为什么这一次的几次实验结果都差不多？但是也没有达到78%？都可以达到77.5%左右。是因为加入了 NER信息的缘故？

|__iter__|__relation identification__|__Dev__|__Test__|
|--------|---------------------------|-------|--------|
|10      |77.35%                     |65.46% |65.37%  |
|20      |77.44%                     |65.67% |65.40%  |
|30      |77.49%                     |64.23% |63.52%  |
|40      |77.27%                     |59.98% |60.27%  |
### 测试 stemmer和 lemmatize
在v1.4.24-debug中，分别测试 stemmer和 lemmatize作为 -NON-PREDICATE处理方法的效果：

|__word lemmatize method__|__concept precision__|
|-------------------------|---------------------|
|lemmatize                |80.47%               |
|stemmer                  |79.72%               |

## 2017-12-18
记录一下加入了 NER之后的相关实验结果。

|      |__introduction__|__concept identification__|__relation identification__|__Final__|
|------|----------------|--------------------------|---------------------------|---------|
|FScore|将NER直接已embedding的形式加入         |79.98%                    |78%(v1.3.2-test)           |--%      |
|FScore|同上+去除span==1的限制         |80.32%                    |78%(v1.3.2-test)           |__66.14%__      |
|FScore|同上+强制根据NER选择FCL+去除span==1的限制         |80.33%                    |78%(v1.3.2-test)           |--%      |
|FScore|同上+强制根据NER选择FCL+去除span==1的限制+oracle PREDICATE         |81.15%                    |78%(v1.3.2-test)           |__66.68%__      |


|      |__introduction__|__concept identification__|__relation identification__|__Final__|
|------|----------------|--------------------------|---------------------------|---------|
|FScore in Test|同上+强制根据NER选择FCL+去除span==1限制   |80.40%                    |78%(v1.3.2-test)           |65.93%   |
从第二条结果，我们看到了很奇怪的现象，明明没有 concept identification的 FScore都还没有下面的80.82%来的高，但是 Pipeline结果却是出奇的好。为了验证一下结果的准确性，我重新跑了一下测试，发现结果是对的，这就很奇怪了。可能的解释：因为是 Pipeline的模式，可能加入了 NER信息的结果更加适合 downstream的代码，所以产生了更好的结果。
## 2017-12-15
将 stanford ner tagger处理完成的语料和之前的进行合并，这里记载一个比较重要的<font color=blue>人工修改</font>：
1. 在 Dev中，bolt12_64556_5620.8，因为句子最后有特殊字符，做 pos的时候，会漏掉一个，人工补上。
2. 在生成的 fcls.gz里面，最后一个 polarity因为考虑不周到的原因，需要人工加入 place holder 'X'

<font color=blue>发现一个问题：为什么当初加 char embedding的时候，没有加入到预测 boundary label的模型中？</font>

|      |__introduction__|__concept identification__|__relation identification__|__Final__|
|------|----------------|--------------------------|---------------------------|---------|
|FScore|             |79.98%                    |78%(v1.3.2-test)           |--%   |
## 2017-12-13
利用从 PropBaank里面提取出来的 frameset，融合进从 LDC2014 train里面提取的 conceptTable，直接进行训练，最终的 FScore又得到了一点提升：

|      |__concept identification__|__relation identification__|__Final__|
|------|--------------------------|---------------------------|---------|
|FScore|80.82%                    |78%(v1.3.2-test)           |65.39%   |
|FScore(w/o oracle FCL PREDICATE)|79.88%                    |78%(v1.3.2-test)           |64.79%   |
|FScore(w/o oracle FCL PREDICATE, using stemmer's concept)|80.00%       |78%(v1.3.2-test)    |64.87%   |
表格中的三行的详细记录：
1. 在 concept identification部分，当在 FCL部分的时候，直接对 PREDICATE部分利用 oracle PREDICATE进行替代。
2. 还是在和1. 相同的部分，不使用 oracle PREDICATE，直接赋值为空。
3. 在预测的时候，如果一个 word没有能够找到它的 concept map，则尝试该 word的 stemmer，再次尝试查询是否存在 concept map，如果存在，则选择使用；否则，赋值为空。

应该能够做一些提升：加入 NER的信息能够更加准确的识别出一些目前还判断错误的地名。

附 stemmer, lemmatizer地址：
[stemmer](http://www.nltk.org/howto/stem.html), [lemmatizer](https://pythonprogramming.net/lemmatizing-nltk-tutorial/)

## 2017-12-12
采用了 lemmatize，对 PREDICATE进行处理：

|      |__concept identification__|__relation identification__|__Final__|
|------|--------------------------|---------------------------|---------|
|FScore|80.35%                    |78%(v1.3.2-test)           |65.04%   |
但是还是采取了 oracle PREDICATE的做法。

## 2017-12-11
对 FCL进行了一些修改：1. 不再执行大小写转换，一律保留 word在句子中的形式；2. 对于 multi-concepts中包含 name字段的 placeholder部分进行填充的时候，在 word两端加上双引号。最新的实验结果如下：

|      |__concept identification__|__relation identification__|__Final__|
|------|--------------------------|---------------------------|---------|
|FScore|78.31%                    |78%(v1.3.2-test)           |63.93%   |
使用的 relation identification部分的内容是有 biaffine output的，有两个原因使用这一部分的测试代码：
1. biaffine output的模型可以随时拿来测试，并且和 concept identificaton的 lstm output模型的效能基本一样。
2. 如果每一次修改一下 concept identification部分，都要根据这一部分的 lstm output重新训练一个 relation部分，有点拖沓。

尝试了一个想法：如果利用 oracle PREDICATE暂时处理当前未在词典里面的 PREDICATE，FScore能够达到64.76%.

## 2017-12-8
Bug: 发现在进行 concept评价的时候，发现进行 concept number计数的时候，存在着一些问题：没有排除空白字符的情况，所以 predicted concepts的总数和正确的数目都是有问题的。更新了评价，发现没有加入 FCL之前的一些 FScore大都维持在77.52%。最近的粗糙的 FCL的FScore，78.15%。

## 调研了lemmatize的相关内容
发现这一部分的内容只能在 NON-PREDICATE这一部分应用；在 PREDICATE这一部分并没有什么用。因为 PREDICATE这一部分大都是 verb+number 的组合，而 lemmatizer并没有这个功能 (non to verb)。


# 将 sumpooling修改为 maxpooling的结果 (2017-12-6)
|      |__concept identification__|__relation identification__|__Final__|
|------|--------------------------|---------------------------|---------|
|FScore|81.3%                     |78%                        |60.48%   |

从结果上来看，没有明显的变化。
fix the bug: when do the concept identification from the "B, I, E, S, O", use the LSTM[<font color=blue>i</font>], actually the LSTM[<font color=blue>index</font>] is true where the index = i + begin_index !

# 初步的实验结果 (2017-12-5)
|      |__concept identification__|__relation identification__|__Final__|
|------|--------------------------|---------------------------|---------|
|FScore|81.3%                     |78%                        |60.4%    |
