from functools import wraps

def starwrapper(func):
    @wraps(func)
    def wrapper(args):
        return func(*args)
    return wrapper

@starwrapper
def foo(name, age, salary):
    print(f"{name}, {age}, {salary}")

foo(('Ram',18,100000000))
