from NewtonInterpolation import NewtonInterpolation

CHANGE = True
NOT_CHANGE = False


def ChangeColumns(Table, SizeTable):
    """
        Смена местами значений x и y таблицы Table
        размера SizeTable.
    """

    for i in range(SizeTable):
        Table[i][0], Table[i][1] = Table[i][1], Table[i][0]
    
    return Table


def SignsChange(Table, SizeTable):
    """
        Проверка функции на смену знака.
    """

    Positives, Negatives, Zeros = 0, 0, 0

    for i in range(SizeTable):
        if Positives and Negatives or Zeros:
            return CHANGE

        if Table[i][1] < 0:
            Negatives = 1
        elif Table[i][1] > 0:
            Positives = 1
        else:
            Zeros = 1
    
    return NOT_CHANGE


def SearchRoot(Table, SizeTable, power, root):
    """
        Поиск корня заданной табличной функции
        с помощью обратной интерполяции, используя
        полином Ньютона.
    """

    if not SignsChange(Table, SizeTable):
        print("\nFunction has no root\n")
        return

    Table = ChangeColumns(Table, SizeTable)
    result = NewtonInterpolation(Table, SizeTable, power, root)

    return result
