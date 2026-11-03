import csv


# ---------------------------------------------------------------- Q1
def q1_average(rows):
    """
    第 1 题：CSV 风格的字典列表，算 score 列平均值。
    rows = [{"name":"甲","score":"88"}, ...]   注意 score 是字符串
    返回 float；空列表返回 0.0
    """
    count, total = 0, 0
    if len(rows) == 0:
        return 0.0
    else:
        for r in rows:
            total += float(r["score"])
            count = count + 1
        ave = total / count
        return ave


# ---------------------------------------------------------------- Q2
def q2_word_freq(text):
    """
    第 2 题：词频统计。按空格切分，返回 {词: 次数}，忽略大小写。
    q2_word_freq("a B a") -> {"a": 2, "b": 1}
    """
    count = {}
    words = text.split()
    for word in words:
        word = word.lower()
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    return count


# ---------------------------------------------------------------- Q3
def q3_stats(numbers, digits=2):
    """
    第 3 题：返回 (最小值, 最大值, 平均值)，平均值保留 digits 位小数。
    要求：digits 是默认参数。
    q3_stats([1, 2, 3]) -> (1, 3, 2.0)
    """
    ma = max(numbers)
    mi = min(numbers)
    ave = sum(numbers) / len(numbers)
    return mi, ma, round(ave, digits)


# ---------------------------------------------------------------- Q4
class Robot:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    def run(self, seconds):
        return f"{self.name} 跑了 {self.speed * seconds} 米"


def q4_robot_run(name, speed):
    """
    第 4 题：写一个类 Robot，__init__ 存 name/speed，run(seconds) 返回
    "<name> 跑了 <speed*seconds> 米"。然后这里 return Robot(...).run(...)
    q4_robot_run("A", 2) 传入 seconds=3 -> "A 跑了 6 米"
    """
    r = Robot(name, speed).run(3)
    return r


# ---------------------------------------------------------------- Q5
def q5_read_default(path, default="文件不存在"):
    """
    第 5 题：读文件内容并返回；文件不存在时返回 default（不许让程序崩）。
    """
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            content = f.read()
            return content
    except FileNotFoundError:
        return default

def csv_average(path, column):
    """
    读 CSV 文件，返回 column 这一列数值的平均值。
    path   : CSV 文件路径
    column : 列名，比如 "伤害"
    返回 float；没有有效数据时返回 0.0
    """
    total = 0.0
    count = 0

    # 打开文件这一段照抄，三个细节都别改：
    with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)      # 每行变成一个字典，键就是表头
        for row in reader:
            value = row[column].strip()   # 关键：接住 strip 的返回值
            if value == "":               # 纯空格也能识别成空值
                continue
            total += float(value)
            count += 1

    if count == 0:                      # 防止除以 0
        return 0.0
    return total / count

def top_n(path, column, n):
    """读 CSV，返回 column 列最大的前 n 条，格式 [(名称, 数值), ...]"""
    with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        
        # ── B2 ────────────────────────────────────────────────
        # 空文件时 reader.fieldnames 的值是 None，
        # 下面那句 [0] 就会炸：'NoneType' object is not subscriptable
        # 请在取 [0] 之前，先判断"有没有表头"，没有就直接返回空列表。
        # 正常返回的是列表，所以空的时候也要返回列表。
        if not reader.fieldnames:
            return []
        name_col = reader.fieldnames[0]
        # ── B1 ────────────────────────────────────────────────
        # 目标：一行一行过，只把"数值有效"的行收进 result。
        # 抄 csv_average 第 98-101 行的思路，三步：
        #   1) 取这一行 column 列的值，去掉前后空格（⚠ 必须接住返回值）
        #   2) 如果去完空格是空字符串，跳过这一行（用一个关键字）
        #   3) 合格的行，存成 (名称, 数字) 这样的小括号对，追加进 result
        #      注意：第 2 个元素要用 float() 转成数字，否则排序会按字符串比
        result = []
        for row in reader:
            value = row[column].strip()
            if value == "":
                continue
            
            result.append((row[name_col], float(value)))

    # ── 排序 ──────────────────────────────────────────────────
    # result 里装的是 ('甲', 120.0) 这样的元组。
    # 要按"第 2 个元素"从大到小排。
    # 提示：用 result.sort(...)，不要用 sorted(...)
    #      （sorted 返回新列表，sort 是原地改 result 自己）
    #      key 用 lambda pair: ____
    result.sort(key=lambda pair: pair[1], reverse=True)

    # ── 切片 ──────────────────────────────────────────────────
    # 返回前 n 个。一行搞定，用切片。
    return result[:n]
