title: SemanticKnowledgeResearch
date: 2017-05-12 12:09:38
tags: [semantic knowledge]
---
# 1. 简介
因为Parsing的需要，现开始调研Semantic Knowledge相关的知识，做一些记录。:)

<!--more-->
# 2. 外部词典的应用
《Parsing the Penn Chinese Treebank with Semantic Knowledge》
1. 从两个外部词典抽取类型 (category)和启发式规则 (heuristic rules).
2. 在抽取出的类别的基础之上建立一个用于优先选择的子模型

有效解决：
1. nominal compund, coordination and POS tagging ambiguity
2. alleviate the data sparseness
## 2.1 抽取语义类别 (Semantic Categories)
外部词典：HowNet and TongYiCi CiLin（同义词词林）
### HowNet
语义类别 == 义位 (sememe)。通过不同类别之间的上下位关系，我们可以抽取具有不同粒度等级的语义类别。我们仅仅使用词的第一定义（定义：每一个词有很多的定义 definitions）
### CiLin
每一个节点代表一个语义类别，总计有三个类别，类别总计有 (12-97-1400种)
### HowNet + CiLin
以HowNet为主，CiLin为辅。如果有一个word在HowNet里面没有找到，但是在CiLin里面找到了，我们会找这个word的同义词，然后使用这个同义词在HowNet当中的类别 (category)。
### Heuristic Rules (HR)
启发式规则。使用简单的启发式规则识别数字和时间表达式。
## 2.2 建立一个基于类 (Class-Based)的优先选择子模型
使用从语义词典当中抽取的类别 (classes)对head和modifier的语义弧进行建模。建立一个类似bilexical-class的子模型

# 我们利用HowNet的过程
记录一下我们利用HowNet的过程：
1. 首先，利用API，将CONLL09的中文数据，所有的词，在API里面都查找一遍，找出能够找到的定义 (Definition)，并计数
2. 写一个Python脚本，利用字典合并所有的相同的定义
3. 统计HowNet覆盖的词的数量，并且得到相同定义不同词的文本文件。
统计的结果如下：

|    |__Words__|__HN1__|__HN2__|__HN2+CL__|
|----|---------|-------|-------|----------|
|Words in train  |40878|22207      |22206  |23787 |
|Words in dev    |8497 |6270       |6270   |6493  |
|Words in test   |11196|8183       |8183   |8510  |
|Classes in train|-    |1562       |465    |465   |
|Classes in dev  |-    |1094       |391    |392   |
|Classes in test |-    |1200       |411    |411   |
在抽取HN2的时候，我发现以下两个问题：
1. 有一个义项：Entity|实体，已经是最顶层的的义项了，并没有再上一层的义项了，所以默认它本身就是上一层义项。
2. 还有一个义项：Attribute|属性，并没有再上一层的义项了。
3. 从上面的数据中，我们看到，其实Train数据集的覆盖率还是挺低的；输出了数据，但是我发现词频都很低2次的很多（可能是1次，不确定抽取word的时候，有没有重复，明天确定一下TODO）
4. 在Dev中的words，6270；和Train重合的部分，5694；在Test中的words，8183.和Train重合的部分，7116
![CoNLL09-Train-HN2](/images/Semantic/CoNLL09-Train-HN2.png)
### HowNet+聚类(2017-7-1)
因为在调用HowNet的过程中，我们发现了语料中存在着大量的词没有HN2，而且这些词基本都是低频词，所以我们希望利用聚类来弥补这个HN2的缺失。
在Train、Dev、Test三个语料中，总计有21630种词没有HN2，利用聚类之后，只剩下9种词没有HN2.
下面记录详细的实验结果。

|__Corpus__|__UAS__|__LAS__|__comments__|__position__|
|------|---|----|--------|--------|
|Dev   |81.10%  |77.50%  |Greedy  |gpu-no-1:~/GN3Parser-beta/3.9.5.1-w-HN2+Word-cluster |
|Test  |81.22%  |77.55%  |Greedy  |gpu-no-1:~/GN3Parser-beta/3.9.5.1-w-HN2+Word-cluster |
|Dev   |84.66%  |81.15%  |Global  |gpu-no-1:~/GN3Parser-beta/3.9.5.1-w-HN2+Word-cluster |
|Test  |84.90%  |81.38%  |Global  |gpu-no-1:~/GN3Parser-beta/3.9.5.1-w-HN2+Word-cluster |

### HowNet细化词性的工作(2017-6-25)
我们尝试了一个工作，利用HowNet抽取语料里面的词的HN2，再按照词性进行分类，合并。
实验结果：

|__Bias__|__Corpus__|__UAS__|__LAS__|
|--------|----------|-------|-------|
|120     |Dev       |78.11% |74.14% |
|120     |Test      |79.68% |75.75% |
|200     |Dev       |75.61% |70.98% |
|200     |Test      |78.32% |74.14% |
### HowNet with GN3Parser实验(2017-6-4)
我们尝试利用HowNet的知识，组织相关的实验。如何利用HowNet？在GN3Parser中，抽取每一个word的时候，会同时抽取该word的HN2，HN2的相关信息在上面已经给出。我们设置HN2的维度为50维，以embedding的方式加入到Parser中。

|__Corpus__|__UAS__|__LAS__|__comments__|__position__|
|----------|-------|-------|------------|------------|
|Dev       |80.66% |77.03% |Greedy      |gpu-no-1:~/GN3Parser-beta/debug-3.9.5.1 |
|Test      |81.11% |77.39% |Greedy      |gpu-no-1:~/GN3Parser-beta/debug-3.9.5.1 |
|Dev       |84.48% |80.98% |Global      |gpu-no-1:~/GN3Parser-beta/debug-3.9.5.1-global  |
|Test      |84.62% |81.10% |Global      |gpu-no-1:~/GN3Parser-beta/debug-3.9.5.1-global  |
|Dev       |81.19% |77.57% |Greedy      |gpu-no-1:~/GN3Parser-beta/3.9.5.1-w-__HN2+CL__  |
|Test      |81.28% |77.53% |Greedy      |gpu-no-1:~/GN3Parser-beta/3.9.5.1-w-__HN2+CL__  |
|Dev       |84.53% |81.19% |Global      |gpu-no-1:~/GN3Parser-beta/3.9.5.1-w-__HN2+CL__  |
|Test      |84.75% |81.28% |Global      |gpu-no-1:~/GN3Parser-beta/3.9.5.1-w-__HN2+CL__  |

(<font color="red">这些实验的代码有问题，所以实验结果忽略不计，也是错误的</font>)

|__Corpus__|__UAS__|__LAS__|__comments__|__position__|
|----------|-------|-------|------------|------------|
|Dev       |79.32% |75.43% |Only train HN2, Greedy       |gpu-no-1:~/GN3Parser-beta/debug-4.0 |
|Test      |80.14% |76.14% |Only train HN2, Greedy       |gpu-no-1:~/GN3Parser-beta/debug-4.0 |
|Dev       |79.24% |75.33% |merged HN2, Greedy           |gpu-no-1:~/GN3Parser-beta/4.0-w-mergeHN2 |
|Test      |80.19% |76.20% |merged HN2, Greedy           |gpu-no-1:~/GN3Parser-beta/4.0-w-mergeHN2 |
|Dev       |82.88% |79.15% |merged HN2, Global           |gpu-no-1:~/GN3Parser-beta/4.0-w-mergeHN2 |
|Test      |82.97% |79.05% |merged HN2, Global           |gpu-no-1:~/GN3Parser-beta/4.0-w-mergeHN2 |

