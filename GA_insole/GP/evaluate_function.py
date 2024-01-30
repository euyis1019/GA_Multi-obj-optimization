import math
from scipy.integrate import dblquad
# ---------------------------------------------------------------
# Copyright (c) 2024-2025 SCNU, Yifu Guo And GDUT. All rights reserved.
# Licensed under the Apache License, Version 2.0
# ---------------------------------------------------------------


#Hmat == Hardness
#Tmat == Thickness
#RWL ----> the Input len width height


def cal_area(length, width, A, B, C, D):
    # Define surface Function
    # Ax^2 + Bx + Cy^2 +D
    def surface(x, y):
        return A * x ** 2 + B * x + C * y ** 2 + D

    # cal double  integral
    area, error = dblquad(surface, 0, width, lambda x: 0, lambda x: length)

    return area

def Buffer(thickness, hardness, a1=1, k1=0.6, k2=0.4):
    return (-a1) * (k1 * thickness - k2 * hardness ** 2)

def Support(r, w, l, a2=1, k3a=0.7, k3b=0.1, k3c=0.3):
    return (a2) * (k3a * r - k3b * w / l - k3c* (r/(w*l)) ** 2)

def light_weight(thickness, area, de, a3=1):
    density = calculate_density(de)
    V = area * thickness
    return a3 * (density * V)

def calculate_density(hardness):  # The variables range from 1 to 70
    es = 20
    de_s = 100
    n = 2  # Open cell foamed material，n is equal to 2.
    if n == 2:
        de_f = math.sqrt(hardness / es) * de_s
        return de_f
    else:
        print("wrong")

# 2 groups of ABCD(Surface Function) and scope.Scope is generative
# Fit function definition
def fit(len, width, A, B, C, D, a, b, c, d, a4=1):#len width is Generative
    # Define surface Function S(x, y) - Actual Surface Function H_actual(x, y)
    def integrand(x, y, A, B, C, D, a, b, c, d):
        S = A * x**2 + B * x + C * y**2 + D  # Surface function S(x, y)
        H = a * x**2 + b * x + c * y**2 + d  # Actual height H_actual(x, y)
        return (S - H)**2

    # Calculate the double integral over the area A
    area, error = dblquad(integrand, 0, width, lambda y: 0, lambda y: len, args=(A, B, C, D, a, b, c, d))

    # Multiply by the coefficient Q4
    return -a4 * area
def Ctotal(thickness, Hmat, Rarch, Warch, Larch, Vmat, Pmat, area, w1, w2, w3, w4,A,B,C,D,a,b,c,d):
    # Assuming Cfit is a predefined function
    return (
        w1 * Buffer(thickness, Hmat) +
        w2 * Support(Rarch, Warch, Larch) +
        w3 * light_weight(thickness, area, Hmat)
        + w4 * fit(Larch, Warch,A,B,C,D,a,b,c,d)  # Replace Cfit with the actual function definition
    )


