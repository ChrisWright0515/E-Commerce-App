import base64
import hashlib
import random
import string


class Product():
    def __init__(self, color, size, price, quantity):
        self.color = color
        self.size = size
        self.price = price
        self.quantity = quantity


def generate_random_string(length):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def hashing(password):
    return hashlib.sha3_256(password.encode())


def check_email(email):
    if '@' in email:
        good = True
        return good
    else:
        good = False
        return good


def check_pass(password):
    char = '[@_!#$%^&*()<>?/\|}{~:]'
    spec_char = list(char)
    special = False
    upper = False
    lower = False
    num = False
    for letter in password:
        if letter.isupper():
            upper = True
        elif letter in spec_char:
            special = True
        elif letter.islower():
            lower = True
        elif letter.isdigit():
            num = True
    if len(password) >= 8:
        if special:
            if upper:
                if lower:
                    if num:
                        return 'Good'
                    else:
                        return 'Num'
                else:
                    return 'Lower'
            else:
                return 'Upper'
        else:
            return 'Special'
    else:
        return 'Length'


def format_account_cookies(row):
    all_accounts = []
    for account in row:
        each_acc = []
        for i in range(len(account)):
            each_acc.append(account[i])
        all_accounts.append(each_acc)
    return all_accounts


def phone_format(n):
    if (len(n)) == 10:
        new_phone = f'({n[0:3]}) {n[3:6]}-{n[6:]}'
        return new_phone
    else:
        return n


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


def one_list_row(row):
    l = []
    for item in row:
        for i in range(len(item)):
            l.append(item[i])
    return l


def list_row(row):
    l = []
    for item in row:
        inner_l = []
        for i in range(len(item)):
            inner_l.append(item[i])
        l.append(inner_l)
    return l


def put_in_list(row, index):
    li = []
    for item in row:
        li.append(item[index])
    return li


def json_product(row):
    all_colors = []
    all_sizes = []
    all_prices = []
    all_quant = []
    for product in row:
        all_colors.append(product[2])
        all_sizes.append(product[3])
        all_prices.append(product[4])
        all_quant.append(product[5])
    p = Product(all_colors.copy(), all_sizes.copy(), all_prices.copy(), all_quant.copy())
    configs = {'product': p.__dict__}
    return configs


def check_cart_qty(row):
    for item in row:
        if item[0] > item[1]:
            return False
    return True
