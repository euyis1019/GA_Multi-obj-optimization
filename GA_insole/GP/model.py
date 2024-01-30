from deap import base, creator, tools
import random
from deap import algorithms
import  numpy as np
from evaluate_function import Buffer, Support, light_weight, fit, cal_area
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

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# 为每个参数生成初始化函数
for param, (low, up) in param_bounds.items():
    toolbox.register(f"attr_{param}", random.uniform, low, up)

# 初始化个体，这里假设所有参数都是必需的
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_length, toolbox.attr_width, toolbox.attr_R,
                  toolbox.attr_Thickness, toolbox.attr_Hardness,
                  toolbox.attr_A, toolbox.attr_B, toolbox.attr_C, toolbox.attr_D,
                  toolbox.attr_a, toolbox.attr_b, toolbox.attr_c, toolbox.attr_d),
                 n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 评价函数调整
def evalBuffer(individual):
    thickness, hardness = individual[3], individual[4]
    return (Buffer(thickness, hardness),)

def evalSupport(individual):
    r, w, l = individual[2], individual[0], individual[1]
    return (Support(r, w, l),)

def evalLightWeight(individual):
    thickness, area = individual[3], cal_area(*individual[:6])
    de = individual[4]  # Assuming density is calculated from hardness
    return (light_weight(thickness, area, de),)

def evalFit(individual):
    return (fit(*individual[:12]),)  # Fit function takes the first 12 parameters

# 注册评价函数
toolbox.register("evaluate1", evalBuffer)
toolbox.register("evaluate2", evalSupport)
toolbox.register("evaluate3", evalLightWeight)
toolbox.register("evaluate4", evalFit)

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

# 多目标优化，可以选择一个或多个评价函数
toolbox.register("evaluate", evalBuffer)  # 可以通过参数更改不同的评价函数


def main():
    # 创建初始种群
    pop = toolbox.population(n=POP_SIZE)

    # 记录最佳个体
    hof = tools.HallOfFame(1)

    # 应用遗传算法
    pop, log = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, GENS, stats=stats, halloffame=hof, verbose=True)

    # 输出最佳个体和其适应度
    best_ind = hof[0]
    print("Best individual is: %s\nwith fitness: %s" % (best_ind, best_ind.fitness.values))

    return pop, log, hof


if __name__ == "__main__":
    main()
