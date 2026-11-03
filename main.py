# -*- coding: utf-8 -*-
"""技能数据小工具：命令行入口。

用法：
    python main.py --check                                跑一遍自测
    python main.py --file skills.csv                      统计"伤害"平均值
    python main.py --file skills.csv --column 冷却秒       统计其他列
    python main.py --file skills.csv --digits 0           控制小数位
"""
import argparse

from utils import (
    csv_average,
    top_n,
    q1_average,
    q2_word_freq,
    q3_stats,
    q4_robot_run,
    q5_read_default,
)


def run_checks():
    """跑一遍全部自测，返回失败的条数（0 表示全通过）。"""
    checks = [
        ("Q1 平均值", q1_average([{"name": "甲", "score": "88"}, {"name": "乙", "score": "92"}]), 90.0),
        ("Q1 空列表", q1_average([]), 0.0),
        ("Q2 词频", q2_word_freq("a B a"), {"a": 2, "b": 1}),
        ("Q2 大小写", q2_word_freq("Hello hello HELLO"), {"hello": 3}),
        ("Q3 stats", q3_stats([1, 2, 3]), (1, 3, 2.0)),
        ("Q3 digits", q3_stats([1, 2, 4], 0), (1, 4, 2.0)),
        ("Q4 类", q4_robot_run("A", 2), "A 跑了 6 米"),
        ("Q5 兜底", q5_read_default("不存在_xyz.txt", default="默认值"), "默认值"),
        ("CSV 平均", round(csv_average("skills.csv", "伤害"), 2), 138.75),
        ("TOP3", top_n("skills.csv", "伤害", 3)[0], ("陨石术", 320.0)),
        ("TOP 脏数据", top_n("dirty.csv", "伤害", 2), [("甲", 120.0), ("丙", 80.0)]),
        ("空文件", top_n("空.csv","伤害",2),[]),
        ("越界",len(top_n("skills.csv","伤害",999)),8),
        ("空文件 0 字节", top_n("真空.csv", "伤害", 2), []),
    ]

    failed = 0
    for name, got, exp in checks:
        ok = got == exp
        failed += 0 if ok else 1
        print(f"{'OK  ' if ok else 'FAIL'} {name}: 得到 {got!r}")

    print(f"\n{len(checks) - failed}/{len(checks)} 通过")
    return failed


def build_parser():
    """命令行参数定义。集中在这里，方便以后加参数。"""
    p = argparse.ArgumentParser(description="技能数据小工具：统计 CSV 某列的平均值")
    p.add_argument("--file", help="CSV 文件路径，例如 skills.csv")
    p.add_argument("--column", default="伤害", help="要统计的列名（默认：伤害）")
    p.add_argument("--digits", type=int, default=1, help="保留小数位（默认：1）")
    p.add_argument("--top", type=int, default=0, help="输出前 N 名（默认 0 = 只看平均值）")
    p.add_argument("--check", action="store_true", help="跑一遍自测")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    # 模式一：自测
    if args.check:
        failed = run_checks()
        raise SystemExit(1 if failed else 0)   # 退出码让外部程序也能判断成败

    # 模式二：统计某个 CSV
    if args.file:
        try:
            if args.top > 0:                                  # 排行榜模式
                ranking = top_n(args.file, args.column, args.top)

                # ── B2 的第二半 ────────────────────────────────
                # 空 CSV、或者整列都是脏数据被跳过后，ranking 会是空列表 []。
                # 现在的表现是打印一个空标题就结束，用户以为程序坏了。
                #
                #   空① ：if 后面填判断条件 —— "ranking 是空列表"怎么用布尔值表达？
                #          （想清楚：你要的是"空的时候进这个分支"，不是"不空的时候"）
                #   空② ：print 一句人话（可以参考 main.py 下面几个 except 里的提示写法）
                #   空③ ：raise SystemExit(2)  —— 这一行不用改，直接抄下面 except 里的写法
                if not ranking:
                    print("错误，ranking为空列表，csv可能为空，或者整列都是脏数据")
                    raise SystemExit(2)

                print(f"{args.column} TOP {args.top}:")
                for i, (name, value) in enumerate(ranking, start=1):
                    # ── B3 ────────────────────────────────────
                    # 现在这行是：print(f"{i}. {name}\t{value}")
                    # 问题：value 是 float，会打出 320.0，不管 --digits 传几都没用。
                    #
                    #   空④ ：要求打印出来是 "1. 陨石术    320"（--digits 0）
                    #          也就是 1. 序号  2. 名字  3. \t 制表符  4. 数字（几位小数可调）
                    #
                    # 提示：形状是  f"{value:.___f}"
                    #       小数点后的 ___ 位置，要再套一对大括号把 args.digits 塞进去，
                    #       写成 .{args.digits}f 的意思就是"按 args.digits 位小数显示"
                    # 注意：round() 做不到这件事，round(320.0, 0) 还是 320.0，去不掉 .0
                    print(f"{i}. {name}\t{value:.{args.digits}f}")
            else:                                             # 平均值模式（原有）
                avg = csv_average(args.file, args.column)
                print(f"{args.column} 平均值: {round(avg, args.digits)}")
        except FileNotFoundError:
            print(f"错误：找不到文件 {args.file}")
            raise SystemExit(2)
        except KeyError:
            print(f"错误：CSV 里没有名为 {args.column!r} 的列，请检查表头")
            raise SystemExit(2)
        except ValueError as e:
            print(f"错误：这一列有非数字内容（{e}）")
            raise SystemExit(2)

        return

    # 模式三：什么都没给，打印帮助
    parser.print_help()


if __name__ == "__main__":
    main()


