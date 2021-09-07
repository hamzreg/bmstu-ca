from dataclasses import dataclass

from newton_interpolation import newton_interpolation

@dataclass
class Constants:
    count_x = 11


def print_results(argument, spline_result, newton_result):
    """
        Печать результатов.
    """
    print("")
    print("Значение аргумента: ", argument)
    print("Результат интерполяции кубическим сплайном: {:.5f}".format(spline_result))
    print("Результат интерполяции полиномом Ньютона (3 степень): {:.5f}".format(newton_result))
    print("")


def get_argument_position(arguments, argument):
    """
       Поиск позиции правой границы интервала,
       в который входит искомый аргумент.
    """

    for i in range(len(arguments)):
        if arguments[i] >= argument:
            return i


def get_value_polynom(value_table, factors, argument):
    """
       Получить значение полинома.
    """

    position = get_argument_position(value_table[0], argument) - 1
    step = argument - value_table[0][position]

    polynom = factors[0][position] + factors[1][position] * step + \
              factors[2][position] * step ** 2 + \
              factors[3][position] * step ** 2 * step 
    return polynom


def get_factors_a(values):
    """
        Получить коэффициенты a.
    """

    factors_a = []

    for i in range(1, Constants.count_x):
        factors_a.append(values[i - 1])
    
    return factors_a


def get_factors_b(value_table, factors_c):
    """
        Получить коэффициенты b.
    """

    factors_b = []

    for i in range(1, Constants.count_x - 2):
        now_step = value_table[0][i] - value_table[0][i - 1]
        now_values_diff = value_table[1][i] - value_table[1][i - 1]
        
        now_b = now_values_diff / now_step - \
                now_step * (factors_c[i] + 2 * factors_c[i - 1]) / 3
        factors_b.append(now_b)

    # b_n
    
    step_n = value_table[0][Constants.count_x - 1] - \
             value_table[0][Constants.count_x - 2]
    values_diff_n = value_table[1][Constants.count_x - 1] - \
                    value_table[1][Constants.count_x - 2]

    b_n = values_diff_n / step_n - \
          step_n * 2 * factors_c[Constants.count_x - 2] / 3
    factors_b.append(b_n)

    return factors_b


def get_factors_e(arguments):
    """
        Получить коэффициенты e.
    """
    
    factors_e = [0]

    for i in range(2, Constants.count_x):
        now_step = arguments[i] - arguments[i - 1]
        prev_step = arguments[i - 1] - arguments[i - 2]
        
        now_e = -now_step / (prev_step * factors_e[i - 2] + \
                2 * (prev_step + now_step))
        factors_e.append(now_e)
    
    return factors_e


def get_factors_g(value_table, factors_e):
    """
        Получить коэффициенты g.
    """

    factors_g = [0]

    for i in range(2, Constants.count_x):
        now_step = value_table[0][i] - value_table[0][i - 1]
        prev_step = value_table[0][i - 1] - value_table[0][i - 2]
        
        now_values_diff = value_table[1][i] - value_table[1][i - 1]
        prev_values_diff = value_table[1][i - 1] - value_table[1][i - 2]
        now_f = 3 * (now_values_diff / now_step - prev_values_diff / prev_step)

        now_g = (now_f - now_step * factors_g[i - 2]) / \
                (now_step * factors_e[i - 2] + 2 * (prev_step + now_step))
        factors_g.append(now_g)
    
    return factors_g


def straight_run(value_table):
    """
        Прямой ход.
    """

    factors_e = get_factors_e(value_table[0])
    factors_g = get_factors_g(value_table, factors_e)

    return factors_e, factors_g


def reverse(factors_e, factors_g):
    """
        Обратный ход.
    """

    factors_c = [0, 0]
    now_end_diff = 0

    for i in range(Constants.count_x - 2, 0, -1):
        now_c = factors_e[i] * factors_c[len(factors_c) - 1 - now_end_diff] + factors_g[i]
        now_end_diff += 1
        factors_c.insert(1, now_c)
    
    return factors_c


def get_factors_c(value_table):
    """
        Получить коэффициенты c.
    """

    factors_e, factors_g = straight_run(value_table)
    factors_c = reverse(factors_e, factors_g)

    return factors_c


def get_factors_d(arguments, factors_c):
    """
       Получить коэффициенты d.
    """

    factors_d = []

    for i in range(1, Constants.count_x - 2):
        now_step = arguments[i] - arguments[i - 1]
        now_d = (factors_c[i] - factors_c[i - 1]) / (3 * now_step)
        factors_d.append(now_d)
    
    # d_n
    
    step_n = arguments[Constants.count_x - 1] - \
             arguments[Constants.count_x - 2]
    d_n = -factors_c[Constants.count_x - 2] / (3 * step_n)
    factors_d.append(d_n)

    return factors_d


def spline_interpolation(value_table, argument):
    """
       Интерполяция кубическим сплайном.
    """

    factors = []

    factors_a = get_factors_a(value_table[1])
    factors.append(factors_a)
    factors_c = get_factors_c(value_table)
    factors_b = get_factors_b(value_table, factors_c)
    factors.append(factors_b)
    factors.append(factors_c)
    factors_d = get_factors_d(value_table[0], factors_c)
    factors.append(factors_d)

    spline_polynom = get_value_polynom(value_table, factors, argument)

    return spline_polynom


def form_value_table():
    """
        Формирование таблицы значений
        y = x^2, x в диапазоне [0...10].
    """

    value_table = [[], []]

    for x in range(Constants.count_x):
        value_table[0].append(x)
        value_table[1].append(x ** 2)

    return value_table


if __name__ == "__main__":
    """
       Сравнение результатов интерполяции
       - кубическим сплайном;
       - полиномом Ньютона 3-й степени.
    """

    value_table = form_value_table()

    argument = 0.5
    spline_result = spline_interpolation(value_table, argument)
    newton_result = newton_interpolation(value_table, Constants.count_x, 3, argument)
    print_results(argument, spline_result, newton_result)


    argument = 5.5
    spline_result = spline_interpolation(value_table, argument)
    newton_result = newton_interpolation(value_table, Constants.count_x, 3, argument)
    print_results(argument, spline_result, newton_result)




