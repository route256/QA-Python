from functools import wraps

PERMISSION_ROLES = ['admin', 'user']


def check_role(role):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if role in PERMISSION_ROLES:
                result = func(*args, **kwargs)
                return result
            else:
                return 'Access denied'
        return wrapper
    return inner


@check_role('user')
def login():
    return 'Добро пожаловать'


@check_role('guest')
def send_money(sender, total_money):
    return 'Деньги переведены!'


print(send_money("Vasya", 100))
