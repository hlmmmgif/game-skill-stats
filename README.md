# 技能数据小工具
本工具通过命令行实现：读CSV，算指定列的平均值，输出前N名排行榜

## 问题
在游戏技能的伤害衡量中往往需要计算平均伤害，进行排名，而人工手算或Excel容易错误，计算时如果遇到脏数据更会直接崩溃


## 方案
- 拆分模块，把可能用到的函数拆分成各个模块，要用时再引入
- 参数化：用 argparse 替代手写 sys.argv，支持命名参数与默认值，-h 自动生成帮助
- 所有可预期的输入错误统一返回退出码 2，让调用方（CI、脚本）能判断失败，而不是看屏幕输出
- logging分级，通过debug，error和info分级过滤显示
- 配备对应时间戳，了解何时出现问题
- 新增pandas可选依赖，不装也能走，--check会提示未安装pandas，提供其他的选择空间


## 效果
- （pandas库安装）20条回归测试全部通过（包含脏数据,越界，空文件等意外情况,保证运行稳定）若没有安装pandas，最后20条中会有14条通过，剩下6条含pandas的会被跳过
- skills.csv 共 8 条技能记录
- 平均伤害 138.75
- TOP1 陨石术 320（冷却 12 秒）
- 脏数据 / 0 字节文件 / n 超过总数 三种边界均不崩溃

## 快速开始

:: 创建并激活虚拟环境
python -m venv .venv
.venv\Scripts\activate

:: 跑自检，20 条测试
python main.py --check

:: 统计"伤害"列平均值
python main.py --file skills.csv

:: 换个列
python main.py --file skills.csv --column 冷却秒

:: 输出前 3 名排行榜
python main.py --file skills.csv --top 3

:: 控制小数位
python main.py --file skills.csv --digits 0

::切换pandas库，计算伤害平均值，应为138.8
python main.py --file skills.csv --engine pandas

::如果提示ModuleNotFoundError: No module named 'pandas'，可以尝试下载pandas
pip install pandas


## 项目结构

```
main.py          命令行入口：解析参数 → 调用函数 → 输出结果
utils.py         工具库：统计与格式化函数，不主动执行
utils_pandas.py  工具库的pandas版本，适用于大型数据批处理
skills.csv       正常测试数据
dirty.csv        脏数据（含纯空格单元格）
boss表.csv       首列名不同的表，验证列名没有写死
空.csv           只有表头，没有数据行
真空.csv         0 字节文件
代码解析笔记.md   逐函数解析与踩坑记录
```
