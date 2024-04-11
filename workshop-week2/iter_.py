
a = [1,2,3]
a = iter(a)
print(next(a))
print(next(a))
print(next(a))
print(next(a))


class MyIter:


    def __iter__(self):
        return self

    def __next__(self):
        pass
