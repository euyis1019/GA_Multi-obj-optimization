import pandas as pd
import numpy as np
import random
from deap import base
from deap import creator
from deap import tools
from evaluate_function import Buffer, Support, light_weight, fit, cal_area
import json
from tqdm import tqdm

# 加载配置文件
with open("/Users/eric/Documents/GitHub/Parameters Optimization for Insole/GA_insole/GP/config.json",
          "r") as config_file:
    config = json.load(config_file)

# 从配置文件中读取的固定常量
a, b, c, d = config['a'], config['b'], config['c'], config['d']

param_bounds = [
    (0, 10),  # length
    (0, 10),  # width
    (0, 10),  # R
    (0, 10),  # Thickness
    (0, 100),  # Hardness
    (-10, 10),  # A
    (-10, 10),  # B
    (-10, 10),  # C
    (-10, 10)  # D
]

weights = (-1., -1., -1., -1.)
creator.create("FitnessMin", base.Fitness, weights=weights)
creator.create("Individual", list, fitness=creator.FitnessMin)


def evaluate(individual):
    # 解包个体的参数
    length, width, R, Thickness, Hardness, A, B, C, D = individual
    area = cal_area(length, width, A, B, C, D)  # 假设有计算面积的函数
    buffer = Buffer(Thickness, Hardness)
    support = Support(R, width, length)
    lw = light_weight(Thickness, area, Hardness)  # 使用Thickness, area, 和Hardness
    # 使用个体的A, B, C, D 和 配置文件中的a, b, c, d
    f = fit(length, width, A, B, C, D, a, b, c, d)
    return (buffer, support, lw, f)


def random_generation():
    return [random.uniform(lower, upper) for lower, upper in param_bounds]


toolbox = base.Toolbox()

toolbox.register("attr_float", random_generation)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, low=[b[0] for b in param_bounds],
                 up=[b[1] for b in param_bounds], eta=1.0, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


# toolbox.population(n=10)
# print(toolbox.population(n=10))


def main():
    pop = toolbox.population(n=30)

    # 评估整个种群中每个个体的适应度
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    CXPB, MUTPB = 0.5, 0.2  # 交叉和变异的概率

    # 开始进化
    for g in tqdm(range(200), desc="进化进度"):  # 使用tqdm包装循环，提供进度条
        # 选择下一代个体
        offspring = toolbox.select(pop, len(pop))
        # 克隆选中的个体
        offspring = list(map(toolbox.clone, offspring))

        # 对后代应用交叉和变异
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # 评估所有适应度无效的个体
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring  # 更新种群

    # 寻找并返回最佳个体
    best = pop[np.argmin([sum(toolbox.evaluate(x)) for x in pop])]
    return best


if __name__ == "__main__":
    best_solution = main()
    print("Best Solution:", best_solution)
    print("Fitness:", best_solution.fitness.values)