加权随机算法一般应用在以下场景：有一个[集合](https://so.csdn.net/so/search?q=集合&spm=1001.2101.3001.7020)S，里面比如有A,B,C,D这四项。这时我们想随机从中抽取一项，但是抽取的概率不同，比如我们希望抽到A的概率是50%,抽到B和C的概率是20%,D的概率是10%。一般来说，我们可以给各项附一个权重，抽取的概率正比于这个权重。那么上述集合就成了：

> ```
> {"A": 5, "B": 2, "C": 2, "D": 1}
> ```

### 方法一

扩展这个集合，使每一项出现的次数与其权重正相关。在上述例子这个集合扩展成：

> ```
> {"A", "A", "A", "A", "A", "B", "B", "C", "C", "D"}
> ```

然后就可以用均匀随机算法来从中选取。

好处：选取的时间复杂度为O(1),算法简单。

坏处：空间占用极大。另外如果权重数字位数较大，例如{A:49.1 B：50.9}的时候，就会产生巨大的空间浪费。

```python
data = {"A": 5, "B": 2, "C": 2, "D": 1}


def list_method(dic_data: dict):
    """
    python 加权随机算法
    Params:
        dic_data：权重集合
    Returns:
        根据权重算法选取出的数据
    """
    all_data = []
    for v, w in dic_data.items():
        temp = []
        for i in range(w):
            temp.append(v)
            all_data.extend(temp)
    n = random.randint(0, len(all_data) - 1)
    return all_data[n]
    
if __name__ == "__main__":
    print(list_method(data))
```

### 方法二

计算权重总和sum，然后在1到sum之间随机选择一个数R，之后遍历整个集合，统计遍历的项的权重之和，如果大于等于R，就停止遍历，选择遇到的项。

还是以上面的集合为例，sum等于10，如果随机到1-5，则会在遍历第一个数字的时候就退出遍历。符合所选取的概率。

好处：没有额外的空间占用，算法也比较简单。

坏处：选取的时候要遍历集合，时间复杂度是O(n)。

```python
def iter_method(dic_data: dict):
    """
       python 加权随机算法
       Params:
           dic_data：权重集合
       Returns:
           根据权重算法选取出的数据
       """
    total = sum(dic_data.values())
    rad = random.randint(1, total)
    cur_total = 0
    res = ""

    for k, v in dic_data.items():
        cur_total += v
        if rad <= cur_total:
            res = k
            break
    return res
  
if __name__ == "__main__":
    print(iter_method(data))
```

### 对比

```python
import random

import collections as coll
import time

data = {"A": 5, "B": 2, "C": 2, "D": 1}


def list_method(dic_data: dict):
    """
    python 加权随机算法
    Params:
        dic_data：权重集合
    Returns:
        根据权重算法选取出的数据
    """
    all_data = []
    for v, w in dic_data.items():
        temp = []
        for i in range(w):
            temp.append(v)
            all_data.extend(temp)
    n = random.randint(0, len(all_data) - 1)
    return all_data[n]


def iter_method(dic_data: dict):
    """
       python 加权随机算法
       Params:
           dic_data：权重集合
       Returns:
           根据权重算法选取出的数据
       """
    total = sum(dic_data.values())
    rad = random.randint(1, total)
    cur_total, res = 0, ""

    for k, v in dic_data.items():
        cur_total += v
        if rad <= cur_total:
            res = k
            break
    return res


def func_time(func):
    def inner(*args, **kw):
        start_time = time.time()
        func(*args, **kw)
        end_time = time.time()
        print('函数运行时间为：', end_time - start_time, 's')

    return inner


@func_time
def test(method):
    dict_num = coll.defaultdict(int)
    for i in range(100):
        dict_num[eval(method.format(data))] += 1

    for i, j in dict_num.items():
        print(i, j)


if __name__ == "__main__":
    test("list_method({})")

    print("*" * 50)

    test("iter_method({})")

    
>>>:
list_method:
A 75
C 11
B 10
D 4
函数运行时间为： 0.0020258426666259766 s
**************************************************
iter_method:
A 51
C 24
D 13
B 12
函数运行时间为： 0.0017800331115722656 s
```
