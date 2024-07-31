def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error! Division by zero is not possible."


def substraction(a, b):
    return a - b


def addition(a, b):
    try:
        return a + b
    except TypeError:
        print("Los argumentos ingresados deben ser numeros")


def multiplicacion(multiplicando, multiplicador):
    try:
        mul = multiplicando * multiplicador
        return mul
    except TypeError:
        print("Los argumentos ingresados deben ser numeros")
