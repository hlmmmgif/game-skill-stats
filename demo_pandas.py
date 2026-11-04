# -*- coding: utf-8 -*-
"""pandas 入门 demo：6 步，每步都 print 出来看。

跑法（在项目根目录，先激活 .venv）：
    python demo_pandas.py

这个文件不用改，先跑通、看懂每一步的输出。看懂之后再自己写函数。
"""
import pandas as pd


def line(title):
    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)


# ---------------------------------------------------------------- 第 1 步
# 你的手写版是怎么读 CSV 的？csv.DictReader 给你一个"字典列表"：
#     [{"技能名": "烈焰斩", "伤害": "120"}, {"技能名": "冰霜新星", "伤害": "85"}, ...]
# pandas 读出来的是另一种东西，叫 DataFrame，你可以先把它理解成
#     "一整张表格 + 每个单元格已经分好类型了"
line("第 1 步：read_csv 读出来的是什么")
df = pd.read_csv("skills.csv", encoding="utf-8-sig")
print(df)          # 直接 print 出来的样子和 Excel 一模一样
print("\n类型：", type(df))

# 它的大小（行数, 列数）
print("大小 df.shape：", df.shape)      # 元组 (行, 列)


# ---------------------------------------------------------------- 第 2 步
# 一张表由"列"组成。取一列，方式和中括号取字典的值一模一样，但拿到的是
# 一个 Series —— 你可以理解成"一列竖着放的数字"，是一个整体
line("第 2 步：取一整列出来看")
col = df["伤害"]
print(col)
print("\n类型：", type(col))

# 手写版你得写 for 循环累加，因为列表只能一个一个过。
# Series 能一次性算完，因为它自己知道自己有几个数：
print("\n这一列有几个数？", len(col))

# 关键区别：对整列做运算，它会自动"每个数都算一遍"
print("\n整列乘以 2（看是不是每个数都变了）：")
print(col * 2)


# ---------------------------------------------------------------- 第 3 步
# 你要的"平均值"，pandas 自带，一行。
# 对比手写版的 csv_average：total 累加 + count 计数 + 除法，15 行。
line("第 3 步：算一个平均值")
avg = df["伤害"].mean()
print("df['伤害'].mean() =", avg)
print("和手写版对照，应该是 138.75")

# 别的也可以一行：max / min / sum / 有多少个非空值
print("最大值 .max() =", df["伤害"].max())
print("最小值 .min() =", df["伤害"].min())
print("求和   .sum() =", df["伤害"].sum())


# ---------------------------------------------------------------- 第 4 步
# 排序 + 只取前几名。手写版是 result.sort(key=lambda...) 然后 result[:n]。
# pandas 用 sort_values：按哪一列排、从大到小还是从小到大
line("第 4 步：按伤害从大到小排")
asc = df.sort_values(by="伤害", ascending=False)
print(asc)

# 只要前 3 名，用 head（头几个）。和列表切片 [:3] 是一个意思。
print("\n只要前 3 名 .head(3)：")
print(asc.head(3))


# ---------------------------------------------------------------- 第 5 步
# 排完之后，怎么变成你手写版那种 [("陨石术", 320.0), ...] 的格式？
# 先只挑两列出来（中括号里放一个列表，就是"挑这几列"）
line("第 5 步：只挑两列，再转成列表")
two = asc.head(3)[["技能名", "伤害"]]
print(two)

# 转成 Python 的列表（.values 去掉表格外壳，.tolist() 变成普通 list）
print("\n转成列表：")
print(two.values.tolist())

# 注意看输出的括号：是 [[...], [...]] 还是 [(...), (...), ]？
# 你手写版 top_n 返回的是圆括号的"元组"。这里出来的是方括号的"列表"。
# 两者内容一样，但 == 比较不相等。这是 Stage 2 要你解决的事，先记住这个现象。


# ---------------------------------------------------------------- 第 6 步
# 最后一件事：列名不要写死。
# 你手写版用的是 reader.fieldnames[0]，pandas 里是 df.columns
line("第 6 步：拿列名，不写死")
print("所有列名 df.columns：", list(df.columns))
print("第一列的名字 df.columns[0]：", df.columns[0])

# 换个文件验证一下：boss表.csv 的第一列叫"首领名"，不叫"技能名"
df2 = pd.read_csv("boss表.csv", encoding="utf-8-sig")
print("\nboss表.csv 的列名：", list(df2.columns))
print("第一列：", df2.columns[0])
print("它的伤害平均值：", df2["伤害"].mean(), "（应该等于 175.0）")


line("跑完了")
print("如果上面每一步的输出你都看得懂，今天的技术部分就够用了。")
