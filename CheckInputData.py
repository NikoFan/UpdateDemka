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


def check_org_name(partner_name: str):
    if len(partner_name) != 0:
        return True
    print(1)
    return False


def check_dir_name(dir_name: str):
    if len(dir_name.split(" ")) == 3:
        return True
    print(12)
    return False


def check_rate(rate: int):
    try:
        if rate in range(1, 11):
            return True
        print(13)
        return False
    except Exception:
        print(133)
        return False


def check_phone(phone_number: str):
    if (len(phone_number) == 13 and
            phone_number[0] in ['9', '8', '4']):
        return True
    print(15)
    return False


def check_mail(mail_address: str):
    if (len(mail_address.split("@")) == 2 and
            len(mail_address.split("@")[-1].split(".")) == 2):
        return True
    print(14)
    return False


def check_inn(inn: str):
    if inn.isdigit() and len(inn) == 10:
        return True
    print(16)
    return False


def check_ur_addr(ur_addr: str):
    if (len(ur_addr.split(",")) > 2 and
            len(ur_addr.split(",")[0]) == 6 and
            ur_addr.split(",")[0].isdigit()):
        return True
    print(17)
    return False
