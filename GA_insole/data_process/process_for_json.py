import json

def filter_data(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)
    num = 0
    # 创建一个新的字典来存储筛选后的数据
    filtered_data = {}

    for file_name, metrics in data.items():
        # 保留 height 和 width 都不为0的条目
        file_name = file_name.replace(".xls", "")
        if metrics['height'] != 0 and metrics['width'] != 0:
            filtered_data[file_name] = metrics
            num += 1
    # 如果你想要保存筛选后的数据到一个新的 JSON 文件
    with open(output_file, 'w') as file:
        json.dump(filtered_data, file, indent=4)
    print(num)
    return filtered_data

if __name__ == "__main__":
    input_file = 'extracted_data.json'
    output_file = 'data.json'
    filtered_data = filter_data(input_file, output_file)
    print(f"筛选后的数据已保存到 '{output_file}'.")
