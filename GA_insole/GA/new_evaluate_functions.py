import json

# 加载配置文件
with open("config_case.json", "r") as config_file:
    config = json.load(config_file)
# 从配置文件中读取的固定常量
length, width, height = config['length'], config['width'], config['height']

param_bounds = [
    (length, length * 1.1),  # length
    (width, width * 1.1),  # width
    (3, 15),  # thickness
    (height * 0.7, height * 1.3),  # height
    (0, (70 / 20) ** 0.5 * 100)  # density
]

w1, w2, w3, w4 = (10, 1, -0.000001, -1)


def buffer(t, d, Es=20, ps=100, n=2, k1=3, k2=2):
    E = Es * (d / ps) ** n
    return k1 * t - k2 * E ** 2


def support(l, w, t, h, d, Es=20, ps=100, n=2, v=0.07, k3a=1, k3b=1, k3c=1, k3d=1):
    rs = l ** 2 / (8 * h)
    E = Es * (d / ps) ** n
    return k3a * h - k3b * w / l - k3c * t ** 5 / rs + k3d * E * t ** 3 / (12 * (1 - v ** 2))


def weight(l, w, t, h, d):
    return l * w * (t + h / 3) * d


def fit(l, w, h):
    return (l * w * h - length * width * height) ** 2 / 9


def total(l, w, t, h, d):
    return w1 * buffer(t, d) + w2 * support(l, w, t, h, d) + w3 * weight(l, w, t, h, d) + w4 * fit(l, w, h)
