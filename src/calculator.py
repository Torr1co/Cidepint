def divide (a,b):
    if b!=0:
        return a/b
    else:
        return "Error! Division by zero is not possible."

def add(a,b):
    try:
        return (a+b)
    except TypeError:
        print("Los argumentos ingresados deben ser numeros")

    