import unittest


def calculate_discount(count: int):
    """
    Функция для расчета скидки по заданию
    :param count: Число продаж
    :return: Число скидки
    """
    # Проверка по зданию
    if count == None:
        return 0
    elif count > 300_000:
        return 15
    elif count > 50_000:
        return 10
    elif count > 10000:
        return 5
    return 0


class TestDiscount(unittest.TestCase):
    def test_one(self):
        self.assertEqual(calculate_discount(10020), 5)

    def test_two(self):
        self.assertEqual(calculate_discount(0), 0)

    def test_three(self):
        self.assertEqual(calculate_discount(50001), 10)

    def test_four(self):
        self.assertEqual(calculate_discount(300020), 15)

    def test_five(self):
        self.assertEqual(calculate_discount(10), 0)


TestDiscount()
