title: span-parser
date: 2016-11-15 20:37:01
tags: [work]
---
# span parser
## span parser 源码剖析
最近在学习基于转移的句法分析，学习span parser，着重学习pycnn的使用。
<!--more-->
LSTM类：
	初始化一个LSTM类，仅仅初始化参数，并没有具体实现相关的具体算法。
State类：
	包含一个LSTM单元，并且实现了网络的计算过程。

struct data: ?
label data: ?

PharseTree类：
	_parse函数，解析一句话Tree
	将line -> tree
Parser.py
	gold_actions(tree): 得到tree的gold actions
### parser的一些参数设置
word dim: 50 tag dim: 20
lstm units: 200
hidden units: 200
batch: 10
dropout: 0.5
unknow param: 0.8375?
alpha: 1.0

### pycnn的使用细节

> * model.add\_parameters(...)
> * parameters.load\_array(np.random.uniform(-0.01, 0.01, self.W\_i.shape()))
> * pycnn.logistic(self.W\_i * x + self.b\_i)
> * g = pycnn.tanh(self.W\_c * x + self.b\_c)
> * c = pycnn.cwise\_multiply(f, self.c) + pycnn.cwise\_multiply(i, g)
> * pycnn.AdadeltaTrainer(self.model, lam=0, eps=1e-7, rho=0.99)
> * model.add\_lookup\_parameters('word-embed', (word\_count, word\_dims))
> * model['word-embed'].init\_from\_array(np.random.uniform(-0.01, 0.01, self.model['word-embed'].shape()),)
> * activation = pycnn.rectify
> * W1\_struct = pycnn.parameter(self.model['struct-hidden-W'])

> * wordvec = pycnn.lookup(self.model['word-embed'], w)
> * vec = pycnn.dropout(vec, self.droprate)
