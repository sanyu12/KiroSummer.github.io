title: NumPy
date: 2016-1-12 21:29:34
tags: [python, Numpy, theano]
---
# numpy中的一些方法汇总
## numpy.asarray
numpy.asarray(a, dtype=None, order=None)将输入转换成一个数组
* 参数：
   + a：类似于数组的输入数据，list，tuple...
   + dtype：数据类型，可选参数，默认情况下，数据类型继承于输入数据　　
   + order：{'C','F'}，可选参数，确定使用以行为主(C)或者以列为主(F)的内存表示方式，默认以行为主
* 输出：ndarray
<!-- more -->
例子：
```
    >>> a = [1, 2]
    >>> np.asarray(a)
    array([1, 2])
```
## theano.tensor
theano.tensor.matrix(name=None, dtype=config.floatX)
* 参数：
   + name：matrix的名字
   + dtype：数据类型
* 返回：返回一个二维的ndarray
theano.tensor.ivector(?)
* 参数：
   + 同上
* 返回：返回一个一维的int32类型的向量
theano.tensor.nnet.conv.conv2d(input, filters, image_shape=None, filter_shape=None, border_mode='valid', subsample=(1, 1), **kargs)
此功能将建立卷积堆叠输入图像与一组过滤器的符号图
* 参数：
   + input：有符号的四维张量
   + filters：
   + image_shape=None：输入参数的形状
   + filrer_shape=None：用于循环展开优化
   + border_mode='valid'：{'valid', 'full'}，'valid'应用过滤器完成图像的补丁
   + subsample=(1, 1)：通过该因子子采样的输出
* 返回：设置由卷积层产生的特征图，有符号的4D张量
theano.tensor.signal.downsample.max_pool_2d(input, ds, ignore_border=None, st=None, padding=(0, 0), mode='max')
将一个N维的张量作为输入
参数：
+ input：输入的图像
+ ds：用来减缩规模的系数
+ ignore_border=None：如果为真，(5, 5)作为输入，当ds=(2, 2)的时候会产生(2, 2)的输出，如果为假，产生(3, 3)的输出
## theano.tensor.grad
theano.tensor.grad(cost, \[w, b\])
计算cost的梯度
例子：
gw, gb = T.grad(cost, \[w, b\])
## theano.tensor.log
theano.tensor.log(a),log2(a),log10(a)
返回一个变量，代表以e，2，10，为底的log函数的值
## theano.tensor.mean
theano.tensor.mean(x, axis=None, dtype=None, keepdims=False, acc_dtype=None)
* 参数：
   + x：有符号的张量
* 返回：x的平均值
## theano.tensor.eq
theano.tensor.eq(a, b)
返回一个能够表示逻辑不等式(a == b)的值，参数类型是有符号的张量(symbolic tensor)
## theano.tensor.scalar
theano.tensor.scalar(name=None, dtype=config.floatX)
返回一个0维的ndarray
lscalar int64
## theano.tensor.nnet.softmax
theano.tensor.nnet.softmax.sigmoid(x)
返回x应用S型非线性的值
公式：
![sigmoid](http://deeplearning.net/software/theano/_images/math/a039611dafb1a945c480b6453a828af1d0a17054.png)
![sigmoid][logo]
[logo]: http://deeplearning.net/software/theano/_images/sigmoid_prec.png
## theano.function
theano.function(inputs, outputs, mode=None, updates=None, givens=None, no_default_updates=False, accept_inplace=False, name=None, rebuild_strict=True, allow_input_downcast=None, profile=None, on_unused_input='raise')
* 参数：
   + input：
   + output：计算表达式
   + updates：新的SharedVariable变量的表达式
   + givens：在计算图形中的特殊取代，类型：list, tuple or dict
* 返回：函数实例
编译图表为可用的对象
```
    >>> import theano
    >>> x = theano.tensor.dscalar()
    >>> f = theano.function([x], 2*x)
    >>> f(4)
    array(8.0)
```
## matrix.getvalue(borrow=True).shape[0]
其中，matrix是由theano.shared方法产生的，返回matrix的维度
## numpy.zeros
numpy.zeros(shape, dtype=float, order='C')
返回一个新的数组array，给定了形状和数据类型，初始化为全0
## numpy.reshape
numpy.reshape(a, newshape, order='C')
* 参数：
   + a：被重新定义形状的数组
   + newshape：新的形状，可以为int, tuple, ints，新的形状要适合原来的形状
   + order：{'C', 'F', 'A'}可选参数
* 返回：返回重新定义形状的二维数组，ndarray
## numpy.mean
numpy.mean(a, axis=None, dtype=None, out=None, keepdims=False)
计算算数表达式的平均值
* 参数：
   + a：包含需要计算平均值的数的数组array
* 返回：平均值
## numpy.arange
numpy.arange(\[start, \]stop, \[step, \]dtype=None)
在给定的时间间隔内，返回均匀间隔值，类型ndarray	
## numpy.random.binomial
numpy.random.binomial(n, p, size=None)
给二项分布提取样货
```
    >>> n, p = 10, .5  # number of trials, probability of each trial
    >>> s = np.random.binomial(n, p, 1000)
    # result of flipping a coin 10 times, tested 1000 times.
```
## numpy.prod:
numpy.prod(a, axis=None, dtype=None, out=None, keepdims=False)
* 参数：
   + a：输入数据，array_like
* 返回：数据a的连乘结果
## numpy.random.normal
numpy.random.normal(loc=0.0, scale=1.0, size=None)
绘制来自高斯(正常)分布的随机样品
* 参数：
   + loc：高斯分布的平均值，float类型
   + scale：高斯分布的标准差
   + size：输出的形状
## numpy.argmax
numpy.argmax(a, axis=None, out=None)
返回沿轴最大值的索引
例子：
```
    a = np.arange(6).reshape(2, 3)
    np.argmax(a)
    5
```
## numpy.random.rand
numpy.random.rand(d0, d1, d2, ..., dn)
创建一个给定形状的数组，然后用一个均匀分布的样本来填充
例子：
```
	>>> d = np.random.rand(2, 3)
	>>> d
	array([[ 0.63816172,  0.76960869,  0.6695834 ],
	       [ 0.54631594,  0.63578294,  0.83058455]])
```
还有如下的使用方法，可以用于神经网络中的dropout方法：
```
	>>> h
	array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
	>>> x = (np.random.rand(*h.shape) < 0.5)
	>>> x
	array([ True, False, False,  True,  True,  True, False,  True, False, False], dtype=bool)
	>>> x * h
	array([0, 0, 0, 3, 4, 5, 0, 7, 0, 0]))
```

更多有关机器学习的知识：[http://deeplearning.net/](http://deeplearning.net/)













































