from src import operations


def calculate():
    num1 = float(input("Ingrese el primer numero: "))
    num2 = float(input("Ingrese el segundo numero: "))

    print("Suma: ", operations.addition(num1, num2))
    print("Resta: ", operations.substraction(num1, num2))
    print("Division: ", operations.divide(num1, num2))
    print("Multiplicacion: ", operations.multiplicacion(num1, num2))
