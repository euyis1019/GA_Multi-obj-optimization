import pandas as pd
import numpy as np
import random
from deap import base
from deap import creator
from deap import tools
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
#########Insure the weights########
weights = (-1., -1., -1., -1.)
################################
creator.create("FitnessMin", base.Fitness, weights=weights)
creator.create("Individual", list, fitness=creator.FitnessMin)
def evaluate(individual):
    buffer =  Buffer(thickness, hardness)
    support = Support(r, w, l)
    lw = light_weight(thickness, area, de)
    f = fit(len, width, A, B, C, D, a, b, c, d)
    return(buffer, support, lw, f)

def n_per_product():
    params = []

    for key, (lower_bound, upper_bound) in param_bounds.items():
        param_value = random.randint(lower_bound, upper_bound)
        params.append(param_value)

    return params

toolbox = base.Toolbox()

toolbox.register("n_per_product", n_per_product)

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.n_per_product, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
print(123)