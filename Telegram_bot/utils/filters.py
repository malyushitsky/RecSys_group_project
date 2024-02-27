import re


BAD_CHARS = list(map(str, range(10))) + [",", ".", " ", "-", ";"]


def check_query(text, n_min=10, n_max=100):
    # беда, если много
    bad_chars_num = len([i for i in text if i in BAD_CHARS])
    # регулярка - только цифры, буквы, пробел и ,.-
    if not bool(re.match(r"^(?![-.]+$)[\w\s.,-;]+$", text)):
        return False
    # подряд более 3 одинаковых символов
    if bool(re.search(r"(.)\1{3,}", text)):
        return False
    # строка состоит только из цифр и ,.- или их больше, чем букв
    if bad_chars_num == len(text) or bad_chars_num >= len(text) - bad_chars_num:
        return False
    # длина
    if len(text) < n_min or len(text) > n_max:
        return False
    return True
