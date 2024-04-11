def add_to(num, target=None):
    if target is None:
        target = []
    target.append(num)
    return target


print(add_to(10))
print(add_to(10))
print(add_to(10))
new_list = []
print(add_to(1, target=new_list))
print(new_list)
print(add_to(10))

