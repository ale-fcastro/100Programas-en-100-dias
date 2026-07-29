# Día 3 - Calculadora de IMC
# Entrada:
# peso: float
# altura: float

# Salida:
# IMC - CALCULO: Peso en kilogramo / altura ^ 2 - variable_computada_float 
# clasificación : Variable Texto computada mediante resultado de calculo computado:
    # opciones
    # 1. Bajo peso: IMC menor a 18.5
    # 2. Peso normal: IMC entre 18.5 y 24.9
    # 3. Sobrepeso: IMC entre 25.0 y 29.9 (Preobesidad)
    # 4. Obesidad: IMC de 30.0 o más
#

# PROGRAMARE COMO SI HABLARA CONTIGO PARA QUE ENTIENDAS MI CAMINO MENTAL
# primero definire persona por que por que ahi peso y altura , y por que el imc es de el puede haber nombre edad etc si scala
class Persona:
    def __init__(self, peso, altura, imc):
        self.peso = peso
        self.altura = altura
        self.imc = imc
    
    def validar_altura_no_sea_cero(self):
        return False if self.altura == 0.0 else True
        

    # no es nesesario mas que esto pero agregare esto por que si java moment y enserio es por que si
    def show_person_information(self, clasificacion):
        print("\n Eres una persona con: ", self.peso, " kg y ", self.altura, " de Altura por lo que tu imc es de ", self.imc, " Esto significa que se encuentra en clasificacion un: " ,clasificacion, "\n")


# luego pienso la persona no clacula aunque si puede hacerlo,
# por eso decimos la heramienta tiene un resultado y la persona un imc mismo dato si pero propositos diferentes 
# es la heramienta la que lo hace imagino que entra a alguna app que lo aga por el asi que tenemso un:
class IMCCalculatorHelper:
    def __init__(self, result, clasificacion):
        self.result = result
        self.clasificacion = clasificacion
    
    def calculate_imc(self, ps, al):
        self.result = ps / (al ** 2)
        self.computar_de_clasificacion()

    def computar_de_clasificacion(self):
        match self.result:
            case self.result if 18.5 >= self.result:
                self.clasificacion = "BAJO PESO"
            case self.result if 18.5 >= self.result <= 24.9:
                self.clasificacion = "PESO NORMAL"
            case self.result if 25.0 >= self.result <= 29.9:
                self.clasificacion = "SOBREPESO"
            case self.result if 30.0 >= self.result:
                self.clasificacion = "OBESIDAD"

print("----- BIENVENIDO A SUPER CALCULADORA DE PESO PARA TI ----- \n")

init_bucle = False
helper = IMCCalculatorHelper(0, "ninguna")
person = Persona(0, 0, 0)

while not init_bucle:
    # primero entrada
    print("Ingresa los datos requeridos para su solicitud de calculo: \n")
    person.peso = float(input("- Peso en kg: "))
    person.altura = float(input("\n- Altura en metro: "))
    if not person.validar_altura_no_sea_cero():
        print("No se puede dividir por cero. retry..... \n")
        continue 

    # calculo
    helper.calculate_imc(person.peso, person.altura)

    # actulizar imc de la persona
    person.imc = helper.result

    # muestro la info
    person.show_person_information(helper.clasificacion)

    init_bucle = False if input("si decea hacer otro calculo escriba 'si' en caso de que no precione 'enter' \n") == "si" else True






# CERIFICADO POR FCASTRO