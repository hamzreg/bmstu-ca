from dataclasses import dataclass
import matplotlib.pyplot as plt
from math import sin, cos, pi, exp
from numpy.polynomial.legendre import leggauss
from numpy import arange


@dataclass
class Limits:
    """
        Пределы операций.
    """

    start = 0
    end = pi / 2

    t_start = 0.05
    t_end = 10


def explore_t(func, n, m):
    """
        Исследование ε(τ).
    """

    x, y  = [], []
    t_step = 0.05

    for t in arange(Limits.t_start, Limits.t_end + t_step, t_step):
        x.append(t)
        y.append(func(t))
    
    plt.plot(x, y, label = "N = {0}, M = {1}, Simpson-Gauss".format(n, m))
    plt.legend(fontsize = 20)
    plt.ylabel("∫∫", fontsize = 20)
    plt.xlabel("τ", fontsize = 20)
    plt.tick_params(labelsize = 20)
    plt.show()


def simpson(func, a, b, n):
    """
        Интегрирование при помощи
        формулы Симпсона.
    """
    
    h = (b - a) / (n - 1)
    x = a
    result = 0

    for _ in range((n  - 1) // 2):
        result += func(x) + 4 * func(x + h) + func(x + 2 * h)
        x += 2 * h
    
    result *= (h / 3)

    return result
    

def change_x(a, b, t):
    """
        Изменение x для применения
        квадратурной формулы Гаусса.
    """

    return (b + a) / 2 + (b - a) * t / 2


def change_func(func, x):
    """
        Изменение функции.
    """

    return lambda y: func(x, y)


def gauss(func, a, b, m):
    """
        Интегрирование при помощи
        формулы Гаусса.
    """

    arguments, factors = leggauss(m)
    result = 0

    for i in range(m):
        now_x = change_x(a, b, arguments[i])
        result += (b - a) / 2 * factors[i] * func(now_x)

    return result


def get_integrable_func(t):
    """
        Интегрируемая функция.
    """

    inter_func = lambda x, y: 2 * cos(x) / \
                 (1 - (sin(x) ** 2) * (cos(y) ** 2))
    integrable_func = lambda x, y: (4 / pi) * \
                      (1 - exp(-t * inter_func(x, y))) * \
                      cos(x) * sin(x)

    return integrable_func


def get_double_integral(func, n, m):
    """
        Вычисление двукратного интеграла.
    """

    gauss_inter = lambda x: gauss(change_func(func, x), Limits.start, Limits.end, m)
    return simpson(gauss_inter, Limits.start, Limits.end, n)


def data_input():
    """
        Ввод n, m, t.
    """

    n = int(input("\nВведите N: "))
    m = int(input("\nВведите M: "))

    t = float(input("\nВведите τ: "))

    return n, m, t


def explore_count_nodes():
    """
       Исследование влияния количества узлов
       по каждому направлению.
    """

    t = 1
    n = 5

    for m in range(3, 8):
        double_integral = lambda x: get_double_integral(get_integrable_func(x), n, m)
        print("\nN = {0}, M = {1}, Двукратный интеграл = {2}".format(n, m, double_integral(t)))

        x, y  = [], []
        t_step = 0.05

        for t in arange(Limits.t_start, Limits.t_end + t_step, t_step):
            x.append(t)
            y.append(double_integral(t))
        
        plt.plot(x, y, label = "N = {0}, M = {1}, Simpson-Gauss".format(n, m))
    
    plt.legend(fontsize = 20)
    plt.ylabel("∫∫", fontsize = 20)
    plt.xlabel("τ", fontsize = 20)
    plt.tick_params(labelsize = 20)
    plt.show()

    m = 5

    for n in range(3, 8):
        double_integral = lambda x: get_double_integral(get_integrable_func(x), n, m)
        print("\nN = {0}, M = {1}, Двукратный интеграл = {2}".format(n, m, double_integral(t)))

        x, y  = [], []
        t_step = 0.05

        for t in arange(Limits.t_start, Limits.t_end + t_step, t_step):
            x.append(t)
            y.append(double_integral(t))
        
        plt.plot(x, y, label = "N = {0}, M = {1}, Simpson-Gauss".format(n, m))
    
    plt.legend(fontsize = 20)
    plt.ylabel("∫∫", fontsize = 20)
    plt.xlabel("τ", fontsize = 20)
    plt.tick_params(labelsize = 20)
    plt.show()


if __name__ == "__main__":
    """
        Ввод данных.
        Печать результата.
        Исследования.
    """

    n, m, t = data_input()

    double_integral = lambda x: get_double_integral(get_integrable_func(x), n, m)

    print("\nДвукратный интеграл = ", double_integral(t))

    explore_t(double_integral, n, m)
    explore_count_nodes()
    