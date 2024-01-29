import json
import numpy as np

# 读取JSON文件
with open('../data.json', 'r', encoding='utf-8') as file:
    json_data = file.read()

# 加载JSON数据
data = json.loads(json_data)

# 初始化空的numpy数组，用于存储每个维度的值
heights = []
lengths = []
widths = []

# 遍历数据并填充数组
for key, value in data.items():
    heights.append(value['height'])
    lengths.append(value['length'])
    widths.append(value['width'])

# 将Python列表转换为numpy数组
heights = np.array(heights)
lengths = np.array(lengths)
widths = np.array(widths)
np.savez('../visualize/data_arrays.npz', heights=heights, lengths=lengths, widths=widths)
# 定义一个函数，计算并打印所需的统计数据
def print_stats(data, name):
    print(f"{name.capitalize()} Stats:")
    print(f"Maximum {name}: {np.max(data)}")
    print(f"Minimum {name}: {np.min(data)}")
    print(f"Average {name}: {np.mean(data)}")
    print(f"Variance of {name}: {np.var(data)}")
    print("")

# 输出统计数据
print_stats(heights, 'height')
print_stats(lengths, 'length')
print_stats(widths, 'width')
