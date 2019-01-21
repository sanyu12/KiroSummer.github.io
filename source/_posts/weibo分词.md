title: weibo分词
date: 2016-05-23 18:07:00
tags: [word segmentation]
---
# 微博分词工作记录
新的工作开始了，新开一个页面记录工作！好好工作，好好生活。
<!--more-->
# 微博数据处理（信息检索课程用）
对源数据（老师给的微博数据）进行处理，源数据一共58384行
```
>>>wc -l raw.txt
>>>58384
```
对数据中的网址链接进行处理，替换掉所有的网址，换成"URL/NN"；替换掉所有的email address，换成"EMAIL/NN"
```
>>>sed 's/http:[^[:space:]]*/URL\/NN/g' raw.txt > raw_no_URL.txt
>>>sed -r 's/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b/EMAIL\/NN/g' raw_no_URL.txt > raw_no_URL_EMAIL.txt
```
而后对文件中的所有的特殊符号进行加空格处理
```
>>>sed  's/#/ # /g' $1 | sed 's/@/ @ /g' | sed 's/\[/ \[ /g' | sed 's/\]/ \] /g' | sed 's/\/\//\/\/\//g' | sed 's/↓↓/ ↓↓ /g' > sentences.txt
```
到目前为止就得到了可以使用[苏大HLT实验室分词demo工具](http://hlt-la.suda.edu.cn)进行分词、词性的处理，然后使用websocket使用实验室的分词处理，最后根据要求提取出需要的sentences。
[websocket调用demo进行分词处理](/documents/weibo_seg/echo_client.py)
出现任务的频率：
大于50个的，提取5个
20～50个的，提取4个
4~20个的， 提取3个
2～3个的， 提取2个
[根据要求提取任务](/documents/weibo_seg/extract_sentences_and_seg_words.py)
# 1 正式处理NLPCC2016数据，2016-7-02 更
### 1.1 使用wspos-tagger试着处理NLPCC2016微博数据
分别使用CTB7、NLPCC分词数据 + CRF模型进行训练，得到以下准确率。迭代__30__次终止。数据仅供参考。。

|             |__CTB7 dev/test__|__NLPCC2016 dev__|
|-------------|-----------------|-----------------|
|CTB7数据模型 |96.13%/95.57%    |91.77%           |
|NLPCC数据模型|90.86%/90.82%    |94.33%           |

### 1.2 使用172::8200分词demo(<font color=red>模型训练出错、待修正</font>)
进行NLPCC2016的train和dev的数据处理，得到的准确率(accuracy)如下

|__train__|__dev__|
|---------|-------|
|92.43%/<font color=red>93.40</font>   |91.62%/<font color=red>92.39</font> |

### 1.3 使用171:~/wsw-tagger，使用NLPCC2016 weibo数据进行跑模型，__close__得到的准确率如下：

|__epoch__|__dev__|
|---------|-------|
|209      |94.67% |
和wspos-tagger对比，就数据上来看，有点提高。但是，ws-tagger跑了209词迭代，而wspos-tagger只跑了30次迭代。
### 1.4 ws-tagger分别使用lexicon、guide、lexicon + guide 实验
__lexicon__: 在模型的训练过程中，加入词典文件(large-dict.txt, 428101个词)，在初始的CRF模型当中新加入一些词典组成的特征
__guide__: 同样使用上述的[苏大hlt-lademo](http://hlt-la.suda.edu.cn)对NLPCC的train、dev、test进行分词词性的处理，然后将得到的分词词性结果作为"guide"合并到NLPCC数据当中，数据格式如下：
```txt
1   回  _   B   B@VV    _   _   _   _   _
2   首  _   E   E@VV    _   _   _   _   _
3   来  _   S   S@VV    _   _   _   _   _
4   时  _   S   S@LC    _   _   _   _   _
5   的  _   S   S@DEG   _   _   _   _   _
6   路  _   S   S@NN    _   _   _   _   _
```
使用合并的数据进行模型的训练以及测试
__guide+lexicon__: 在使用guide的数据的同时，还使用字典文件


|__epoch__|__dev__|__lexicon dev__|__guide E@NN dev__|__guide E dev__|__lexicon + guide dev __|__CTB7 crf guide dev__|
|---------|-------|---------------|------------------|---------------|------------------------|----------------------|
|1        |88.48% |90.78%         |93.82%            |93.56%         |94.64%                  |92.56%                |
|2        |90.54% |92.25%         |94.39%            |94.07%		 |95.24%       			  |92.88%                |
|3        |91.61% |92.97%         |94.46%            |94.30%		 |95.34% 				  |93.21%                |
|4        |92.11% |93.36%         |94.60%            |94.61%         |95.58%                  |93.37%                |
|20       |94.04% |94.91%         |94.96%            |94.86%         |95.84%                  |94.11%                |
|40       |94.42% |95.38%         |95.03%(over)      |94.97%         |95.97%                  |94.29%                |
|60       |94.27% |95.42%         |                  |95.05%(over 123)|__95.97%(over 35)__    |94.26%                |
|         |94.67%(209 over)  |95.74%(413 over)|                 |               |                        |94.41%(123(over))    |

### couple模型 172:~/coupled-ws-tagger
couple模型:
一个使用了NLPCC数据+CTB7数据
另外一个使用了NLPCC数据+CTB7数据+PKU数据
#### couple模型的数据格式
__NLPCC__数据格式:
```text
1   回  _   B^* _   _   _   _   _   B^b_B^m_B^e_B^s
2   首  _   E^* _   _   _   _   _   E^b_E^m_E^e_E^s
3   来  _   S^* _   _   _   _   _   S^b_S^m_S^e_S^s
4   时  _   S^* _   _   _   _   _   S^b_S^m_S^e_S^s
5   的  _   S^* _   _   _   _   _   S^b_S^m_S^e_S^s
6   路  _   S^* _   _   _   _   _   S^b_S^m_S^e_S^s
```
__CTB7__、__PKU__的数据格式:
```text
1   中  _   *^b _   _   _   _   _   B^b_M^b_E^b_S^b
2   国  _   *^e _   _   _   _   _   B^e_M^e_E^e_S^e
3   最  _   *^b _   _   _   _   _   B^b_M^b_E^b_S^b
4   大  _   *^e _   _   _   _   _   B^e_M^e_E^e_S^e
```

|__epoch__|__weibo + CTB7__|__weibo + CTB7 + PKU__|
|---------|----------------|----------------------|
|1        |91.74%          |92.31%                |
|2        |92.69%          |93.24%                |
|3        |93.59%          |93.87%                |
|4        |93.97%          |94.35%                |
|20       |95.41%          |95.51%                |
|40       |95.67%          |95.54%                |
|60       |95.79%          |95.88%                |
|80       |95.88%          |95.98%                |
|81       |96.01%(over)    |96.06%/135 96.10%/190(over)|

### 使用最好的模型进行结果的对比(2016-7-5-晚间更新！)
#### gold:nlpcc2016 dev
使用nlpcc2016 dev数据作为gold，分别测试baseline等模型的accurcy。其中，viterbiMerge是使用 viterbi算法+一定的规则 计算四种模型的最优BIES路径，融合这四种模型的结果。
四种模型：lexicon, guide+lexicon, couple, couple+pku。得到最后一列的数据"viterbiMerge"。
其中，规则纠正是利用规则对标注不对的BIES进行纠正，例如"BB"就属于一个不对的BIES标记。

|                  |__baseline__|__lexicon__|__guide+lexicon__|__couple__|__couple+pd__|__viterbiMerge__|
|------------------|------------|-----------|-----------------|----------|-------------|-------------|
|未纠正(accuracy)  |94.67%      |95.74%     |95.97%           |96.01%    |95.98%/96.10%|96.14%/__96.22%__   |
|规则纠正(accuracy)|94.60%      |95.73%     |95.95%           |96.01%    |95.98%/96.08%|             |
|P(未纠正)         |93.30%      |94.45%     |94.77%           |94.74%    |94.78%/94.80%|95.03%/95.10%       |
|R(未纠正)         |93.99%      |95.31%     |95.53%           |95.61%    |95.56%/95.82%|95.72%/95.84%       |
|F(未纠正)         |93.65%      |94.88%     |95.15%           |95.17%    |95.17%/95.30%|95.37%/__95.47%__   |
|p(规则纠正)       |93.30%      |           |                 |          |             |             |
|R(规则纠正)       |93.99%      |           |                 |          |             |             |
|F(规则纠正)       |93.65%      |           |                 |          |             |             |

额，好奇怪，规则纠正为什么差距不大了呢。。可能是以前的数据看差掉了
#### gold-couple dev
使用couple模型输出的dev作为gold，分别测试以下模型的accuracy。数据仅供参考

|__baseline__|__lexicon__|__guide+lexicon__|__couple__|__couple+pd__|__viterbiMerge__|
|------------|-----------|-----------------|----------|-------------|-------------|
|96.26%      |98.44%     |97.47%           |100%      |99.10%/98.87%|99.26%/99.25%|
#### gold-couple test(未纠正)
使用couple模型输出的test作为gold，分别测试以下模型的accuracy。数据仅供参考

|__baseline__|__lexicon__|__guide+lexicon__|__couple__|__couple+pd__|__viterbiMerge__|
|------------|-----------|-----------------|----------|-------------|-------------|
|96.38%      |98.38%     |97.47%           |100%      |99.10%       |99.32%       |

#### gold-dev.viterbiMerge.conll 测试dev
|__baseline__|__lexicon__|__guide+lexicon__|__couple__|__couple+pd__|__viterbiMerge__|
|------------|-----------|-----------------|----------|-------------|-------------|
|96.46%/96.44%|98.83%/98.77%|98.01%/98.06% |99.26%/99.25%|99.22%/99.02%|100%         |
#### gold-test.viterbiMerge.conll 测试test
|__baseline__|__lexicon__|__guide+lexicon__|__couple__|__couple+pd__|__viterbiMerge__|
|------------|-----------|-----------------|----------|-------------|-------------|
|96.56%      |98.78%     |97.99%           |99.32%    |99.14%       |100%         |

## 最终实验结果对比
|                       |__epoch__|__NLPCC dev accuracy__|
|-----------------------|---------|----------------------|
|close NLPCC train      |209      |94.67%                |
|open NLPCC + lexicon   |413      |95.74%                |
|open NLPCC + guide     |123      |95.05%                |
|open NLPCC + lexicon + guide|35  |95.97%                |
|open NLPCC + couple    |81       |96.01%                |
|open NLPCC + couple + pd|190        |96.10%               |

## 附加实验
### 实验、准确率、PRF值及其地址总结
|__Approch__                                     |__Address__                      |__Accuracy__|__P__|__R__|__F__|
|------------------------------------------------|---------------------------------|------------|-----|-----|-----|
|Baseline                                        |171 ~/ws-tagger/nlpcc2016\_baseline|94.66       |93.30|93.99|93.65|
|Lexicon Feature                                 |171 ~/ws-tagger/lexicon          |95.74       |94.45|95.31|94.88|
|-guide- WS from WSTagger(CTB7)                  |171 ~/ws-tagger/guide\_ws\_from\_wstagger\_ctb7            |94.52       |93.21|93.93|93.58|
|------ WS from WSTagger(CTB7+PD)                |171 ~/ws-tagger/guide\_ws\_from\_wstagger\_ctb7+pd(<font color=red>已修正</font>)         |94.80      |93.41|94.40|93.90|
|------ WS from WSPOSTagger(CTB7)                |171 ~/ws-tagger/guide\_ws\_from\_wspostagger\_ctb7         |94.86       |93.64|94.27|93.95|
|------ WS from WS&POSTagger(CTB7+PD)            |171 ~/ws-tagger/guide\_ws\_from\_wspostagger\_ctb7+pd      |95.05       |93.76|94.57|94.16|
|------ WS&POS from WSPOSTagger(CTB7)            |171 ~/ws-tagger/guide\_wspos\_from\_wspostagger\_ctb7/weibo\_dev|94.88       |94.33|93.64|93.98|
|------ WS&POS from WS&POSTagger(CTB7+PD)        |171 ~/ws-tagger/guide\_wspos\_from\_wspostagger\_ctb7+pd   |95.03       |93.83|94.50|94.16|
|Lexicon + Guide WS&POS from WSPOSTagger(CTB7+PD)|171 ~/ws-tagger/guide+lexicon                                                      |95.97       |94.77|95.33|95.15|
|Couple on WB&CTB7                               |172 ~/coupled-ws-tagger-from-jiayuan-2016-7-4/exp-coupled-weibo-and-ctb7-no-dict   |95.38       |94.12|94.91|94.51|
|-----  on WB&(CTB7+PD)                          |172 ~/coupled-ws-tagger-from-jiayuan-2016-7-4/exp-coupled-weibo-and-ctb7+pd-no-dict|95.50       |94.25|95.03|94.64|
|-----  on WB&CTB7 + lexicon                     |172 ~/coupled-ws-tagger-from-jiayuan-2016-7-4/exp-coupled-weibo-and-ctb7           |96.01       |94.74|95.61|95.17|
|-----  on WB&CTB7+PD lexicon(submitted)         |172 ~/coupled-ws-tagger-from-jiayuan-2016-7-4/exp-coupled-weibo-and-ctb7+pd        |95.98       |94.78|95.56|95.17|
|-----  on WB&CTB7+PD lexicon                    |172 ~/coupled-ws-tagger-from-jiayuan-2016-7-4/exp-coupled-weibo-and-ctb7+pd        |96.11       |94.80|95.82|95.30|
|Merge submit                                    |kiro ~/Work/NLPCC2016/viterbiMerge                      |96.14       |95.03|95.72|95.37|
|Merge ultimate                                  |kiro ~/Work/NLPCC2016/viterbiMerge                      |96.22       |95.10|95.84|95.47|
|Merge all<font color=red>已修正</font>          |kiro ~/Work/NLPCC2016/nlpcc2016\_dev\_eval              |95.88       |94.76|95.48|95.12|

其中，为了补全上面的表格，需要训练一些没有的模型。

|__model__          |__address__                                   |__Weibo train accuracy__|__Weibo dev accuracy__|
|-------------------|----------------------------------------------|------------------------|----------------------|
|WSTagger(CTB7)     |171 :~/ws-tagger/nlpcc\_CTB7\_train(model)    |92.76%                  |92.01%                |
|WSPOSTagger(CTB7)  |173 ~/wspos-tagger/nlpcc\_WSPOS\_CTB7(model)  |                        |                      |
|Couple on WB&CTB7  |172 ~/coupled-ws-tagger-from-jiayuan-2016-7-4/exp-coupled-weibo-and-ctb7-no-dict|             |95.30%        |
|-----  on WB&(CTB7+PD)|172 ~/coupled-ws-tagger-from-jiayuan-2016-7-4/exp-coupled-weibo-and-ctb7+pd-no-dict|       |95.50%        |

