# -*- coding: utf-8 -*-
"""技能数据小工具：命令行入口。

用法：
    python main.py --check                                跑一遍自测
    python main.py --file skills.csv                      统计"伤害"平均值
    python main.py --file skills.csv --column 冷却秒       统计其他列
    python main.py --file skills.csv --digits 0           控制小数位
"""
import argparse
import logging

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
        logging.info(f"{'OK  ' if ok else 'FAIL'} {name}: 得到 {got!r}")

    logging.info(f"{len(checks) - failed}/{len(checks)} 通过")
    return failed


def build_parser():
    """命令行参数定义。集中在这里，方便以后加参数。"""
    p = argparse.ArgumentParser(description="技能数据小工具：统计 CSV 某列的平均值")
    p.add_argument("--file", help="CSV 文件路径，例如 skills.csv")
    p.add_argument("--column", default="伤害", help="要统计的列名（默认：伤害）")
    p.add_argument("--digits", type=int, default=1, help="保留小数位（默认：1）")
    p.add_argument("--top", type=int, default=0, help="输出前 N 名（默认 0 = 只看平均值）")
    p.add_argument("--check", action="store_true", help="跑一遍自测")
    p.add_argument("--verbose", action="store_true", help="输出详细日志")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

  

    # 模式一：自测
    if args.check:
        failed = run_checks()
        raise SystemExit(1 if failed else 0)   # 退出码让外部程序也能判断成败

    # 模式二：统计某个 CSV
    if args.file:
        try:
            if args.top > 0: 
                logging.debug(f"进入排行榜模式：file={args.file} column={args.column} top={args.top}")#排行榜模式
                ranking = top_n(args.file, args.column, args.top)

                if not ranking:
                    logging.error(f"没有可用数据：{args.file} 的{args.column}列里没有有效数值")
                    raise SystemExit(2)

                logging.info(f"{args.column} TOP {args.top}:")
                for i, (name, value) in enumerate(ranking, start=1):
                    logging.info(f"{i}. {name}\t{value:.{args.digits}f}")
            else:
                logging.debug(f"进入平均值模式：file={args.file} column={args.column} digits={args.digits}")
                avg = csv_average(args.file, args.column)
                logging.info(f"{args.column} 平均值: {round(avg, args.digits)}")
        except FileNotFoundError:
            logging.error(f"错误：找不到文件 {args.file}")
            raise SystemExit(2)
        except KeyError:
            logging.error(f"错误：CSV 里没有名为 {args.column!r} 的列，请检查表头")
            raise SystemExit(2)
        except ValueError as e:
            logging.error(f"错误：这一列有非数字内容（{e}）")
            raise SystemExit(2)

        return

    # 模式三：什么都没给，打印帮助
    parser.print_help()


if __name__ == "__main__":
    main()

