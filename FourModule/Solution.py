"""
'...С целью обеспечить одинаковый расчет количества материала,
требуемого для производства продукции, необходимо разработать метод...'

* Следуя из задания - от нас не требуется разработать окно / фрейм. Просто функция, которая должна выполнять действие
"""

"""
'...Метод должен принимать идентификатор типа продукции,
идентификатор типа материала, количество получаемой продукции – целые
числа, параметры продукции (два параметра) – вещественные, положительные
числа, а возвращать целое число – количество необходимого материала с
учетом возможного брака материала....'

*Как следует из ответа от Организаторов:
'
Добрый день! 

Параметры продукции (два параметра) - длина и ширина или ширина и высота, например, или любые два вещественных
положительных числа. Всего пять аргументов функции (метода) расчета количества материала: идентификатор типа продукции,
идентификатор типа материала, количество получаемой продукции, параметр продукции1, параметр продукции2.
'
=> Параметры продукции - W H
Идентификатор типа продукции - Product_type_id
Идентификатор типа материала - Material_type_id
Количество получаемой продукции - Result_count_of_products

- 5 параметров
"""

material_id_dict = dict()
product_id_dict = dict()

from DATABASE.Database import Database

def function(product_type_id, material_type_id, result_count, w:int, h:int):
    """
    Представим что делаем квадратные доски
    :param product_type_id: Идентификатор типа продукции
    :param material_type_id: Идентификатор типа материала
    :param result_count: Количество получаемой продукции
    :param w: Ширина
    :param h: высота
    :return: целое число – количество необходимого материала с
учетом возможного брака материала
    """

    try:
        # если идет установка, что должен учитываться Брак - Данные про материал и Продукцию берутся из БД
        # НО - тип материала не привязан к типу продукции -> Мы их связываем тут

        # Использование глобального словаря

        break_material = material_id_dict[material_type_id]
        coefficient_product = product_id_dict[product_type_id]
        if result_count <= 0:
            return -1
        elif w <= 0:
            return -1
        elif h <= 0:
            return -1
    except Exception:
        return -1



    print(type(break_material), type(coefficient_product))
    print(break_material, coefficient_product)


    """
    Количество необходимого материала на одну единицу продукции рассчитывается как
    произведение параметров продукции,
    умноженное на коэффициент типа продукции. 
    Кроме того, нужно учитывать процент брака материала в зависимости от его типа: с учетом возможного
    брака материала необходимое количество материала должно быть увеличено.
    Коэффициент типа продукции и процент брака – вещественные числа.
    """

    # Произведение параметров продукции
    params_mult = w * h

    # Количество необходимого материала
    need_material_count = params_mult * coefficient_product

    # Расчет % брака и его приколов
    """
    На примере Материала 1 - брак = 0.1%
    => из 100 продукции - 10 брак
    => На 100 продукции нужно (условно) 1000 материала
    => 100 материала уйдут на брак. Надо этот материал прибавить к уже готовому, чтобы выйти в 0 (Выполнить план и + брак)
    """
    # Получение бракованного материала для восполнения
    break_count = need_material_count * break_material

    # Увеличение материала, чтобы убрать брак
    need_material_count += break_count

    """
    => need_material_count -> Количество материала для Единицы продукции
    """

    # все количество материала для всей продукции
    all_materials_count =need_material_count * result_count
    return all_materials_count



def get_all_materials_id(connect):
    query = """
    select *
    from material_type_import
    """

    cursor = connect.cursor()
    cursor.execute(query)

    materials = []
    for el in cursor.fetchall():

        materials.append([el[0].strip(), el[1].strip()])

    return materials

def get_all_products_id(connect):
    query = """
    select *
    from product_type_import
    """

    cursor = connect.cursor()
    cursor.execute(query)

    products = []
    for el in cursor.fetchall():
        products.append([el[0].strip(), str(el[1])])

    return products


def main():
    connection_string = Database().connection_uri
    # Получение данных из БД
    products = get_all_products_id(connection_string)
    materials = get_all_materials_id(connection_string)

    # Ввод данных от пользователя

    p = []  # Массив для хранения материалов без брака
    for el in products:
        print("ID: '" + "'Коэффициент продукции: ".join(el))
        p.append(el[0])
        product_id_dict[el[0]] = float(el[1])
    print("Введите требуемый id продукции:")
    p_id = input("~: ")


    m = [] # Массив для хранения материалов без брака
    for el in materials:
        print("ID: '"+"' %Брака: ".join(el))
        m.append(el[0])
        material_id_dict[el[0]] = float(el[1][:-1])
    print("Введите требуемый id материала:")
    m_id = input("~: ")


    print("Введите требуемое количество продукции")
    try:
        count = int(input("~: "))
    except Exception:
        count = -1
        print("Проверьте ввод!")


    print("Введите требуемое Ширину и Высоту продукции")
    try:
        w = int(input("Ширина: "))
        h = int(input("Высота: "))
    except Exception:
        w, h = -1, -1
        print("Проверьте ввод!")

    # Вызов функции
    print(function(p_id, m_id, count, w, h))



main()
