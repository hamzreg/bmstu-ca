COUPLE = 2


def SortTable(Table, SizeTable):
    """
        Сортировка таблицы по возрастанию.
    """

    for i in range(SizeTable - 1):
        MinIndex = i
        for j in range(i + 1, SizeTable):
            if Table[j][0] < Table[MinIndex][0]:
                MinIndex = j
        
        Table[MinIndex], Table[i] = Table[i], Table[MinIndex]
    
    return Table


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

    if center == 0:
        return Table[:power + 1]
    
    if center == SizeTable:
        return Table[SizeTable - power - 1:]

    if abs(Table[center][0] - argument) > abs(argument - Table[center - 1][0]):
        center -= 1

    low = center - power // 2 - 1
    top = center + power // 2 + 1

    if power % 2 == 0:
        return Table[center - power // 2:top]

    if abs(Table[top][0] - argument) > abs(argument - Table[low][0]):
        return Table[low:top]
    
    return Table[low: top + 1]


def CreateSplitDiff(Table, power):
    """
        Построение таблицы разделенных разностей.
        Параметры выбираются из таблицы Table,
        степень полинома power.
    """

    SplitDiff = []
    diffs = []

    for i in range(power + 1):
        diffs.append(Table[i][1])
    
    SplitDiff.append(diffs)

    for i in range(power):
        size = len(SplitDiff)
        diffs = []
        DiffX = Table[0][0] - Table[i + 1][0]

        for j in range(1, len(SplitDiff[size - 1])):
            DiffY = SplitDiff[size - 1][j - 1] - SplitDiff[size - 1][j]
            diffs.append(DiffY/DiffX)

        SplitDiff.append(diffs)
    
    return SplitDiff


def NewtonPolynomial(Config, power, argument, SplitDiff):
    """
        Получение значения интерполяционного полинома
        Ньютона степени power при аргументе argument.
        Начальная конфигурация Config, таблица разде-
        ленных разностей SplitDiff. 
    """

    result = SplitDiff[0][0]
    factor = 1

    for i in range(power):
        factor *= argument - Config[i][0]
        result += SplitDiff[i + 1][0] * factor

    return result


def NewtonInterpolation(Table, SizeTable, power, argument):
    """
        Значение интерполяцинного полинома Ньютона
        при заданной степени power и аргументе argument.
        Параметры выбираются из таблицы Table размером
        SizeTable.
    """

    Table = SortTable(Table, SizeTable)
    Config = CreateConfig(Table, SizeTable, power, argument)
    SplitDiff = CreateSplitDiff(Config, power)
    result = NewtonPolynomial(Config, power, argument, SplitDiff)

    return result


def TwoNewtonIntrepolation(StartTable, X, Y, PowerX, PowerY,
ArgumentX, ArgumentY):
    """
       Интерполяция функции двух переменных.
       X, Y - значения координат x и y соответственно.
       StartTable - таблица со значениями z(x,y).
       PowerX, PowerY - степени по координатам x и y 
       соответственно.
       ArgumentX, ArgumentY - значения аргументов x и y 
       соотвественно.
    """

    TableY = []

    for i in range(len(Y)):
        column = []
        column.append(Y[i])
        TableY.append(column)

    for i in range(len(StartTable)):
        Table = []

        for j in range(len(StartTable[i])):
            row = []
            row.append(X[j])
            row.append(StartTable[i][j])
            Table.append(row)
        
        ResultX = NewtonInterpolation(Table, len(Table), PowerX, ArgumentX)
        TableY[i].append(ResultX)
        print(TableY)
    
    result = NewtonInterpolation(TableY, len(TableY), PowerY, ArgumentY)

    print(PowerX, PowerY, result)
    return result


StartTable = [[0, 1, 4, 9, 16],
              [1, 2, 5, 10, 17],
              [4, 5, 8, 13, 20],
              [9, 10, 13, 18, 25],
              [16, 17, 20, 25, 32]]

X = [0, 1, 2, 3, 4]
Y = [0, 1, 2, 3, 4]

Table = [[0.00, 1.000000],
         [0.15, 0.838771],
         [0.30, 0.655336],
         [0.45, 0.450447],
         [0.60, 0.225336],
         [0.75, -0.018310],
         [0.90, -0.278390],
         [1.05, -0.552430]]
SizeTable = 8
power = 4
argument = 0.525

TwoNewtonIntrepolation(StartTable, X, Y, 0, 0, 1.5, 1.5)