import random
import importlib
from tqdm import tqdm
from deap import base, creator, tools
import new_evaluate_functions

# refresh data
importlib.reload(new_evaluate_functions)
param_bounds = new_evaluate_functions.param_bounds
total = new_evaluate_functions.total


# 定义问题的参数
# 可以更改的变量：问题类型、问题维度、种群大小、迭代次数等
# 示例问题：最大化一个二元函数 f(x, y) = x^2 + y^2
population_size = 300
num_generations = 100
CXPB, MUTPB = 0.5, 0.2  # 交叉和变异的概率


# 创建适应度评价类和个体类
creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.Fitness)


# 定义个体初始化方法和评价函数
# 可以更改的变量：问题的初始化范围、评价函数
def init_individual():
    return [random.uniform(lower, upper) for lower, upper in param_bounds]


def evaluate(individual):
    # 解包个体的参数并作为参数传入函数
    return total(*individual),


# 初始化 DEAP 工具箱
toolbox = base.Toolbox()

toolbox.register("individual", tools.initIterate, creator.Individual, init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, low=[_[0] for _ in param_bounds], up=[_[1] for _ in param_bounds], eta=1.0, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


# 遗传算法主循环
def main():
    refresh_file()
    
    order_ind = []
    
    # 生成初始种群
    population = toolbox.population(n=population_size)
    
    # 评价种群中的个体
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
    
    for gen in tqdm(range(num_generations), desc="进化进度"):  # 使用tqdm包装循环，提供进度条
        # 选择下一代个体
        offspring = toolbox.select(population, len(population))
        
        # 复制选定个体
        offspring = list(map(toolbox.clone, offspring))
        
        # 对选定个体进行交叉
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        
        # 对选定个体进行变异
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        # 评估所有适应度无效的个体
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # 用变异后的个体替代原始种群
        population[:] = offspring
        
        # 选取当前种群最优个体
        order_ind = tools.selBest(population, population_size)
        
        output(order_ind)
    
    # 返回最优个体
    return order_ind


def refresh_file():
    file = open("output.txt", "w")
    file.close()
    
    return


def output(order_ind):
    file = open("output.txt", "a")
    
    file.write(str(order_ind[0].fitness.values[0]) + '\n')
    file.write(str(sum([order_ind[_].fitness.values[0] for _ in range(population_size * 95 // 100)]) / (population_size * 95 // 100)) + '\n')
    for _ in order_ind[0]:
        file.write(str(_) + '\n')
    file.write('\n')
    
    file.close()
    
    return


if __name__ == "__main__":
    order_ind = main()
    
    print("Minimum sizes:", [_[0] for _ in param_bounds])
    
    print("Best solution:", order_ind[0])
    
    print("Maximum sizes:", [_[1] for _ in param_bounds])
    
    print("Whether converge: ", end='')
    for best, bounds in zip(order_ind[0], param_bounds):
        if abs(best - bounds[0]) < 0.01 or abs(best - bounds[1]) < 0.01:
            print(False, end=' ')
        else:
            print(True, end=' ')
    print()
    
    print("Best fitness:", order_ind[0].fitness.values)
    
    print()
