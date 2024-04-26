import importlib
import json
import new_modle

data_list = []

# 打开并读取JSON文件
with open('data.json', 'r') as file:
    # 加载JSON数据
    data = json.load(file)
    
    with open("integration_output.txt", "w") as f:
        for v in data.values():
            with open("config_case.json", "w") as trans:
                json.dump(v, trans, indent=4)
            
            # refresh data and call the script
            importlib.reload(new_modle)
            order_ind = new_modle.main()
            
            data_list.append([])
            data_list[-1].append(order_ind[0].fitness.values[0])
            f.write(str(order_ind[0].fitness.values[0]) + '\n')
            for _ in order_ind[0]:
                data_list[-1].append(_)
                f.write(str(_) + '\n')
            f.write('\n')

for _ in range(len(data_list[0])):
    average = sum([data_list[i][_] for i in range(len(data_list))]) / len(data_list)
    variance = sum([(data_list[i][_] - average) ** 2 for i in range(len(data_list))]) / len(data_list)
    
    print("Average:", average, "| Variance:", variance)
