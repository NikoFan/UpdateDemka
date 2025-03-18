def start_check(partners_input_data: dict):
    """
    Функция вызова проверок для данных
    :param partners_input_data: Словарь с данными, которые будут проверяться
    :return: Результат проверки True / False
    """
    if (
            check_inn(partners_input_data['inn']) and
            check_mail(partners_input_data['mail']) and
            check_rate(int(partners_input_data['rate'])) and
            check_phone(partners_input_data['phone']) and
            check_org_name(partners_input_data['name']) and
            check_dir_name(partners_input_data['dir']) and
            check_ur_addr(partners_input_data['addr'])
    ):
        return True
    return False

def check_inn(inn):
    try:
        if (
                int(inn) > 0 and
            len(str(inn)) == 10
        ):
            return True
        print("inn")
        return False
    except Exception:
        return False

def check_mail(mail):
    # nr@mail.ru
    # -> ["n", "mail.ru"]
    # -> ["n", "mail.ru"] -> ["mail", "ru"]
    # -> ["nr@mail", "ru"]
    if (
        len(mail.split("@")) == 2 and
        len(mail.split("@")[1].split(".")) == 2
    ):
        return True
    print("mail")
    return False

def check_rate(rate):
    try:
        if int(rate) in range(1, 11):
            return True
        print("rate")
        return False
    except Exception:
        return False

def check_phone(phone):
    # 999 999 99 99
    if (
        len(phone.split(" ")) == 4 and
        phone[0] in ["9", "8", "4"]
    ):
        return True
    print("phone")
    return False

def check_org_name(name):
    if len(name) != 0:
        return True
    return False

def check_dir_name(name):
    if len(name.split(" ")) == 3:
        return True
    return False

def check_ur_addr(addr):
    # 123123, Moscrdf -> ["123123", "MOcrdf"]
    if (
        len(addr.split(", ")) >= 2 and
        addr.split(", ")[0].isdigit()
    ):
        return True
    print("addr")
    return False