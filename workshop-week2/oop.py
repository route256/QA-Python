class Phone:
    username = "Evgeny"
    __how_many_calls_missed = 0

    def call(self):
        print(f"Hi, {self.username}")

    def _missed_calls(self):
        self.__how_many_calls_missed += 1
        print(f"Missed calls: {self.__how_many_calls_missed}")


my_phone = Phone()
print(my_phone.username)
my_phone.call()
my_phone.call()
my_phone._missed_calls()
my_phone._missed_calls()
# print(my_phone.__how_many_calls_missed)
print(my_phone._Phone__how_many_calls_missed)


class Product:
    def __init__(self, price):
        self.price = price

    def __str__(this):
        return "Это информация о продукте"

    def __add__(this, other):
        return this.price + other.price


product = Product(100)
iphone = Product(100_000)


print(product)
print(product + iphone)
print(product.price + iphone.price)

