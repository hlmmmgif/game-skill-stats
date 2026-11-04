# -*- coding: utf-8 -*-
"""pandas 版工具库。

和 utils.py 的关系：同一个问题、两套实现，函数的作用完全一样，只是换了工具。
今天只写 csv_average_pandas，写完能跑出 138.75 就算过。
"""
import pandas as pd


def csv_average_pandas(path, column):
    """
    读 CSV，返回 column 这一列数值的平均值。pandas 版。

    path   : CSV 文件路径，比如 "skills.csv"
    column : 列名，比如 "伤害"
    返回 float

    对照手写版 utils.csv_average：那边是 total 累加 + count 计数 + 除法，15 行。
    这边只要 2 行——一行读表，一行算平均。
    """
    # 第 1 步：读表。抄 demo 第 1 步的那行，encoding 别漏（Excel 存的 CSV 带 BOM）。
    #         读完之后 df 就是一张表。
    df = pd.read_csv(path,encoding="utf-8-sig")

    # 第 2 步：取出 column 这一列，算平均值，直接 return。
    #         提示：demo 第 3 步。取列是 df[列名]，算平均是一个方法，前面带点。
    return float(df[column].mean())


def top_n_pandas(path, column, n):
    """
    读 CSV，返回 column 列最大的前 n 条。
    返回格式必须和 utils.top_n 一模一样：[("技能名", 320.0), ...]，圆括号，数字是 float。
    """
    # 第 1 步：读表
    df = pd.read_csv(path, encoding="utf-8-sig")

    # 第 2 步：拿第一列的名字。不许写死"技能名"——boss表.csv 第一列叫"首领名"。
    #         提示：demo 第 6 步，df.columns 是个列表。
    name_col = df.columns[0]

    # 第 3 步：按 column 这一列从大到小排序，然后只取前 n 行。
    #         提示：demo 第 4 步。这里要连写两个方法，排序的后面接取前几个。
    #         sort_values 需要告诉它按哪一列排：by="列名"；从大到小是 ascending=False。
    top = df.sort_values(by=column,ascending=False)
    top = top.head(n)
    # 第 4 步：只挑这两列（名字列 + 数值列），转成普通列表。
    #         这一步我写好了，你看一眼它出来的是方括号还是圆括号。
    rows = top[[name_col, column]].values.tolist()

    # 第 5 步：把每个小列表变成圆括号的元组，装进新列表。
    #         提示：row 是 ['陨石术', 320] 这样的小列表，row[0] 是名字，row[1] 是数字。
    #         你手写版 utils.top_n 里就是这么 append 的，照那个思路来。
    result = []
    for row in rows:
        result.append((row[0],float(row[1])))

    return result
