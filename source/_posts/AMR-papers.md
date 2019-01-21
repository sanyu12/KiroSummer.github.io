---
title: AMR-papers
date: 2017-11-20 15:12:10
tags: [AMR]
---
# 简介
新开一篇博客，记录在阅读AMR论文的时候的一些收获。
<!--more-->
# 论文列表以及收获
## Parsing English into Abstract Meaning Representation Using Syntax-Based Machine Translation
本片论文主要采用了SBMT的方法将English sentences转换成AMR。主要的工作在于，SBMT是一个机器翻译的框架，这个框架所需要的是一个Tree，而AMR Graph是一个有向图。所以，需要做一些Transformation：
1. 拆分具有多个节点的节点，但是因为这样子的结构过于“扁平”，所以效果不好
2. 进一步转换，进行 concept reconstruct，role reconstruct等一系列的工作

本文还建立了一个AMR的语言模型，采用了一些外部的语义资料
最终的Smtach FScore: 67%
值得注意的是，在使用了一些外部的tricks (data/number/name rules, semantic categories, morphological normalization, rule-based alignments)之前，该篇工作在2014的Dev上面的F值是62.3%
## Getting the Most out of AMR Parsing
本片论文主要处理了目前AMR Parsing的瓶颈问题：concept identification 和 alignment，本篇论文通过：
1. 建立一个基于双向LSTM的 concept分类器，通过利用丰富的上下文信息学习 AMR concept labels。FCL：对于具有多个 concept node的concept，我们根据 word和 concept leaf节点进行判断，如果 char个数大于4那么就进行 category操作，构成FCL。而对于谓语的情况，我们仅仅利用它的 sense tag? CNN-based Character-level Embedding，为了充分利用 character的信息，本文利用了窗口化的 character + CNN + Max Pooling构成一个词的 character，再加上 word embedding + NER embedding，构成双向 LSTM的input，即 concept identifier的输入。
2. 然后通过扩展一个基于 HMM的 word-to-concept 对齐器，在 AMR Parsing的 decoding阶段起作用。

## CU-NLP at SemEval-2016 Task 8: AMR Parsing using LSTM-based Recurrent Neural Networks
目的：得到怎么处理 FCL中 PREDICATE部分的方法
没有得到解决方案，论文没有那么详细。。
一些收获，在论文提到的评测中：语料是包含了 Alignments的。
## Neural Semantic Parsing by Character-based Translation: Experiments with Abstract Meaning Representations
本文主要采用了机器翻译的技术来处理 AMR Parsing。其中，以 character做为基本单位，OpenNMT为模型，采用的数据是 LDC2016E25。本文还采用了很多其他的辅助方法用来提高这个基于机器翻译技术的 AMR Parsing：
1. AMR Re-ordering：可以用来 argument训练数据
2. Introducting Super Characters：在 character-based技术中，并不完全全部地死板的以 character为单位。像 relation、pos这种信息，以其本身作为 character！
3. 加入词性的信息，但是利用的并不是 stanford pos tagger，而是一个 POS-tagger of the C&C tools (Clark et al.2003)。
4. 加入了称之为 “Silver Standard Data”的额外的训练数据，在所有的提升方法中，这一种方法的提升最大，有10个点的提升。那么什么是 "Silver Standard Data"呢？其实，就是利用现有的模型 (JAMR, CAMR)对数据 the Groningen Meaning Bank (Basile et al. 2012)进行分析，然后通过阈值 (55%)进行提取。最后，通过选取适量 (包括选取 JAMR还是 CAMR产生的 Graph的问题)的数据进行训练语料的扩充，用来达到提升性能的目的，实际效果也是非常好。
5. 对于模型的一些优化方法，设计机器翻译相关的一些专业知识。 
这是第一篇在 LDC2016E25的数据。但是这个模型在 LDC2015E86的数据上面仍然稍微逊色于 5 bi-LSTM (Foland and Martin 2017)。通过这一篇论文，我大致还猜到 2016其实就是 2015数据的训练数据的扩充版本？但是很奇怪的是，这两年的数据现在在 AMR官网上面已经找不到了，目前只剩下了 2014和 2017，称为 1.0和 2.0。

## Abstract Meaning Representation Parsing using LSTM Recurrent Neural Networks
本篇论文采用5个LSTM组成了Parser处理 AMR Parsing问题。下面简单介绍一下该篇论文提出的 Parser的大致流程。
1. 给定一个句子，利用 aligner进行处理，得到 word span和 concept的对应。
2. 利用 word span就可以对每一个 word生成一个{I, O, B, E, S}标签，然后就可以利用这样的数据训练SG Network（SubGraph），子图扩展成为 concept在测试阶段。
3. 预测 Args，Nargs，Attr，NCat四个模型。

在2016的数据上面，该篇论文的F值达到了70.9%.（2016年的评测 semeval 2016 task 8）
