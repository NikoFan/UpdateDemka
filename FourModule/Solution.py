# инициализация и объявление пустых словарей
material_id_dict = dict()
product_id_dict = dict()

# импорт класса базы данных
from DATABASE.Database import Database

# метод рассчета количества материала для производства продукции с учетом предоставленных данных
# product_type_id - ID типа продукции, material_type_id - ID типа материала, result_count - кол во продукции,
# w - ширина h - высота
def function(product_type_id, material_type_id, result_count, w:int, h:int):
    try:
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
    # произведение параметров продукции
    params_mult = w * h

    # количество необходимого материала
    need_material_count = params_mult * coefficient_product

    # получение бракованного материала для восполнения
    break_count = need_material_count * break_material

    # увеличение материала, чтобы убрать брак
    need_material_count += break_count

    # все количество материала для всей продукции
    all_materials_count =need_material_count * result_count
    return all_materials_count

# функция поиска материала по ID
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

# функция поиска продукции по ID
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

# основная функция
def main():
    connection_string = Database().connection_uri
    # получение данных из БД
    products = get_all_products_id(connection_string)
    materials = get_all_materials_id(connection_string)

    # массив для хранения материалов без брака
    p = []
    for el in products:
        print("ID: '" + "'Коэффициент продукции: ".join(el))
        p.append(el[0])
        product_id_dict[el[0]] = float(el[1])
    print("Введите требуемый id продукции:")
    p_id = input("~: ")

    # массив для хранения материалов без брака
    m = []
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

    # вызов функции
    print(function(p_id, m_id, count, w, h))
main()
