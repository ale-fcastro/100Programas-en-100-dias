class HelperCalculator:
    def __init__(self, result):
        self.result = result

    def validar_signo(self, signo):
        lista_de_signos_validos = ("+","*","-","/","^","%")
        return signo in lista_de_signos_validos

    def suma(self, a, b):
        self.result = a + b

    def mult(self, a, b):
        self.result = a * b
    
    def resta(self, a, b):
        self.result = a - b
    
    def divicion(self, a, b):
        self.result = a / b

    def potencia(self, a, b):
        self.result = a ** b
    
    def residuo(self, a, b):
        self.result = a % b

    def update_result(self, operador, a, b):
        match operador:
            case "+":
              self.suma(a, b) 
            case "*":
              self.mult(a, b) 
            case "-":
              self.resta(a, b) 
            case "/":
              self.divicion(a, b) 
            case "^":
              self.potencia(a, b) 
            case "%":
              self.residuo(a, b)


print("------ CALCULADORA BASICA ------ \n")

# definir variables de scope
mycalculatorhelper = HelperCalculator(0)
ApagarPrograma = False

# inicializar el programa por decirlo de alguna manera
while not ApagarPrograma :
    # solicitar el operador
    operador = input("Indique la Operacion entre: +, *, -, /, ^, %: ")

    # validar operador antes de continuar en caso de no proseguir continuar con otra operacion
    if not mycalculatorhelper.validar_signo(operador):
        print("Operacion invalida \n")
        continue
    
    # solicitar numeros para el procedimiento
    num1 = float(input("Introduce el primer_numero: "))
    num2 = float(input("Introduce el segundo_numero: "))

    # evitar imposivilidad de divicion entre 0
    if num2 == 0 and operador == "/":
        print("NO puedes dividir entre 0, pendejo! \n \n")
        print("Te Dejo Reintentarlo pero bro sea serio \n")
        continue

    # actulizar el valor de la clase en el helper
    mycalculatorhelper.update_result(operador, num1, num2)
    
    # imprimir resultado
    print("Resultado:", mycalculatorhelper.result)

    # preguntar si continuar
    ApagarPrograma = input("Si Desea continuar ingrese 'si' en caso de que no ingrese 'no' ") == "no"
    print("\n \nSiguiente Calculo \n")

