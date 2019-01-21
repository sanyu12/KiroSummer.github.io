title: eigen学习
date: 2017-02-17 12:32:12
tags: [eigen]
---
# eigen学习
最近需要学习一下eigen,开此博客记录一些笔记有些重要的东西就直接从eigen官网copy过来了~
<!--more-->
### The matrix class
This represents a matrix of arbitrary size (hence the X in MatrixXd), in which every entry is a double (hence the d in MatrixXd).
Matrix &lt; typename Scalar, int RowsAtCompileTime, int ColsAtCompileTime &gt;
typedef Matrix &lt; float, 3, 1 &gt; Vector3f;
typedef Matrix &lt; double, Dynamic, Dynamic &gt; MatrixXd;
All Eigen matrices default to column-major storage order.
rows(), cols() and size().
use fixed sizes for very small sizes where you can, and use dynamic sizes for larger sizes or where you have to.
### Matrix and vector arithmetric
Therefore, the instruction a = a.transpose() does not replace a with its transpose(except multiplication)
the dot() and cross() methods.
伴随矩阵?忘了..
### The Array class and coefficient-wise operations
The Array class provides general-purpose arrays.
Furthermore, the Array class provides an easy way to perform coefficient-wise operations.
Array &lt; typename Scalar, int RowsAtCompileTime, int ColsAtCompileTime &gt;
For element-wise product?
#### Converting between array and matrix expressions
Matrix expressions have an .array() method that 'converts' them into array expressions.
Array expressions have a .matrix() method
Array: <font color='red'>coefficient wise</font>
### Block operations
Individual columns and rows are special cases of blocks. Eigen provides methods to easily address them: .col() and .row().
### Advanced initialization
The finished() method is necessary here to get the actual matrix object once the comma initialization of our temporary submatrix is done.
### Reductions, visitors and broadcasting
Norm computations?
Partial reductions are applied with colwise() or rowwise() .
The concept behind broadcasting is similar to partial reduction.
### Interfacing with raw buffers: the Map class
You can use a Map object just like any other Eigen type:
### Reshape and Slicing
### Aliasing
Aliasing occurs more naturally when trying to shrink a matrix
a = a.transpose(); // !!! do NOT do this !!!
mat.bottomRightCorner(2,2) = mat.topLeftCorner(2,2).eval();
Eigen provides the special-purpose function transposeInPlace() which replaces a matrix by its transpose.
If an xxxInPlace() function is available, then it is best to use it, because it indicates more clearly what you are doing.
Thus, if matA is a squared matrix, then the statement matA = matA * matA;
Aliasing occurs when the same matrix or array coefficients appear both on the left- and the right-hand side of an assignment operator.
### Storage orders
If the storage order is not specified, then Eigen defaults to storing the entry in column-major.
## Dense linear problems and decompositions
### Linear algebra and decompositions
可以求解矩阵运算
(中间跳过了几个章节)
### Sparse matrix manipulations

