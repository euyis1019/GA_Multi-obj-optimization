import pandas as pd
import numpy as np
import random
from deap import base
from deap import creator
from deap import tools
from evaluate_function import Buffer, Support, light_weight, fit, cal_area
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

a, b, c, d = config['a'], config['b'], config['c'], config['d']

param_bounds = {
    'length': (0, 10),
    'width': (0, 10),
    'R': (0, 10),
    'Thickness': (0, 10),
    'Hardness': (0, 100),
    'A': (-10, 10),
    'B': (-10, 10),
    'C': (-10, 10),
    'D': (-10, 10),
}

# Ensure the weights
weights = (-1., -1., -1., -1.)
################################
creator.create("FitnessMin", base.Fitness, weights=weights)
creator.create("Individual", dict, fitness=creator.FitnessMin)

# 评估函数，根据个体字典参数计算适应度
def evaluate(individual):
    # 从个体中提取变量
    thickness = individual['Thickness']
    hardness = individual['Hardness']
    r = individual['R']
    w = individual['width']
    l = individual['length']
    area = cal_area(l, w)  # 假设有一个计算面积的函数
    A, B, C, D = individual['A'], individual['B'], individual['C'], individual['D']
    buffer = Buffer(thickness, hardness)
    support = Support(r, w, l)
    lw = light_weight(thickness, area, hardness)  # 修改de为hardness
    f = fit(l, w, A, B, C, D, a, b, c, d)
    return (buffer, support, lw, f)

# 随机生成函数，用于生成个体的键值对
def random_generation():
    individual = {}
    for key, (lower_bound, upper_bound) in param_bounds.items():
        individual[key] = random.uniform(lower_bound, upper_bound)  # 使用uniform以支持浮点数
    return individual

toolbox = base.Toolbox()

# 注册随机生成函数
toolbox.register("attr_float", random_generation)
# 使用initIterate来初始化个体，更适合字典类型的个体
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
# 初始化群体
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 注册其他遗传算法操作
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
