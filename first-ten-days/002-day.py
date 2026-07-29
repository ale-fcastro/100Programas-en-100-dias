class ViewHelper:
    def __init__(self, active_option, sub_menu_select):
        self.active_option = active_option
        self.sub_menu_select = sub_menu_select

    def show_menu(self):
        print("""
            ====================================
                    CONVERSOR DE UNIDADES
            ====================================

            1. Grados
            2. Distancias
            3. Pesos

            0. Salir

            ====================================
        """)

    def show_grados(self):
        print("\n \n")
        print("""
            ------ GRADOS ------

            1. Fahrenheit -> Celsius
            2. Celsius -> Fahrenheit

            0. Volver
        """)
        print("\n \n")

    def show_distancias(self):
        print("\n \n")
        print("""
            ------ DISTANCIAS ------

            1. Kilómetros -> Millas
            2. Millas -> Kilómetros

            0. Volver
        """)
        print("\n \n")

    def show_pesos(self):
        print("\n \n")
        print("""
            ------ PESOS ------

            1. Kilogramos -> Libras
            2. Libras -> Kilogramos

            0. Volver
        """)
        print("\n \n")

    def opcion_switcher(self):
        match self.active_option:
            case 1:
              self.show_grados()
            case 2:
              self.show_distancias()
            case 3:
              self.show_pesos()

    def print_result_depend(self, entrada, result):
        match self.active_option:
            case 1:
                if self.sub_menu_select == 1:
                    print(f"\n{entrada:.2f} °F = {result:.2f} °C")
                else:
                    print(f"\n{entrada:.2f} °C = {result:.2f} °F")

            case 2:
                if self.sub_menu_select == 1:
                    print(f"\n{entrada:.2f} Km = {result:.2f} Millas")
                else:
                    print(f"\n{entrada:.2f} Millas = {result:.2f} Km")

            case 3:
                if self.sub_menu_select == 1:
                    print(f"\n{entrada:.2f} Kg = {result:.2f} Libras")
                else:
                    print(f"\n{entrada:.2f} Libras = {result:.2f} Kg")

class HelperConversor:
    def __init__(self, salida):
        self.salida = salida

    def formula_helper(self, value, helper, invert):
        return value * helper if invert == True else value / helper


    def calcular_grados(self, inputvalue, invert):
        help_primario = 32.0
        help_secundario = 1.8
        self.salida = (inputvalue - help_primario) / help_secundario if invert == True else (inputvalue * help_secundario) + help_primario

    def calcular_distancias_y_pesos(self, inputvalue, invert, is_distance):
        help_shared_convercion = 1.60934 if is_distance == True else 2.20462
        self.salida = self.formula_helper(inputvalue, help_shared_convercion, invert)
    
    def opcion_final_procedure_execute(self, value, sub_opcion_select, is_distance, procceso):
        match procceso:
            case 1:
                self.calcular_grados(value, sub_opcion_select)
            case 2 | 3:
                self.calcular_distancias_y_pesos(value, sub_opcion_select, is_distance)

print("----- BIENVENIDO A MI CONVERSOR DE UNIDADES SUPER BKN -----")

init_bucle = False
helper_conversor = HelperConversor(0)
view = ViewHelper(0, 0)
inputvalue = 0.0
while not init_bucle:

    #  mostrar el menu en caso de ser primera vez o no estar en una opcion <--> o viseversa 
    if view.active_option == 0:
        view.show_menu()
        view.active_option = int(input("Enter: "))
        if view.active_option == 0:
            exit()
        continue
    else:
        view.opcion_switcher()
        view.sub_menu_select = int(input("Enter: "))
        if view.sub_menu_select == 0:
            view.active_option = 0
            continue
    print("\n")

    inputvalue = float(input("Ingresa el valor a convertir: "))

    # variables computadas o como le llamo yo lo que el usuario no ve
    invert_conputado = True if view.sub_menu_select == 1 else False
    is_distance = True if view.active_option == 2 else False

    helper_conversor.opcion_final_procedure_execute(inputvalue, invert_conputado, is_distance, view.active_option);

    view.print_result_depend(inputvalue, helper_conversor.salida)



# GRADOS
# calculo F to C ( (F - 32) / 1.8  ) treu 
# claculo C to F ( ( C * 1.8 ) + 32 ) false

# DISTANCIAS
# calculo K to M ( K / 1.60934 ) true
# calculo M to K ( M * 1.60934 ) false

# PESOS
# calculo K to L ( K * 2.20462 ) true
# calculo L to K ( L / 2.20462 ) false