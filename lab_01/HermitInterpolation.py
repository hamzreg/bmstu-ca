from NewtonInterpolation import SortTable


def CreateConfig(Table, SizeTable, power, argument):
    """
        Построение конфигурации узлов из таблицы Table
        размера SizeTable для построение полинома степени 
        power при аргументе argument.
    """

    center = 0

    while center < SizeTable:
        if Table[center][0] >= argument:
            break
        center += 1
    
    CountDerivs = (power + 1) // 2
    CountValues = power + 1 - CountDerivs

    if center == 0:
        return Table[:CountValues + 1]
    
    if center == SizeTable:
        return Table[SizeTable - CountValues - 1:]

    if abs(Table[center][0] - argument) > abs(argument - Table[center - 1][0]):
        center -= 1

    if (CountValues - 1) % 2 == 0:
        return Table[center - CountValues // 2:center + CountValues // 2 + 1]
    
    low = center - (CountValues - 1) // 2 - 1
    top = center + (CountValues - 1) // 2 + 1

    if abs(Table[top][0] - argument) > abs(argument - Table[low][0]):
        return Table[low:top]
    
    return Table[low: top + 1]


def CreateSplitDiff(Table, power):
    """
        Построение таблицы разделенных разностей.
        Параметры выбираются из таблицы Table,
        степень полинома power.
    """

    CountDerivs = (power + 1) // 2
    CountValues = power + 1 - CountDerivs

    SplitDiff = []
    diffs = []

    for i in range(CountValues):
        diffs.append(Table[i][1])
    
    SplitDiff.append(diffs)
    diffs = []

    j = 0
    for i in range(power):
        if i % 2 == 0:
            diffs.append(Table[j][2])
            j += 1
        else:
            DiffX = Table[j - 1][0] - Table[j][0]
            DiffY = SplitDiff[0][j - 1] - SplitDiff[0][j]
            diffs.append(DiffY/DiffX)
    SplitDiff.append(diffs)

    for i in range(power - 1):
        size = len(SplitDiff)
        diffs = []

        DiffX = Table[0][0] - Table[i // 2 + 1][0]

        for j in range(1, len(SplitDiff[size - 1])):
            DiffY = SplitDiff[size - 1][j - 1] - SplitDiff[size - 1][j]
            diffs.append(DiffY/DiffX)
    
        SplitDiff.append(diffs)
    
    return SplitDiff


def HermitPolynomial(Config, power, argument, SplitDiff):
    """
        Получение значения интерполяционного полинома
        Эрмита степени power при аргументе argument.
        Начальная конфигурация Config, таблица разде-
        ленных разностей SplitDiff. 
    """

    result = SplitDiff[0][0]
    factor = 1

    j = 0
    for i in range(power):
        if i % 2 == 0:
            factor *= argument - Config[j][0]
        else:
            factor *= argument - Config[j][0]
            j += 1
        
        result += SplitDiff[i + 1][0] * factor
    
    return result


def HermitInterpolation(Table, SizeTable, power, argument):
    """
        Значение интерполяцинного полинома Эрмита
        при заданной степени power и аргументе argument.
        Параметры выбираются из таблицы Table размером
        SizeTable.
    """

    Table = SortTable(Table, SizeTable)
    Config = CreateConfig(Table, SizeTable, power, argument)
    SplitDiff = CreateSplitDiff(Config, power)
    result = HermitPolynomial(Config, power, argument, SplitDiff)

    return result


Table = [[0.00, 1.000000, -1.000000],
         [0.15, 0.838771, -1.14944],
         [0.30, 0.655336, -1.29552],
         [0.45, 0.450447, -1.43497],
         [0.60, 0.225336, -1.56464],
         [0.75, -0.018310, -1.68164],
         [0.90, -0.278390, -1.78333],
         [1.05, -0.552430, -1.86742]]
SizeTable = 8
power = 4
argument = 0.525
