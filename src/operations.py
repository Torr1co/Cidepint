def multiplicacion(multiplicando,multiplicador):
    try:
        mul = multiplicando * multiplicador
        return mul
    except TypeError:
        print("Los argumentos ingresados deben ser numeros")