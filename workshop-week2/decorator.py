from functools import wraps


def check_not_none(func):
    @wraps(func)
    def wrapper(*args):
        """docs for wrapper"""
        result = func(*args) if args else 'is None!'
        return result
    return wrapper


@check_not_none
def square(x):
    """Документация для функции square"""
    return x ** 2

print(square.__name__)
print(square.__doc__)

# new_square = check_not_none(square)
#
# print(new_square())

print(square(10))
