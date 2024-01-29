import os
import pandas as pd
import json

def extract_data(file_path):
    # 读取 Excel 文件并提取特定单元格数据
    try:
        # 根据文件类型选择引擎
        engine = 'openpyxl' if file_path.endswith('.xlsx') else 'xlrd'
        df = pd.read_excel(file_path, engine=engine, header=None)
        # 使用数字索引来访问列，'C'列对应索引2
        data = {
            'height': df.iat[11, 2],  # 使用 iat 来访问特定单元格的数据
            'length': df.iat[12, 2],
            'width': df.iat[13, 2]
        }
        return data
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误: {e}")
        return None

def main():
    folder_path = 'data_Foot'
    all_data = {}  # 用于保存所有文件的数据
    processed_count = 0  # 已处理文件计数器
    error_count = 0  # 处理时发生错误的文件计数器
    i =0
    for filename in os.listdir(folder_path):
        i+=1
        if filename.endswith('.xls'):
            file_path = os.path.join(folder_path, filename)
            data = extract_data(file_path)
            if data is not None:
                all_data[filename] = data
                processed_count += 1  # 增加已处理文件计数
            else:
                error_count += 1  # 增加错误文件计数
    print(all_data)
    # 将数据保存为 JSON 文件
    with open('extracted_data.json', 'w') as json_file:
        json.dump(all_data, json_file, indent=4)

    print(f"数据提取并保存到 'extracted_data.json'.")
    print(f"总计处理文件数: {processed_count}")
    print(f"处理时发生错误的文件数: {error_count}")
    print(i)
if __name__ == "__main__":
    main()
