---
title: Syntax-for-SRL
date: 2018-03-19 21:37:25
abstract: emnlp2018
tags: [SRL]
toc: true
---
# 简介
为了 EMNLP2018的工作, 尝试在 SRL的工作中加入句法的信息, 用以提升 SRL的性能.
<!--more-->
# 参考的工作
本工作参考 [deep_srl](https://github.com/luheng/deep_srl). 工作参考了 deep_srl中的神经网络结构, 并且在开源代码的支持下, 很方便的从 theano切换到了 pytoch框架. 在使用 Pytorch重现论文工作的过程中, 还受到了作者的指导, 十分感谢.
# 看过的论文：
[He Highway LSTM Deep SRL](https://homes.cs.washington.edu/~luheng/files/acl2017_hllz.pdf)
[Position Encoding TPF2](https://www.aclweb.org/anthology/D16-1007)
[SDP](http://www.aclweb.org/anthology/D15-1206)
[Attention SRL](https://arxiv.org/pdf/1712.01586.pdf)
[SA-LSTM for SRL](http://www.aclweb.org/anthology/W17-4305)
[Dependency Path Embedding](http://www.aclweb.org/anthology/P16-1113)
[CoNLL-2005 SRL Introduction](http://www.cs.upc.edu/~srlconll/st05/papers/intro.pdf)
# 显著性检验
[显著性检验 ensemble all vs He ensemble || single he vs TPF](/documents/SRL/significance_test.txt)
[显著性检验 baseline vs TreeGRU](/documents/SRL/log_conll05_devel_baseline_and_tree_gru.txt)
[显著性检验 baseline vs SDP](/documents/SRL/log_devel_conll05_baseline_and_sdp.txt)
[显著性检验 baseline vs TPF](/documents/SRL/log_devel_conll05_baseline_and_tpf.txt)
[显著性检验 baseline vs Pattern](/documents/SRL/log_devel_conll05_baseline_and_pattern.txt)
[显著性检验 Test both baseline vs TreeGRU](/documents/SRL/log_test_both_conll05_baseline_ours_and_treegru.txt)
[显著性检验 Test both baseline vs SDP](/documents/SRL/log_conll05_test_both_sdp.txt)
[显著性检验 Test both baseline vs TPF](/documents/SRL/log_conll05_test_both_tpf.txt)
[显著性检验 Test both baseline vs Pattern](/documents/SRL/log_test_both_conll05_baseline_and_pattern.txt)
[显著性检验 Test both baseline w ELMo vs Tree-GRU w ELMo](/documents/SRL/log_test_both_treegru_elmo_compare_baseline_elmo.txt)  高
[显著性检验 Test both baseline w ELMo vs SDP w ELMo](/documents/SRL/log_test_both_sdp_elmo_compare_baseline_elmo.txt)
[显著性检验 Test both baseline w ELMo vs tpf w ELMo](/documents/SRL/log_test_both_baseline_elmo_and_tpf_elmo.txt)
[显著性检验 Test both baseline w ELMo vs pattern w ELMo](/documents/SRL/log_test_both_pattern_elmo_compare_baseline_elmo.txt)
[显著性检验 Test both baseline poe vs tpf poe](/documents/SRL/log_test_both_baseline_pos_and_tpf_poe.txt)
[显著性检验 Test both baseline poe vs four methods poe](/documents/SRL/log_test_both_baseline_poe_and_five_ensemble.txt)
[显著性检验 Test both TPF poe vs four methods poe](/documents/SRL/log_test_both_tpf_poe_compare_four_methods_poe.txt) 有点高
[显著性检验 Test both baseline poe elmo vs tpf poe elmo](/documents/SRL/log_test_both_tpf_poe_and_tpf_elmo.txt) 
[显著性检验 Test both baseline poe elmo vs four methods ensemble elmo](/documents/SRL/log_test_both_baseline_elmo_and_tpf_elmo_append_five_methods.txt) 
[显著性检验 Test both tpf elmo ensemble vs four methods elmo ensemble](/documents/SRL/log_test_both_tpf_elmo_ensemble_compare_four_methods_elmo_ensemble.txt) 还算正常

# 2018-8-4-记录一下 ELMo的相关实验
因为 ELMo的出现，DeepSRL的性能又被往前推了很多，所以我们尝试加入 ELMo，学习一下 ELMo的相关使用方法，顺便看看性能如何。

| __Model__| __Path__| __Dev__| __Test WSJ__| __Test Brown__|
|----------|---------|--------|-------------|---------------|
|DeepATT (FFN)| 论文结果 |83.1  |84.8  |74.1  |
|DeepSRL (re-impl) |141/data/qrxia/DeepSRL-w-ELMO/exp-baseline/ | 81.6 | 82.9 | 72.2 |
|LSGN       |论文结果 |-- |83.9  |73.7  |
|-------  |------  |------ |------- |----- |
|DeepSRL w ELMo (offline) |143~/DeepSRL-w-ELMo/exp-baseline-w-ELMo-hdf5-full-formulation| 85.5 | 86.3 | 74.7 |
|DeepSRL w ELMo + syn label (offline) |126~/DeepSRL-w-ELMo/exp-baseline-w-ELMo-syn-label| 85.6 | 86.0 | 77.1 |
|DeepSRL w ELMo + TPF (offline) |126~/DeepSRL-w-ELMo/exp-baseline-w-ELMo-syn-label| 85.3 | 86.9 | 76.8|
|LSGN w ELMo|论文结果 |-- | 87.4 | 80.4 |

# 开始跑 CoNLL-2012的实验
| __Path__| __实验内容__| __Dev FScore__| __iter__|
|---------|-------------|---------------|---------|
|141/data/qrxia/EMNLP2018/deep_syntactic_for_srl/exp-conll2012-baseline | baseline |   |   |

# 分析 CoNLL2005 SRL结构和 句法结构之间的关系 (2018-4-26)
同时分析了 predicate_argument 在句法树中的相对位置，这里的 predicate_argument 包含了"O"
详细的数据在 [这里](/documents/srl/predicate_argument_frequence.txt)

分析了 predicate_argument_pair (从predicate word 走到 argument word 是否可以在句法树中找到一条父子线) 和 head_modifier_pair之间的重合度。在一条父子线可以找到 predicate-argument
最高达到 [89.46%](/documents/srl/overlapping.txt)， 意味着在所有的有效的 predicate_argument_pair当中，存在着 81.9%能够在 head_modifier中找到，即能够在句法树中找到。

# TPF2 的 Ensemble (5-fold)实验 (2018-5-10)
|__Path__|__实验内容__|__Dev FScore__|__iter__|
|--------|------------|--------------|--------|
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_5fold_0_tpf2_model  |5 fold 0  |80.96%        |417 / 500|
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_5fold_1_tpf2_model  |5 fold 1  |80.71%        |461 / 500|
|kiro@ubuntu14-04:~/Work/Semantic/deep_srl-master/conll05_5fold_2_tpf2_model  |5 fold 2  |80.98%        |482 / 500|
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_5fold_3_tpf2_model  |5 fold 3  |81.08%  |491 / 500|
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_5fold_4_tpf2_model  |5 fold 4  |80.93%  |443 / 500|

# 使用 Gold syntax进行 TPF2 以及 SDP的实验 (2018-5-10)
|__Path__|__实验内容__|__Dev FScore__|__iter__|
|--------|------------|--------------|--------|
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_whole_tpf2_model_gold_syntax  | gold syntax for tpf2 |  87.75% |443 / 500 |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_whole_sdp_model_gold_syntax  | gold syntax for sdp |      |      |


# 根据新架构的实验 (2018-5-1)
|__Path__|__实验内容__|__Dev FScore__|__iter__|
|--------|------------|--------------|--------|
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_train_model/          |2w Train Baseline old architecture | __72.04%__    |    |
|kiro@ubuntu14-04:~/Work/Semantic/deep_srl-master/exp-new-architecture-baseline/          |2w Train Baseline | __71.39%__    |        |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/exp-new-architecture-baseline          |2w Train Baseline in Server 141 | 71.35% |      |
|kiro@ubuntu14-04:~/Work/Semantic/deep_srl-master/exp-new-architecture-baseline-w-bucket  |2w Train Baseline w bucket| 71.11% (w viterbi 73.28%)  | 211 / 261      |
|kiro@ubuntu14-04:~/Work/Semantic/deep_srl-master/exp-new-architecture-baseline-w-bucket-outer-random  |2w Train Baseline w bucket and outer random | 71.09%  | 220 / 270      |
|kiro@ubuntu14-04:~/Work/Semantic/deep_srl-master/exp-new-architecture-baseline-w-bucket-viterbi  |2w Train Baseline w bucket viterbi| __73.08%__   | 155 / 205  |

1. 新的架构的模型的效果比不上之前的 Baseline， 因为新的架构有一个操作是 50次评价不更新， 就直接杀掉程序，所以效果并不好，停留在了 383次迭代 (71.59%，是old architecture的效果)
2. 加入了 bucket，速度确实能够得到很大的提升，从原来的2min30s -> 1min10s ，粗略估计，个人台式机 1080Ti
3. 因为在 Train过程中，使用 viterbi解码的结果作为评判标准，从结果上来看，会损失 0.2%个点。
4. 给 Bucket加入了桶之间的随机，发现结果还是和不加桶之间的随机差不多，基本一致。依旧不如 Baseline.

# deep srl 架构图
![deep_srl](/images/srl/highway-example.png)

# 我的实验的测试记录 (2018-5-14)

|__Path__|__内容__|__Dev Precision__|__Dev Recall__|__Dev FScore__|__Dev Comp.__|__Test WSJ Precision__|__Test WSJ Recall__|__Test WSJ FScore__|__Test WSJ Comp.__|__Test Brown Precision__|__Test Brown Recall__|__Test Brown FScore__|__Test Brown Comp.|__Test Both P__|__Test Both R__|__Test Both F__|
|--------|--------|-----------------|--------------|--------------|----------------------|-------------------|----------------|------------------|-------------------|-----------------|-------|-------|------|
|Paper |He __POE__|83.1%  |82.4%   |82.7% |64.1% |85.0%  | 84.3%  | 84.6%  |66.5%|74.9%  | 72.4% |73.6% |46.4| - | -  | __83.2%__ |
|Paper |He __Single__|81.6%  |81.6%   |81.6% |62.3%|  83.1%  | 83.0%  | 83.1%  |64.3%|72.9%  | 71.4% |72.1% |44.8%| - | -  |81.6% |
|141:...exp-conll05-syn-label-predict |syntactic label 测试|82.46%  |82.85%   |82.66% |63.55%|  83.58%  | 83.70%  | 83.64%  |65.45%|73.19%  | 71.98% |72.58% |45.65%|82.21% |82.13%  |82.17% |
|n141:...exp-conll05-tpf2-predict |TPF2 测试|82.77%  |82.20%   |82.48% |63.21%|  84.32%  | 83.78%  | 84.05%  |65.86%|73.68%  | 72.03% |72.85% |45.52%|82.92% |82.21%  |82.56% |
|n141:...exp-conll05-whole-tpf-syn-label |TPF2 and Syn label|82.39%  |82.61%   |82.50% |63.73%|  84.04%  | 83.91%  | 84.98%  |65.65%|73.58%  | 72.67% |73.12% |47.26% |82.65% |82.40%  |82.53% |
|n143:...exp-conll05-tree-gru-predict |Tree-GRU 测试|82.71%  |82.78%   |82.75% |63.70%|  83.92%  | 83.59%  | 83.75%  |65.22%|72.90%  | 71.66% |72.27% |44.90%|82.46% |81.99%  |82.22% |
|n143:...exp-conll05-whole-sdp-predict |SDP 测试|82.60%  |82.47%   |82.53% |64.01%|  84.21%  | 83.86%  | 84.03%  |65.86%|73.96%  | 72.03% |72.98% |45.27%|82.86% |82.28%  |82.57% |
|n143:...exp-conll05-whole-pattern-predict |pattern |82.50%  |82.47%   |82.49% |62.93%|83.70%  | 83.84%  | 83.77%  |65.26%|73.40%  | 72.49% |72.94% |46.14%| 82.34% | 82.32%  | 82.33% |
|n141:...exp-ensemble-scores-predict |syntactic label + TPF2|84.15%  |83.58%   |83.87% |65.67%|  85.23%  | 84.93%  | 85.08%  |67.65%|75.82%  | 73.91% |74.85% |48.76%|84.00% |83.45%  |83.72% |
|n141:...exp-ensemble-scores-predict(no pattern) |ensemble all four|84.61%  |84.03%   |84.32% |66.72%|85.67%  | 85.37%  | 85.52%  |68.43%|76.53%  | 74.41% |75.45% |49.13%| __84.47%__ | __83.91%__  | __84.19%__ |
|n141:...exp-ensemble-scores-predict(all) |ensemble all five|84.57%  |84.04%   |84.30% |66.41%|85.79%  | 85.48% | 85.63%  |68.71%|76.26%  | 74.51% |75.37% |49.25%| __84.54%__ | __84.01%__  | __84.27%__ |
|n143:...exp-conll05-whole-tpf2-gold-syntax-predict |tpf2 gold syntax|88.31%  |88.41%   |88.36% |72.91%| 89.60%| 89.62% |89.61% | 75.05% |80.27%|  79.24%|  79.75%| 55.72% |88.36% |88.23%  |88.30%  |
|n143:...conll05_5fold_0_tpf2_model |tpf2 5fold 0 |81.95%  |81.99%   |81.97% |62.38%| 83.55%| 83.43% |83.49% | 65.22% |73.02%|  71.98%|  72.50%| 45.27% |82.15% |81.90%  |82.03%  |
|n143:...conll05_5fold_1_tpf2_model |tpf2 5fold 1 |81.74%  |81.33%   |81.54% |61.67%| 83.46%| 82.94% |83.20% | 64.25% |72.85%|  71.11%|  71.97%| 44.53% |82.06% |81.35%  |81.70%  |
|kiro:...conll05_5fold_2_tpf2_model |tpf2 5fold 2 |82.00%  |81.86%   |81.93% |62.35%| 83.10%| 83.02% |83.06% | 64.50% |72.40%|  70.74%|  71.56%| 44.15% |81.70% |81.38%  |81.54%  |
|n143:...conll05_5fold_3_tpf2_model |tpf2 5fold 3 |82.31%  |81.72%   |82.01% |62.38%| 83.46%| 82.89% |83.17% | 64.44% |73.77%|  71.43%|  72.58%| 45.40% |82.19% |81.36%  |81.77%  |
|n143:...conll05_5fold_4_tpf2_model |tpf2 5fold 4 |82.16%  |81.51%   |81.84% |61.61%| 83.94%| 83.15% |83.54% | 64.95% |72.14%|  70.28%|  71.20%| 43.91% |82.38% |81.43%  |81.90%  |
|n141:...exp-POE-tpf2-scores-predict|tpf2 POE     |84.01%  |83.39%   |83.70% |65.09%| 85.59%| 85.01% |85.30% | 68.05% |75.89%|  73.37%|  74.79%| 48.13% |84.31% |83.50%  |83.91%  |

|__Path__|__内容__|__Dev Precision__|__Dev Recall__|__Dev FScore__|__Dev Comp.__|__Test WSJ Precision__|__Test WSJ Recall__|__Test WSJ FScore__|__Test WSJ Comp.__|__Test Brown Precision__|__Test Brown Recall__|__Test Brown FScore__|__Test Brown Comp.|__Test Both P__|__Test Both R__|__Test Both F__|
|--------|--------|-----------------|--------------|--------------|----------------------|-------------------|----------------|------------------|-------------------|-----------------|-------|-------|------|
|n141:...exp-baseline-w-ELMo-hdf5-full-formulation|w ELMo  |85.42%  |85.56%  |85.49%|68.04%| 86.36% |86.21% |86.29%  | 69.43%|75.15%|  74.32%|  74.73% | 48.13% |84.87% |84.63%  |84.75%  |
|n126:...exp-baseline-w-ELMo-syn-label|w ELMo + syn label |85.55%  |85.66%  |85.60%|68.17%| 86.07% |85.97% |86.02%  | 68.96%|77.61%|  76.57%|  77.09% | 51.12% |84.95% |84.71%  |84.83%  |
|85.36 n126:...exp-baseline-w-ELMo-TreeGRU|w ELMo + TreeGRU |85.74%  |85.63%  |85.69%|68.20%|86.16%|86.16% |86.16% |68.86%|77.85%|  75.56%|  76.69% | 50.75% |85.07% |84.74%  |84.90%  |
|85.40 n126:...exp-baseline-w-ELMo-SDP    |w ELMo + SDP     |85.61%  |85.66%  |85.63%|68.75%|86.89%|86.67% |86.78% |70.17%|77.97%|  76.25%|  77.10% | 52.36% |85.71% |85.27%  |85.49%  |
|n126:...exp-baseline-w-ELMo-TPF|w ELMo + TPF         |85.45%  |85.12%  |85.28%|67.89%      | 87.03% |86.76% |86.89%  | 70.40%|77.63%|  75.88%|  76.75% | 51.62% |85.79% |85.30%  |85.55%  |
|n126:...exp-baseline-w-ELMo-TPF-Gold-syntax|w ELMo + TPF Gold syntax|90.14%  |89.54%  |89.84%|75.40%   | 91.07% |91.04%|91.06%| 77.48%|82.30%|  82.04%|82.17% | 59.45%|89.90% |89.84%  |89.87%  |
|n126:...exp-baseline-w-ELMo-pattern|w ELMo + pattern |85.53%  |85.44%  |85.49%|68.17%      | 86.51% |86.31% |86.41%  | 69.62%|77.36%|  76.44%|  76.89% | 51.49% |85.29% |84.98%  |85.13%  |
|n141:...exp-ensemble-scores-predict|ensemble four w elmo TPF |86.53%  |86.07%  |86.30% |69.74%    | 87.62% |87.31% |87.46%  | 71.52%|78.81%|  77.40%|  78.10% | 53.48%|86.46% |85.98%  |86.22%  |
|n141:...exp-ensemble-scores-predict|ensemble TPF + elmo TPF |86.32%  |85.74%  |86.03% |69.33%  | 87.51% |87.02% |87.26%  | 71.12%| 78.55%|  76.53%|  77.52% | 52.49%|86.33% |85.62%  |85.97%  |
|n126:...exp-baseline-5-fold-0 |baseline 5fold 0  |80.68%|80.55%|80.62%|60.41%	|82.33%|82.29%|82.31%|62.94%	|70.79%|69.13%|69.95%|41.67%	|80.82% |80.53%  |80.67%  |
|n126:...exp-baseline-5-fold-1 |baseline 5fold 1  |81.08%|80.64%|80.86%|61.18%	|82.41%|81.83%|82.12%|62.31%	|72.30%|70.97%|71.63%|44.90%	|81.07% |80.37%  |80.72%  |
|n126:...exp-baseline-5-fold-2 |baseline 5fold 2  |81.08%|80.40%|80.74%|61.11%	|82.61%|81.89%|82.24%|62.41%	|71.04%|69.41%|70.21%|41.04%	|81.08% |80.21%  |80.64%  |
|n126:...exp-baseline-5-fold-3 |baseline 5fold 3  |80.61%|80.41%|80.51%|59.98%	|82.34%|81.94%|82.14%|62.46%	|72.42%|69.73%|71.05%|43.16%	|81.05% |80.31%  |80.68%  |
|n126:...exp-baseline-5-fold-4 |baseline 5fold 4  |80.41%|80.81%|80.61%|60.16%	|81.81%|81.44%|81.62%|61.65%	|71.07%|69.50%|70.27%|40.92%	|80.39% |79.84%  |80.11%  |
|n126:...exp-baseline-POE      |baseline 5fold    |83.05%|82.47%|82.76%|64.16%	|84.63%|84.00%|84.31%|66.36%	|74.90%|72.12%|73.48%|46.14%	|83.36% |82.41%  |82.88%  |
|n126:...exp-ensemble |baseline 5fold ensemble baseline ELMo|86.26%|86.16%|86.21%|69.55%|87.20%|86.79%|86.99%|70.80%|77.67%|75.75%|76.70%|50.37%|85.94%|85.31%|85.63%|
|n126:...exp-ensemble-five-2... |ensemble 5 methods w ELMo 3|86.99%|86.92%|86.95%|71.09%|87.95%|87.64%| __87.80%__|72.24%|79.65%|78.04%|78.84%|53.23%|86.87%|86.37%|86.62%|


__备注__：ensemble w elmo TPF: 0.5 0.1 0.1 0.1 0.1 0.1

past process results.
|n126:...exp-ensemble-five-... |ensemble 5 methods w ELMo|87.07%|86.77%|86.92%|70.75%|87.97%|87.55%|87.76%|72.13%|79.56%|77.95%|78.75%|53.48%|86.87%|86.27%|86.57%|
|n126:...exp-ensemble-five-2... |ensemble 5 methods w ELMo 2|86.95%|86.89%|86.92%|70.84%|87.91%|87.58%|87.74%|72.11%|79.52%|78.14%|78.82%|53.61%|86.80%|86.31%|86.55%|
### 按照 Dev试试调整一下 ensemble的系数

|		 | __Baseline 5fold ensemble ELMo__| __TPF 5fold ensemble ELMo__|
|--------|---------------------------------|----------------------------|
|0.1  0.5|86.21%  / 86.99%				   |86.03%  /  87.26%           |
|0.1  0.8|85.93%  / 86.99%				   |85.92%  /87.28%             |
|0.15 0.8|86.09%  / 87.05%                 |86.11%  /  87.29%           |

# 编写论文使用到的一些技巧
### vim 拼写检查
```
:set spell spelllang=en_us
:set nospell
```
# 使用原版代码跑出来的实验结果
测试集分为 WSJ, Brown, -Combined-

|__路径__|__说明__|__Dev FScore__|__Dev FScore w constrain__|__Test FScore__|__Test FScore w constrain__|
|--------|--------|----------|------------------------|---------------------|---------------------------|
|-- |论文结果  |大约80.1%, 从图表看出,并未直接给出结果  |81.6%   |              | 83.1%/72.1%/81.6%          |
|gpu-no-1:~/deep_srl-master/conll05_model |代码结果  |81.01%  |82.08%  |         |          |
|ubuntu14-04:~/Work/Semantic/deep_srl-master/conll05_model          |Pytorch重现结果|80.47%     |81.53%     |    |83.19%/71.57%/81.64%      |

# 进行句法信息第一步: Biaffine 隐层信息
## 5-fold获取PTB Train的自动句法结果 (2018-3-22)
|__路径__|__n-fold__|__Dev FScore (UAS/LAS)__|__Test FScore (UAS/LAS)__|
|--------|----------|--------------|---------------|
|gpu-no-1:~/BiaffineParser-pytorch-new/experiments/ptb_model_fold_0        |0-7965         |95.51%/93.60%       |95.54%/93.54%            | 
|gpu-no-1:~/BiaffineParser-pytorch-new/experiments/ptb_model_fold_1        |7966-15931     |95.59%/93.77%      |95.61%/93.68%    | 
|gpu-no-1:~/BiaffineParser-pytorch-new/experiments/ptb_model_fold_2        |15932-23897         |95.39%/93.46%       |95.44%/93.50%         | 
|gpu-no-1:~/BiaffineParser-pytorch-new/experiments/ptb_model_fold_3        |23898-31863         |95.42%/93.43%      |95.36%/93.36%           | 
|gpu-no-1:~/BiaffineParser-pytorch-new/experiments/ptb_model_fold_4        |31864-39831         |95.54%/93.71%   |95.37%/93.40%     | 

其中: Test数据集是5-fold当中, 剩下的那一份数据. 在实验的合并阶段, 发现 Biaffine代码的输出中包含了 "unk"字段替换了原先的字段, 词性部分也是省略了一列. 所以利用原本的 train数据, 和生成的自动弧和标签的 train数据进行了合并的操作, 进行接下来的5-fold模型的训练. 另外一个小的测试: Train集合的封闭测试: UAS 98.25%

接下来的工作是: 抽取语料中句子对应的 LSTM output.
## 分析CONLL05 SRL的数据和 PTB 句法的数据构成关系
* CONLL05 SRL: Train 36085
* CONLL05 SRL: Dev 1240
* CONLL05 SRL: Test Brown/WSJ/Total 361/2156/2517
* PTB: Train 39832
* PTB: Dev 1700
* PTB: Test 2416

其中, Train训练集合: PTB完全包含了 SRL; Dev集合和 PTB __完全没有__ 重合的部分; Test集合中 WSJ在 PTB的 Test里面可以完全找到, 但是 Brown完全没有.
PTB 句法:2-21 train; 22 devel; 23 test; (2018-5-4)
因为句法的数据中不包含 wsj24的部分，所以只能通过使用 stanford parser进行获取，经过2个小时的研究，终于给跑出来了。记录相关日志如下：
* 在本机上进行 stanford parser的运行，路径：kiro@ubuntu14-04:~/Work/DependencyParsing/stanford-parser-full-2013-11-12
* 执行的命令是：java -cp "*" -mx1g edu.stanford.nlp.trees.EnglishGrammaticalStructure -basic -keepPunct -conllx -treeFile wsj_24.mrg > wsj_24.conll.punct
* 需要注意的是，PTB的数据文件是 LDC1999T42，而不是 PennTreenbankv2

### Train, Test-wsj的自动 dep和 Biaffine LSTM Representation的获取 (2018-3-24)
因为在上述的分析中, SRL CONLL05的 Train (PTB Train 5-fold model) 和 Test-wsj (PTB Train model) 是 PTB的子集, 所以可以从 PTB的子集中进行抽取, 抽取的数据存在以下目录:
* autodep: gpu-no-1:~/EMNLP2018/PTB_CONLL05_analysis/conll05_autodep/
* lstm representation: gpu-no-1:~/EMNLP2018/PTB_CONLL05_analysis/conll05_biaffine_lstm_representation/

### 处理 CONLL05的数据 Dev, Test-brown (2018-3-25)
1. 首先抽取 Dev, Test-brown的文本数据
2. 利用 Stanford POSTagger-2017-06-09 + models/english-bidirectional-distsim.tagger 进行词性标注
3. 利用获取到的词性, 进行 BiaffineParser (PTB Train model)的分析, 得到: 自动依存句法+LSTM Representation

数据保存在如上路径

## 开始跑 Biaffine的 LSTM 句法信息的实验 (2018-3-26)
读取 Biaffine的 LSTM的代码已经书写完毕, 并且添加了检查功能, 确保读取的 Biaffine LSTM Out能和 CONLL05的句子对应上.现在开始跑实验, 但是目前有一个问题就是 __Biaffine LSTM维度太高:800__ 我们可能需要利用 Linear Projection将它降维, 变成一个合理的维度, 就像张老师的论文一样. 但是从目前的结果来看, 出现了一个非常奇怪的现象: Train集合可以和往常一样正常收敛, 但是 Dev上的效果至始至终没有太大的变化, 暂时不知道是什么原因导致的, 正在分析原因. (目前打算将 800维度降维至 200)
### 直接利用 Biaffine LSTM output + Softmax进行的实验 (2018-3-27)
实验结果表示, 结果很差, 从输出的结果 (经过了log_softmax)来看, 就是 O 所对应的位置的得分最高, 为-0.*左右, 其他的几乎全部集中在-4及以下, 这是一个很奇怪的现象. __按道理:__ 应该Train集合能够收敛 loss, Dev的结果不应该是这么差, 正在排查原因.
发现了一个非常诡异的现象:
1. 我直接输出了 LSTM的浮点数信息, 但是居然在文件中 egrep不到???查到了一个可能的问题,  Biaffine LSTM的文件中, 有小数点后18位, 但是只保留了11位, 在numpy读取的时候. 乌龙: 其实是一样的, 只不过是输出精度的问题.原本我以为我想错了, 可是 Batch之后输出出来在 LSTM文件中还是查找不到??
2. 第二个问题: 为什么在连续的 LSTM Out中, 会有 全是零的存在? 原来是自己制造的乌龙: LSTM Minus

__好了__ 哈哈哈! 为什么这么说呢, 因为在 Dev的封测上面, 利用 Biaffine 的 LSTM Output 能够达到99.84%的 F值 (貌似还在继续上涨, 直接kill掉, 目标不是这个), 算是可以了. 接下来就是用 Train训练集试试看, 看看结果如何! 至于是怎么调试好的, __尘归尘, 土归土__:)
悲伤, Train集合训练, 在 Dev上面还是不行. 但是有一个非常奇怪的地方: 在利用 Train封闭测试得到的 LSTM Output上得到的模型, Dev目前可以达到 58% FScore; 但是切换到 5-fold的Train LSTM Output, Dev就不可以了, FScore还是只有0.几.
### 利用 TreeLSTM (2018-3-30)
在张梅山老师的代码基础之上, 需要稍做修改就可以进行我们的 SRL的实验. 目前采用的方式是直接利用 TreeLSTM的输出替换掉原本 Model的输出, 直接进行实验.
实验记录:

|__Path__|__实验内容__|__Dev FScore__|
|--------|------------|--------------|
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_tree_lstm_model |TreeLSTM + 2 Highway BiLSTM |因为设备不够用, 已经 kill, 效果也不行    |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_tree_lstm_model |TreeLSTM + 4 Highway BiLSTM |79.36%, 运行了268次迭代, 设备不够用, 已经kill    |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_tree_lstm_4_layers_model |TreeLSTM + 8 Highway BiLSTM |    |

### 利用 Syntactic Label (2018-3-31)
直接利用 Biaffine Parser的句法输出结果, 以 Embedding的形式加入到 神经网络的输入中, 以这种最简单直接的方式试一试效果.

|__Path__|__实验内容__|__Dev FScore__|
|--------|------------|--------------|
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_syn_label_model/ | Input Embedding + auto syntactic label embedding | __81.75%__    |

从以上的结果来看, 即便是这样子基本的句法信息, 也是能够产生很好的效果, 这里的 FScore还是w/o constrain
### 利用 TPF2 (2018-4-26)
|__Path__|__实验内容__|__Dev FScore__|
|--------|------------|--------------|
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_whole_tpf2_model/ | Input Embedding + tpf2 embedding | __81.57%__    |

### 利用 SDP (2018-4-26)
|__Path__|__实验内容__|__Dev FScore__|
|--------|------------|--------------|
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_whole_sdp_model  |SDP | __81.68%__   |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_whole_sdp_model_gold_syntax  | SDP with gold syntax |    |

### 利用 Pattern的实验 (2018-5-7)
|__Path__|__实验内容__|__Dev FScore__|
|--------|------------|--------------|
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/exp-conll05-whole-pattern | Input + Pattern representation | __81.57%__|

### 加入 Bucket
为了加速的效果, 加入 Bucket, 1w Train的速度由 5:50 降低到了 4:46
## 因为速度的问题, 现在开始 2w Train的实验
### Baseline以及其他的一些实验 (2018-4-6)

|__Path__|__实验内容__|__Dev FScore__|
|--------|------------|--------------|
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_train_model/          |2w Train Baseline | __72.04%__    |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_tpf2_model            |2w Train with TPF2 | __75.92%__    |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_only_syn_label_model  |2w Train with syntactic label | __74.31%__ |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_syn_label_model       |2w Train with syntactic label + PE | 73.89% |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_syn_label_tree_lstm_model  |2w Train with syntactic label + TreeLSTM | __75.87%__ |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/exp-conll05-2w-pattern  |2w Train with Pattern | __76.50%__ |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_sdp_model       |2w Train with SDP | __76.76%__ |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_tree_lstm_model       |2w Train with syntactic TreeLSTM |72.02% |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_highway_tree_lstm_mean_model       |2w Train with syntactic Highway TreeLSTM |72.00% |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_tree_lstm_model       |2w Train with syntactic TreeLSTM w sorted training corpus |71.74% |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_pool_tree_lstm_model  |2w Train with syntactic TreeLSTM (max pooling node forward) |72.35% |

### 跟着张老师做实验 (from 2018-4-11)
现在的工作转向于试图改变 Baseline的结构, 从而获取更快的速度.

|__Path__|__实验内容__|__Dev FScore__|
|--------|------------|--------------|
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_train_model/          |2w Train Baseline | __72.04%__    |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_baseline_highway_mlp_output_model          |2w Train Baseline + mlp + output | __72.24%__   |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_baseline_minus_model  |2w Train Baseline-Minus, 取消 predicate embedding |54.31% |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_baseline_concate_minus_model  |同line3 + output layer concate(h_i - h_p, hi) |56.24% |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_minus_concate_nonlinear_model  |同line4 + nonlinear layer    |66.76%|
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_concate_minus_predicate_model  |同line3 + output layer concate(h_i - h_p, hi, predicate_embedding)  |56.09% |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/conll05_2w_baseline_m_biaffine_model  |同line3 + output layer Biaffine Layer    |67.80% |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/exp-conll05-2w-biaffine-sentence-level-predicates  |sentence level predicates + Biaffine Layer    |67.20% 待续  |
|qrxia@n141:~/EMNLP2018/deep_syntactic_for_srl/exp-conll05-2w-biaffine-layer-3-mlp/conll05_model  |同2 + 3 layer mlp + Biaffine Layer    |65.32% |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/exp-conll05-2w-biaffine-layer    |2w Train Biaffine Layer w baseline input MLP size 100|71.96% |
|qrxia@n143:~/EMNLP2018/deep_syntactic_for_srl/exp-conll05-2w-biaffine-layer-200    |2w Train Biaffine Layer w baseline input w MLP size 200 |71.14% |

实验结果：
1. 在 Baseline的 highway后加了一层 Linear Layer。 效果稍有提高 + 0.2%， 但是如果是全部数据，实验结果就不确定了，全部数据可能会有补缺短板的功能。
2. 尝试着简化输入，input layer仅仅是 word embedding：1) h_i - h_p : 54.31; 2) concate(h_i - h_p, h_i) 56.24%; 3) concate(h_i - h_p, h_i, i_predicate_embedding) : 56.09%。通过取消 softmax layer，改换以上三种方式的预测 layer，结果都不如人意
3. concate(h_i - h_p, h_i) + NonLinear Layer + Softmax Layer， 效果接近于 MLP + Biaffine Layer 66.76% vs 67.80%
4. Baseline 和 Baseline + Biaffine Layer的效果基本一致：72.04% vs 71.96%, 相差 0.9%； 但是在全部数据上，Biaffine的效果要比 Baseline高0.3%. 可能是数据量的原因？导致Biaffine的效果不能很好地学习到？
5. 尝试通过增加 MLP的层数来模拟 Highway的层数的功能，实验效果并不好：65.32% 相比较于一层 MLP + Biaffine：67.80%
6. 增加 MLP的 HiddenSize的实验也是没有明显效果的：71.14%
7. 尝试通过加入 sentence level predicate embedding + Highway + MLP + Biaffine 但是还是不行：67.20%

[conll05-label分布](/documents/srl/label_freq.txt)

### 调查105个 SRL Label是什么意思? (2018-4-13)
O:	不在语义框架之内
V, A0, A1, A2, A3, A4, A5
AM-LOC, AM-MNR, AM-TMP, AM-NEG, AM-MOD, AM-DIS, AM-EXT, AM-ADV, AM-PNC, AM-DIR, AM-PRD, AM-CAU, AM-REC, AM-TM, AM, AA
其中, 以上每一个标签都有两个组合 __R-\*__, __C-\*__, 例如: R-AM-LOC, C-AM-LOC..., 分别表示 __r__eference, __c__ontinuation, 表示对\*的一种引用; 这种组合可以看成是一个独立的标签 
另外: 有两个标签可以与以上进行组合, __B, I__: __b__egin, __i__nternal, 每一个标签都能有 2种组合 (B-\*, I-\*) 的可能. B, I的作用不言而喻
![一个C-*的列子](/images/srl/srl-c.png)

#### 一个奇怪的现象 (2018-4-16)
在李老师发现的他跑的实验会比我跑的实验少一个点的情况下, 我尝试了恢复原本的代码, 一块一块的恢复, 发现最终的问题居然出现在 hidden\_drop初始化的部分, 简直匪夷所思.
不过我猜想这个对最终的实验结果应该不会有影响.
# 这个工作的心得：
总的来讲，这个工作旨在利用句法的信息来帮助语义角色标注的工作。
在这里，我主要记录一下自己写论文时候的一些想法。
1. 于我而言，写论文中最难的部分莫过于 abstract, introduction, related work and conclusion.
2. 对于 abstract，是论文中很重要的部分：总结论文的工作，给出“摘要”
3. 对于 introduction，介绍任务，简单介绍本文的动机，任务的发展呢
4. 对于 related work，充分体现了自己对于领域内他人工作的熟知程度，更加的体现了自己在阅读论文中记录的多少。
