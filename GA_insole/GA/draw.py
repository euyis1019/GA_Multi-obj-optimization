import matplotlib.pyplot as plt

generations = 100
graphs_num = 7

name_map = ["Best_Ind Fitness", "Population Fitness", "Length", "Width", "Thickness", "Height", "Density"]

x = [_ for _ in range(1, generations + 1)]

y = [[] for _ in range(graphs_num)]
file = open("output.txt", "r")
for _ in range(1, generations + 1):
    for i in range(graphs_num):
        y[i].append(float(file.readline()))
    file.readline()
file.close()

# 使用plot()函数创建折线图
for _ in range(graphs_num):
    plt.close()
    
    plt.plot(x, y[_])

    # 添加标题和轴标签
    plt.title('Visualization')
    plt.xlabel('Generations')
    plt.ylabel(name_map[_])
    
    # 显示网格（可选）
    plt.grid(True)
    
    # 保存图表为本地文件，指定文件名和格式
    plt.savefig('line_graph_' + str(_) + '.png', format='png', dpi=1000)
