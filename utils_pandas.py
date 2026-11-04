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
    """
    try:
        df = pd.read_csv(path,encoding="utf-8-sig")
    except pd.errors.EmptyDataError:
        return 0.0
    values = pd.to_numeric(df[column], errors="coerce")
    ave = float(values.mean())
    if pd.isna(ave):
        return 0.0
    return ave

def top_n_pandas(path, column, n):
    """
    读 CSV，返回 column 列最大的前 n 条。
    返回格式必须和 utils.top_n 一模一样：[("技能名", 320.0), ...]，圆括号，数字是 float。
    """
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except pd.errors.EmptyDataError:
        return []
    df[column] = pd.to_numeric(df[column], errors="coerce")#把column那一列转为数字，并放回df，为下面排序准备
    df = df.dropna(subset=[column])
    name_col = df.columns[0]#获得名字的那一列
    top = df.sort_values(by=column,ascending=False)#排序
    top = top.head(n)
    rows = top[[name_col, column]].values.tolist()
    result = []
    for row in rows:
        result.append((row[0],float(row[1])))

    return result
