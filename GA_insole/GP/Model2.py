from deap import base, creator, tools, algorithms
import random
import numpy as np
from evaluate_function import Buffer, Support, light_weight, fit, cal_area

# 参数范围
param_bounds = {
    'length': (0, 10),
    'width': (0, 10),
    'R': (0, 10),
    'Thickness': (3,15),
    'Hardness': (1, 70),
    'A': (-10, 10),
    'B': (-10, 10),
    'C': (-10, 10),
    'D': (-10, 10)
}


# 评价函数
def evalFit(individual, individual2):
    # 从种群1的个体中获取A, B, C, D
    A, B, C, D = individual[0], individual[1], individual[2], individual[3]

    # 从种群2的个体中获取len和width
    len, width = individual2[0], individual2[1]

    # 调用fit函数
    return (fit(len, width, A, B, C, D, 1, 1, 1, 1),)  # A, B, C, D


def evalSupport(individual):
    return (Support(individual[0], individual[1], individual[2], 1, 1, 1, 1),)  # len, width, R


def evalBufferLightWeight(individual):
    area = cal_area(1, 1, individual[0], individual[1], individual[2],
                    individual[3])  # Assume fixed length and width for area calculation
    return (
    Buffer(individual[0], individual[1]) + light_weight(individual[0], area, individual[1]),)  # Thickness, Hardness


# 设置GA基础结构
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# 遗传算法参数
POP_SIZE = 100
GENS = 40
CXPB, MUTPB = 0.5, 0.2

# 遗传操作
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# 统计操作
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

# 定义每个种群的结构和评价函数
populations = {'surface': {'params': ['A', 'B', 'C', 'D'], 'eval': evalFit},
               'arch': {'params': ['length', 'width', 'R'], 'eval': evalSupport},
               'material': {'params': ['Thickness', 'Hardness'], 'eval': evalBufferLightWeight}}

# 结果存储
# 结果存储
best_individuals = {}

# 对每个种群运行GA
for key, setting in populations.items():
    # 初始化种群
    for param in setting['params']:
        toolbox.register(f"attr_{param}", random.uniform, *param_bounds[param])
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     (toolbox.__getattribute__(f"attr_{param}") for param in setting['params']),
                     n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)


    # 初始化种群
    pop = toolbox.population(n=POP_SIZE)

    # 记录最佳个体
    hof = tools.HallOfFame(1)

    # 应用遗传算法
    algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, GENS, stats=stats, halloffame=hof, verbose=True)

    # 记录最佳个体
    best_individuals[key] = hof[0]

# 输出每个种群的最佳个体
for key, individual in best_individuals.items():
    print(f"Best individual from {key} population: {individual}")
    print(f"Fitness: {individual.fitness.values}\n")


# 如果需要，这里可以将这些最佳个体组合在一起，以形成最终的解决方案
