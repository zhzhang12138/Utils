import random

import collections as coll
import time


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
    data = {"A": 5, "B": 2, "C": 2, "D": 1}

    test("list_method({})")

    print("*" * 50)

    test("iter_method({})")
