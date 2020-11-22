import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import matplotlib.colors as clr
# библиотеки
# инициализиация
pmin, pmax, qmin, qmax = -2.5, 1.5, -2, 2
# пусть c = p + iq и p меняется в диапазоне от pmin до pmax,
# а q меняется в диапазоне от qmin до qmax
ppoints, qpoints = 200, 200
# число точек по горизонтали и вертикали
max_iterations = 300
# максимальное количество итераций
infinity_border = 10
# если ушли на это расстояние, считаем, что ушли на бесконечность
def mandelbrot(pmin, pmax, ppoints, qmin, qmax, qpoints,
               max_iterations=200, infinity_border=10):
    image = np.zeros((ppoints, qpoints))
    p, q = np.mgrid[pmin:pmax:(ppoints*1j), qmin:qmax:(qpoints*1j)]
    c = p + 1j*q
    z = np.zeros_like(c)
    for k in range(max_iterations):
        z = z**2 + c
        mask = (np.abs(z) > infinity_border) & (image == 0)
        image[mask] = k
        z[mask] = np.nan
    return -image.T
#image = mandelbrot(-0.793191078177363, 0.16093721735804, 1000, -0.793191, 0.160937, 1000)
plt.figure(figsize=(10, 10))
colorpoints = [(1 - (1 - q) ** 4, c) for q, c in zip(np.linspace(0, 1, 20),
                                                     cycle(['#ffff88', '#000000',
                                                            '#ffaa00', ]))]
cmap = clr.LinearSegmentedColormap.from_list('mycmap',
                                             colorpoints, N=2048)
# LinearSegmentedColormap создаёт палитру по заданным точкам и заданным цветам
# можете попробовать выбрать другие цвета
plt.xticks([])
plt.yticks([])
image = mandelbrot(-2.5, 1.5, 1000, -2, 2, 1000)
plt.imshow(image, cmap=cmap, interpolation='none')
plt.show()
plt.savefig("mandelbrot-full.png")

p_center, q_center = -0.793191078177363, 0.16093721735804
for i in range(1,11):
    scalefactor = i / 12000
    plt.xticks([])
    plt.yticks([])
    pmin_ = (pmin - p_center) * scalefactor + p_center
    qmin_ = (qmin - q_center) * scalefactor + q_center
    pmax_ = (pmax - p_center) * scalefactor + p_center
    qmax_ = (qmax - q_center) * scalefactor + q_center
    image = mandelbrot(pmin_, pmax_, 500, qmin_, qmax_, 500)
    print("(", pmin_, ",", pmax_, ") (", qmin_, ",", qmax_, ")")
    plt.figure(figsize=(10, 10))
    plt.imshow(image, cmap='flag', interpolation='none')
    filename = "mandelbrot-" + str(i) + ".png"
    plt.savefig(filename)
    print(filename  + " saved")
