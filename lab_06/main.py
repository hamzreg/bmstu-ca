from math import fabs

def print_result(table, deriv_table):
    """
        Печать таблицы
        с разностными производными.
    """
    
    print("RESULT\n")
    print("-" * 54)
    for i in range(len(table[0])):
        print("| {:^.0f} | {:^.3f} |".format(table[0][i], table[1][i]), end= "")

        for j in range(len(deriv_table)):
            if type(deriv_table[j][i]) == float:
                print(" {:^4.3f} |".format(deriv_table[j][i]), end= "")
            elif j == len(deriv_table) - 1:
                print("   -    |", end= "")
            else:
                print("   -   |", end= "")
        print()
    print("-" * 54)


def two_deriv(table):
    """
        Вычисление второй
        разностной производной.
    """

    result = ["-"]
    step = fabs(table[0][1] - table[0][0])

    for i in range(1, len(table[0]) - 1):
        result.append((table[1][i - 1] - 2 * table[1][i] + table[1][i+1]) / (step ** 2))
    
    result.append("-")

    return result


def alignment_vars(table):
    """
        Вычисление разностной производной
        при помощи выравнивающих переменных.
    """

    result = []

    for i in range(len(table[0]) - 1):
        now = (1 / table[1][i + 1] - 1 / table[1][i]) / (1 / table[0][i + 1] - 1 / table[0][i])
        result.append((now * (table[1][i] ** 2)) / (table[0][i] ** 2))
    result.append("-")

    return result
    

def two_runge(table):
    """
        Вычисление разностной производной
        при помощи 2-ой формулы Рунге.
        Расчет ведется по левой разностной
        производной.
    """

    result = ["-", "-"]
    step = fabs(table[0][1] - table[0][0])

    for i in range(2, len(table[0])):
        a = (table[1][i] - table[1][i-1]) / step
        b = (table[1][i] - table[1][i-2]) / (2 * step)

        result.append(a + a - b)

    result.append("-")

    return result


def central_deriv(table):
    """
        Вычисление центральной
        разностной производной.
    """

    result = ["-"]
    step = fabs(table[0][1] - table[0][0])

    for i in range(1, len(table[0]) - 1):
        result.append((table[1][i + 1] - table[1][i-1]) / (2 *step))
    
    result.append("-")

    return result 


def one_sided_deriv(table):
    """
        Вычисление левой разностной
        производной.
    """

    result = ["-"]
    step = fabs(table[0][1] - table[0][0])

    for i in range(1, len(table[0])):
        result.append((table[1][i] - table[1][i-1]) / step)

    return result    


def fill_deriv_table(table):
    """
        Заполнение таблицы
        разностными производными.
    """

    result = []

    result.append(one_sided_deriv(table))
    result.append(central_deriv(table))
    result.append(two_runge(table))
    result.append(alignment_vars(table))
    result.append(two_deriv(table))

    return result


def data_input():
    """
       Ввод данных.
    """

    n = int(input(("Введите число узлов: ")))

    table = [[], []]

    print("Введите значения аргументов:")

    for _ in range(n):
        table[0].append(float(input()))

    print("Введите значения функции:")
    
    for _ in range(n):
        table[1].append(float(input()))
    
    return table


if __name__ == "__main__":
    """
        Ввод данных.
        Заполнение таблицы.
        Печать результата.
    """

    table = data_input()
    result = fill_deriv_table(table)
    print_result(table, result)
