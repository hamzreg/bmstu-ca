from dataclasses import dataclass
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from random import uniform

@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 4"

    font_bold = "FreeMono 14 bold"
    font = "FreeMono 14"

@dataclass
class Colour:

    back = "#ABCDEF"
    button = "#DDF1FF"


def draw(all_rms):
    """
        Вывод графиков.
    """

    plt.plot(all_rms[0][2], all_rms[0][3], 'ro', label = "Данные")

    for rms in all_rms:
        plt.plot(rms[2], rms[0], label = "p = " + str(rms[1]))

    plt.grid()
    plt.legend(fontsize = 20,
               ncol = 2)
    plt.tick_params(labelsize = 20)
    plt.title("Наилучшее среднеквадратичное приближение", fontsize = 20)
    plt.xlabel("x", fontsize = 20)
    plt.ylabel("y", fontsize = 20)

    plt.show()

def get_rms(arguments, factors_a):
    """
        Получить наилучшее среднеквадратичное приближение.
    """

    rms = []

    for x in arguments:
        result = 0

        for i in range(len(factors_a)):
            result += factors_a[i] * (x ** i)

        rms.append(result)
    
    return rms

def get_x_y(table_nodes):
    """
        Получить список аргументов и значений.
    """

    x, y = [], []

    for node in table_nodes:
        x.append(node[0])
        y.append(node[1])
    
    return x, y


def insert_column(matrix, free_membrs, j):
    """
        Вставка столбца свободных членов в
        матрицу.
    """

    i = 0

    for row in matrix:
        row[j], free_membrs[i] = free_membrs[i], row[j]
        i += 1
    
    return matrix, free_membrs


def get_factors_a(matrix, free_membrs):
    """
        Получить коэффициенты a.
    """

    main_det = np.linalg.det(matrix)
    factors_a = []

    for j in range(len(matrix[0])):
        matrix, free_membrs = insert_column(matrix, free_membrs, j)
        now_det = np.linalg.det(matrix)
        factors_a.append(now_det / main_det)
        matrix, free_membrs = insert_column(matrix, free_membrs, j)
    
    return factors_a

def get_prod_x(table_nodes, k, m):
    """
        Получить произведение (x^k, x^m).
    """

    prod_x = 0

    for node in table_nodes:
        prod_x += node[2] * (node[0] ** (k + m))

    return prod_x

def get_prod_y(table_nodes, k):
    """
        Получить произведение (y, x^k).
    """

    prod_y = 0

    for node in table_nodes:
        prod_y += node[2] * node[1] * (node[0] ** k)
    
    return prod_y

def get_matrix(table_nodes, power):
    """
        Создание СЛАУ.
    """

    matrix = []
    free_membrs = []

    for k in range(power + 1):
        row = []

        for m in range(power + 1):
            row.append(get_prod_x(table_nodes, k, m))
        
        matrix.append(row)
        
        free_membrs.append(get_prod_y(table_nodes, k))
    
    return matrix, free_membrs

def get_table_nodes(table_entry):
    """
        Ввод таблицы узлов.
    """

    table_nodes = []

    for entry in table_entry:
        x = float(entry[0].get())
        y = float(entry[1].get())
        p = float(entry[2].get())

        table_nodes.append([x, y, p])
    
    return table_nodes

def mediator(table_entry, power_entry, all_rms):
    """
        Получить список данных для вывода графиков.
    """

    table_nodes = get_table_nodes(table_entry)
    power = int(power_entry.get())

    matrix, free_membrs = get_matrix(table_nodes, power)
    factors_a = get_factors_a(matrix, free_membrs)
    x, y = get_x_y(table_nodes)
    all_rms.append([get_rms(x, factors_a), power, x, y])

def input_nodes(window, count_nodes_entry):
    """
        Ввод узлов.
    """

    x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font_bold,
                             bg = Colour.back)
    x_lbl.place(x = 50, y = 250)

    y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font_bold,
                             bg = Colour.back)
    y_lbl.place(x = 300, y = 250)

    p_lbl = tk.Label(window, text = "p:",
                             font = Graphic.font_bold,
                             bg = Colour.back)
    p_lbl.place(x = 550, y = 250)

    count_nodes = int(count_nodes_entry.get())
    y_start = 310

    table_entry = []

    for i in range(count_nodes):
        x_entry = tk.Entry(window, font = Graphic.font,
                                   justify = tk.CENTER,
                                   width = 8)
        x_entry.insert(tk.END, str(i + 1))
        x_entry.place(x = 50, y = y_start + i * 60)

        y_entry = tk.Entry(window, font = Graphic.font,
                                   justify = tk.CENTER,
                                   width = 8)
        y_entry.insert(tk.END, str(uniform(0, 10)))
        y_entry.place(x = 300, y = y_start + i * 60)

        p_entry = tk.Entry(window, font = Graphic.font,
                                   justify = tk.CENTER,
                                   width = 8)
        p_entry.place(x = 550, y = y_start + i * 60)
        p_entry.insert(tk.END, "1")

        table_entry.append([x_entry, y_entry, p_entry])

    # Ввод степени полинома

    power_lbl = tk.Label(window, text = "Введите степень полинома:",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    power_lbl.place(x = 50, y = y_start + 60 * count_nodes)

    power_entry = tk.Entry(window, font = Graphic.font,
                                   justify = tk.CENTER)
    power_entry.place(x = 50, y = y_start + 60 * (count_nodes + 1))

    # Решение

    all_rms = []

    solve_button = tk.Button(window, text = "Решить",
                                     bg = Colour.button,
                                     font = Graphic.font,
                                     bd = 6,
                                     command = lambda : mediator(table_entry, power_entry, all_rms))
    solve_button.place(x = 50, y = y_start + 60 * (count_nodes + 2))

    draw_button = tk.Button(window, text = "Нарисовать",
                                    bg = Colour.button,
                                    font = Graphic.font,
                                    bd = 6,
                                    command = lambda : draw(all_rms))
    draw_button.place(x = 50, y = y_start + 60 * (count_nodes + 3) + 40)


def create_interface():
    """
        Создание интерфейса.
    """

    window = tk.Tk()
    window.title(Graphic.window_title)
    window.geometry(Graphic.window_size)
    window.config(bg = Colour.back)

    # Ввод количества узлов

    count_nodes_lbl = tk.Label(window, text = "Введите число узлов:",
                                       font = Graphic.font_bold,
                                       bg = Colour.back)
    count_nodes_lbl.place(x = 50, y = 50)

    count_nodes_entry = tk.Entry(window, font = Graphic.font,
                                         justify = tk.CENTER)
    count_nodes_entry.place(x = 50, y = 110)

    # Ввод узлов

    input_nodes_button = tk.Button(window, text = "Ввести узлы",
                                           bg = Colour.button,
                                           font = Graphic.font,
                                           bd = 6,
                                           command = lambda : input_nodes(window, count_nodes_entry))
    input_nodes_button.place(x = 50, y = 170)

    window.mainloop()

if __name__ == "__main__":
    create_interface()
