title: SyntaxNet学习
date: 2016-08-20 16:47:39
tags: [syntaxnet]
---
# 概述
因为最近的工作需要使用到SyntaxNet，所以新建一篇博客，记录相关的学习过程。：）
[github地址](https://github.com/tensorflow/models/tree/master/syntaxnet)

[MaxLogLikelihood的公式推导](/documents/MaxLogLikelihood/main.pdf)
# 继续学习
<!--more-->
因为最近需要继续学习SyntaxNet，故而继续更新这篇博客。
找了半天的模型代码：171 qrxia@amax:~/TensorFlow/models/syntaxnet/

# 任务1：搞懂Google双隐含层是怎么实现的
如果有pre trained的embedding，就是用pre trained的embedding，否则就是用随机初始化: 1/sqrt(embedding\_size) *embedding\_size: [64, 32, 32]*
relu 的weight的初始化范围: -1e-4 ~ +1e-4, 正态分布
relu 的bias的初始化范围: -0.2 ~ +0.2, 正态分布
softmax (最后一层)的weight的初始化范围: 1e-4, 正态分布
softmax 的bias的初始化范围: 0!
```python
relu_init=1e-4, # 初始化weight，略有不同
bias_init=0.2, # 同上，bias，略有不同

# Create ReLU layers.
for i, hidden_layer_size in enumerate(self._hidden_layer_sizes):  # [200, 200] @kiro
	weights = self._AddParam(
		[last_layer_size, hidden_layer_size],
		tf.float32,
		'weights_%d' % i,
		self._ReluWeightInitializer(), return_average=return_average)
	bias = self._AddParam([hidden_layer_size],
		tf.float32,
		'bias_%d' % i,
		self._relu_bias_init, return_average=return_average)
	last_layer = tf.nn.relu_layer(last_layer, weights, bias, name='layer_%d' % i)
	last_layer_size = hidden_layer_size
```

# 任务2：执行流程
__不看train pos, train local的部分，直接看train global部分。__

工程执行入口： bazel-bin/syntaxnet/parser\_eval（这是一个python程序，只不过没有.py后缀）
1. 从Main()函数开始执行
	bazel-bin/syntaxnet/parser_eval.runfiles/  # 这个里面还有文件？
	bazel-bin/syntaxnet/parser_trainer.runfiles/__main__/syntaxnet # parser trainer位置
2. function Train() # Train函数入口
	parser = structured_graph_builder.StructuredGraphBuilder
	_beam_size = 10
	_max_steps = 25
	_AddLearningRate(...) # Returns a learning rate that decays by 0.96 every decay_steps.
		decayed_learning_rate = learning_rate * decay_rate ^ (global_step / decay_steps)
	learning_rate=0.1
	decay_steps=4000
3. bazel-bin/syntaxnet/parser\_trainer.runfiles/\_\_main\_\_/syntaxnet/ops/gen\_parser\_ops.py (machine generated)
	beam parse reader是c++写的，
	__beam parse reader__是由C++完成的代码，但是在文件gen_parser_ops里面是py 函数的形式存在着，如何通过beam parse reader获取features，state...目前还不得而知（暂时不看C++部分）！
	cross entropy
# 任务3：相关手册？
\_op\_def\_lib.apply\_op(...)  # python 调用C++程序？
\_op\_def\_lib =\_InitOpDefLibrary() # line 468  来自于tensorflow的核心 tensorflow.core.framework import op\_def\_pb2
```python
tf.constant(value, dtype=None, shape=None, name='Const')  # Creates a constant tensor.
tf.train.exponential_decay(...)  # Applies exponential decay to the learning rate. global step ? @kiro
tf.logical_and(x, y, name=None)  # Returns the truth value of x AND y element-wise.
tf.reduce_any(input_tensor, ...)  # Computes the "logical or" of elements across dimensions of a tensor.
tf.while_loop(cond, body, loop_vars, ...) # Repeat body while the condition cond is true.
tf.nn.softmax_cross_entropy_with_logits(logits, labels, ...)  # Computes softmax cross entropy between logits and labels.
class tf.train.MomentumOptimizer  # Optimizer that implements the Momentum algorithm.
tf.train.Optimizer.get_slot(var, name)  # Return a slot named name created for var by the Optimizer.
tf.reduce_sum(input_tensor, axis=None,)  # Computes the sum of elements across dimensions of a tensor. Equivalent to np.sum
tf.div(x, y, name=None)  # Returns x / y element-wise.
tf.nn.l2_loss(t, name=None)  # Computes half the L2 norm of a tensor without the sqrt: output = sum(t ** 2) / 2
tf.add_n(inputs, name=None)  # Adds all input tensors element-wise.
```
# 要点：cross entropy
1.tf.nn.softmax\_cross\_entropy\_with\_logits
	类似于先应用softmax, 再应用cross\_entropy


## 处理流程
摘抄了一些重要的信息。

break the text into words, run the POS tagger, run the parser, and then generate an ASCII version of the parse tree.
1. Training the SyntaxNet POS Tagger
   We process the sentences left-to-right. For any given word, we extract features of that word and a window around it, and use these as inputs to a feed-forward neural network classifier, which predicts a probability distribution over POS tags. Because we make decisions in left-to-right order, we also use prior decisions as features in subsequent ones.
   run the trained model over our training, tuning, and dev (evaluation) sets.
2. Local Pretraining
3. Global Training

# 模型的训练
有几点需要注意
> * contex文件中缺少char-map
> * 注释需要去掉，否则shell脚本不可执行
> * POS tags 需要使用到CONLL格式的第4列

使用的数据：
> * traing-corpus: /home/qrxia/data/ptb-data-wsj/wsj\_02\_21.train.conll07
> * tuning-corpus: /home/qrxia/data/ptb-data-wsj/wsj\_24.dev.conll07
> * dev-corpus: /home/qrxia/data/ptb-data-wsj/wsj\_22.dev.conll07cp3to4.conll

查看GPU的使用情况，每10s刷新一次显示：
```bash
>>watch -n 10 nvidia-smi
```
按照github上面的tutorial，使用SyntaxNet训练一个句法分析模型需要以下三步：
### 1.训练一个POStagger
按照tutorial的指引，非常方便就可以训练一个POStagger，其中，对以上三个进行evaluation：

|__training__|__tuning__|__dev__|
|------------|----------|-------|
|98.25%      |96.84     |96.74% |
### 2.训练一个local模型，用来pre-training
eval metric如下:

|__training__|__tuning__|__dev__|
|------------|----------|-------|
|95.32%      |90.01%    |91.54% |
### 3.训练一个global模型
eval metric如下：

|__training__|__tuning__|__dev__|
|------------|----------|-------|
|95.44%      |91.03%    |92.67% |
# 代码阅读：
初步看，SyntaxNet的主要代码集中在models/syntaxnet/syntaxnet。
*BUILD*: 应该是指定bazel的如何编译文件
ps: 在阅读代码的过程中，会记录一些tensorflow的语法：）
### parser\_trainer.py
主要交代了：命令行参数及其一些默认的configuration
```python
tf.app.flags #argparser, which implements a subset of the functionality in python-gflags
tf.app.run() #It's just a very quick wrapper that handles flag parsing and then dispatches to your own main
os.path.join('/home/aa','/home/aa/bb','/home/aa/bb/c') #返回组合路劲
>>> '/home/aa/bb/c'
```
main()：
1.compute lexicon (default: false) and load lexicon use "FeatureSize"
	projectivize\_training\_set (default: false)
2.Train

### lexicon\_builder.cc
包含的几个类： __LexiconBuilder FeatureSize__
需要提取的几个TermFrequencyMap: __words lcwords tags categories labels chars__
其他的几个需要提取的: __prefixes suffixes tag\_to\_category__

### embedding\_feature\_extractor.\*
Class: ParserEmbeddingFeatureExtractor
提取特征相关的文件

### feature\_extractor.\*
Generic feature extractor for extracting features from objects.

### term\_frequency\_map.\*
A mapping from strings to frequencies with save and load functionality.
Class: TermFrequencyMap, TagToCategoryMap
TagToCategoryMap: 从输出文件上来看，tag和category是一一对应的？

### parser\_transitions.\*
__Nothing__?

### sentence.proto
一个Sentence由docid, text, token组成，最大长度1000
token: word, start, end, head, tag, category, label

### proto\_io.h
Class: TextReader()

### document\_format.\*
Class: DocumentFormat --A document format component converts a key/value pair from a record to one or more documents
key/value pair? __Nothing__?

### graph\_builder.py
Builds parser models.
Class: GreedyParser

```bash
tf.name_scope()  #sharing variables
tf.concat(concat_dim, values, name='concat')  #Concatenates tensors along one dimension.
>>> a = [1,2,3,4,5]
>>> a = tf.reshape(a, [-1, 5])
>>> a
<tf.Tensor 'Reshape:0' shape=(1, 5) dtype=int32>
>>> sess = tf.Session()
>>> init = tf.initialize_all_variables()
>>> sess.run(init)
>>> sess.run(a)
array([[1, 2, 3, 4, 5]], dtype=int32)
>>> b = [3,4,5,6,7]
>>> b = tf.reshape(b, [-1, 5])
>>> b
<tf.Tensor 'Reshape_1:0' shape=(1, 5) dtype=int32>
>>> c = [a, b]
>>> sess.run(c)
[array([[1, 2, 3, 4, 5]], dtype=int32), array([[3, 4, 5, 6, 7]], dtype=int32)]
>>> d = tf.concat(1, c)
>>> d
<tf.Tensor 'concat_1:0' shape=(1, 10) dtype=int32>
>>> sess.run(d)
array([[1, 2, 3, 4, 5, 3, 4, 5, 6, 7]], dtype=int32)
enumerate(sequence, start=0) #
>>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
```

```python
dict.update(dict2)  # The method update() adds dictionary dict2's key-values pairs in to dict. Python
tf.identity # Return a tensor with the same shape and contents as the input tensor or value. is useful when you want to explicitly transport tensor between devices (like, from GPU to a CPU). The op adds send/recv nodes to the graph, which make a copy when the devices of the input and the output are different.
tf.random_normal_initializer(mean=0.0, stddev=1.0, seed=None, dtype=tf.float32)  # Returns an initializer that generates tensors with a normal distribution.
tf.ones(shape, dtype=tf.float32, name=None)  # Creates a tensor with all elements set to 1.
tf.get_variable(...)  # Gets an existing variable with these parameters or create a new one.
tf.cast(x, dtype, name=None)  # Casts a tensor to a new type.
class tf.train.ExponentialMovingAverage  # Maintains moving averages of variables by employing an exponential decay.
tf.convert_to_tensor(value, dtype=None, name=None, as_ref=False)  # Converts the given value to a Tensor.
tf.nn.embedding_lookup(params, ids, partition_strategy='mod', name=None, validate_indices=True)  # Looks up ids in a list of embedding tensors. 如果id查抄不到，会报错indices.
tf.unsorted_segment_sum(data, segment_ids, num_segments, name=None)  # Computes the sum along segments of a tensor.
tf.train.Optimizer.get_slot(var, name)  # Return a slot named name created for var by the Optimizer.
tf.group(*inputs, **kwargs)  # Create an op that groups multiple operations.
tf.check_numerics(tensor, message, name=None)  # Checks a tensor for NaN and Inf values.
tf.size(input, name=None)  # Returns the size of a tensor.
tf.greater(x, y, name=None)  # Returns the truth value of (x > y) element-wise.
tf.cond(pred, fn1, fn2, name=None)  # Return either fn1() or fn2() based on the boolean predicate pred.
```
feature\_endpoints是一连串这样子的数组。其中，local, feature\_endpoints shape=(?,) dtype=int32
```
['\x08\x8a\x06' '\x08\x8f\x01' '\x08\xf7\r' '\x08\xe0\x11'
   '\x08\xe1\xb3\x02' '\x08\xe0\xb3\x02' '\x08\xe0\xb3\x02'
   '\x08\xe0\xb3\x02' '\x08\x02' '\x08\xf8\x03' '\x08\xe0\xb3\x02'
   '\x08\xe0\xb3\x02' '\x08\xe0\xb3\x02' '\x08\xe0\xb3\x02'
   '\x08\xe0\xb3\x02' '\x08\xe0\xb3\x02' '\x08\xe0\xb3\x02'
   '\x08\xe0\xb3\x02' '\x08\xe0\xb3\x02' '\x08\xe0\xb3\x02']
```
[unsorted_segment_sum](https://www.tensorflow.org/versions/r0.10/api_docs/python/math_ops.html#unsorted_segment_sum)

Interesting: syntaxnet/bazel-syntaxnet/bazel-out/local-opt/genfiles/syntaxnet/ops/gen\_parser\_ops.py

### reader\_ops.cc
Class: GoldParseReader
```python
OP_REQUIRES_OK  #如果想要测试一个函数返回的 Status 对象是否是一个错误, 可以使用 OP_REQUIRES_OK. 这些宏如果检测到错误, 会直接跳出函数, 终止函数执行.
```

### sentence\_batch.\*
Helper class to manage generating batches of preprocessed ParserState objects by reading in multiple sentences in parallel.

### parser\_state.\*
Parser state for the transition-based dependency parser.

### affix.\*
Class: Affix, AffixTable
affix: 词缀

### text\_formats.cc
CONLL格式文件的定义

### structured\_graph\_builder.py
Build structured parser models.

```python
tf.NoGradient(op_type)  # Specifies that ops of type op_type do not have a defined gradient.
tf.while_loop(cond, body, loop_vars, parallel_iterations=10, back_prop=True, swap_memory=False, name=None) # Repeat body while the condition cond is true.
```
### parser\_state.\*
Parser state for the transition-based dependency parser.

### parser\_transitions.\*
Transition system for the transition-based dependency parser.


# 问题：
### Q1: 为什么train  pos的时候，num\_actions=45,而不是12？
因为在FeatureSize的代码中，有很明显的一行
```
num_actions->scalar<int32>()() = transition_system->NumActions(label_map_->Size())
```
### unpack\_sparse\_features.cc
Operator to unpack ids and weights stored in SparseFeatures proto.

### Q2: 重大发现
以前不知道的一些h文件，通过egrep发现，在 bazel-genfiles/syntaxnet/ 文件夹下面
