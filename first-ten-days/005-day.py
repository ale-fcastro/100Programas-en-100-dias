# **Día 5 — Gestor de tareas en consola (CRUD in-memory)**  
# Clase `Tarea` (id, texto, completada) + `TareaManager` con add/complete/delete/list. Fuerza a pensar en listas de objetos y búsqueda por id, no solo por índice.

# Task, Status, TaskManager, ConsoleUI
# IntEnum

from enum import IntEnum

class ValidatorEntryHelper:
    def __init__(self):
        pass

    def validate_entry(self, entry, type: any):
        return True if isinstance(entry, type) else False

    def validate_multi_entry(self, entries, types: list[any], valores_a_validar: list[str]): # certificado por fcastro, ame esto encerio estoy orgulloso waos
        result: list[bool] = []
        list_value_errors: list[str] = []
        for i, entry in enumerate(entries):
            if isinstance(entry, types[i]):
                result.append(True)
                # valores_a_validar.pop(i) # esto me jugo una mala pasada en el test no pense en que al eliminar el primero el segundo queda fuera de rango por que es truecambiare la metodologia
            else:
                result.append(False)
                list_value_errors.append(valores_a_validar[i])
        
        return [result, list_value_errors]

class Task:
    def __init__(self, Id: int, Titulo: str, Description: str):
        self.Id = Id
        self.Titulo = Titulo
        self.Status = Status.CREATED
        self.Description = Description

class Status(IntEnum):
    CREATED = 1
    EN_PROCESO = 2
    COMPLETADA = 3
    CANCELADA = 4
    DELETE = 0

class TaskManager:
    def __init__(self):
        self.Tasks: list[Task] = []
        self.validator_helper: ValidatorEntryHelper = ValidatorEntryHelper()

    def Create(self, Titulo: str, Descripcion: str):
        validation_result = self.validator_helper.validate_multi_entry(
            [Titulo, Descripcion], 
            [str, str],
            ["Titulo", "Descripcion"]
        )

        # si algo paso no continuo el processo
        if False in validation_result[0]:
            return validation_result

        new_task = Task(len(self.Tasks), Titulo, Descripcion)
        self.Tasks.append(new_task)

        return validation_result

    def Update(self,Id: int, Titulo: str, Descripcion: str):
        validation_result = self.validator_helper.validate_multi_entry(
            [Id, Titulo, Descripcion], 
            [int, str, str], 
            ["Id", "Titulo", 'Descripcion']
        )

        if False in validation_result[0]:
            return validation_result

        task = self.FindByid(Id)

        task.Titulo = Titulo
        task.Description = Descripcion

        return validation_result
    
    def Delete(self, Id: int):
        # capturamos el error en caso de existir
        result = self.validator_helper.validate_entry(Id, int)

        # cortamos procceso en caso de falla 
        if not result:
            return [result, "Tipo de dato en id invalido"]
        
        tarea_a_eliminar = self.FindByid(Id)

        # validamos que la tarea realmente sea una tarea es casi imposible pero uno nunca sabe (reutilizamos result)
        result = self.validator_helper.validate_entry(tarea_a_eliminar, Task)

        if not result:
            return [result, "Error Encontrando Tarea valida"]

        self.update_status(Status.DELETE, tarea_a_eliminar)
        return [result,  "Listo"]
            
    def CompletarTarea(self, Id: int):
        # capturamos el error en caso de existir
        result = self.validator_helper.validate_entry(Id, int)

        # cortamos procceso en caso de falla 
        if not result:
            return [result, "Tipo de dato en id invalido"]
        
        tarea_a_completar = self.FindByid(Id)

        # validamos que la tarea realmente sea una tarea es casi imposible pero uno nunca sabe (reutilizamos result)
        result = self.validator_helper.validate_entry(tarea_a_completar, Task)

        if not result:
            return [result, "Error Encontrando Tarea valida"]

        self.update_status(Status.COMPLETADA, tarea_a_completar)
        return [result,  "Listo"]

    def FindByid(self, Id: int):
        for t in self.Tasks:
            if t.Id == Id:
                return t
            else:
                return "Task no encontrado"

    def ListAll(self):
        return [n for n in self.Tasks if n.Status != Status.DELETE]

    def List_By_Status(self, Status: Status):
        return [n for n in self.Tasks if n.Status == Status]
    # internal herper metod
    def update_status(self, new_status: Status, task: Task):
        task.Status = new_status

class ConsoleUI:
    def __init__(self):
        self.task_manager: TaskManager = TaskManager()
        self.primary_menu_select: int = 0

    def status_to_string(self, status: Status):
        opciones = {
            Status.CREATED: "Creada",
            Status.EN_PROCESO: "En Proceso",
            Status.COMPLETADA: "Completada",
            Status.DELETE: "Eliminada"
        }

        return opciones[status]

    def preguntar_si_continuar_en_el_procedimiento(self):
        opt = input("si desea volver al menu principal indique 'si' en caso de que no precione enter: ")
        if opt == "si":
            self.primary_menu_select = 0

    def solicitar_datos(self):
        print("\nIngrese los datos de la tarea")

        titulo = input("Titulo: ")
        descrition = input("Description: ")

        return [titulo, descrition]

    def crear_tarea(self):
        self.primary_menu_select = 1
        result = self.solicitar_datos()
        validate_operation_result = self.task_manager.Create(result[0], result[1])

        if False in validate_operation_result[0]:
            print("\n No se pudo crear la tarea por que algunos de estos datos en invalido: ", validate_operation_result[1])
            return 0
    

    def update_task(self):
        self.primary_menu_select = 2
        self.list_show_task()
        taskid = input("Increce el numero de la tarea qeu decea editar: ")
        result = self.solicitar_datos()

        validate_operation_result = self.task_manager.Update(taskid, result[0], result[1])

        if False in validate_operation_result[0]:
            print("\n No se pudo crear la tarea por que algunos de estos datos en invalido: ", validate_operation_result[1])
            return validate_operation_result

    def list_show_task(self):
        print("\n")
        print("=" * 70)
        print(f"{'ID':<5}{'Título':<25}{'Estado':<15}Descripción")
        print("=" * 70)

        for t in self.task_manager.ListAll():
            print(
                f"{t.Id:<5}"
                f"{t.Titulo:<25}"
                f"{self.status_to_string(t.Status):<15}"
                f"{t.Description}"
            )

        print("=" * 70)
        print("\n")

    def menu_principal(self):
        print("\n ------------ Welcome to task manager ------------ \n")
        if len(self.task_manager.ListAll()) == 0:
            print("No tines ninguna tarea en este momento: crea la primera tarea \n")
            if self.crear_tarea() == 0:
                print("\n retry ....\n")
                return 1
            return 0
        else:
            self.list_show_task()
            return input("""
                "1. Crear Tareas"
                "2. Editar Tareas"
                "3. Eliminar Tarea"
                "4. Iniciar Tarea"
                "5. Completar tarea"
                "6. Filtrar Tarea"
                "enter. Salir
            """)

    def show_opt_by_opt(self):
        match self.primary_menu_select:
            case 1:
                self.crear_tarea()
            case 2: 
                self.update_task()
            # case 3:
            #     self.delete_task()
            # case 4:
            #     self.iniciar_tarea()
            # case 5:
            #     self.completar_tarea()
            # case 6:
            #     self.listar_tarea_por_status()
            case 0:
                self.menu_principal()



# test
def main():
    consola = ConsoleUI()
    init = True
    while init:
        if consola.primary_menu_select == 0:
            guardar_int = consola.menu_principal()
            if guardar_int == '':
                continue
            consola.primary_menu_select = int(guardar_int)
            continue

        if consola.primary_menu_select == '':
            init = False
            continue

        print(consola.primary_menu_select)
        
        consola.show_opt_by_opt()
        consola.preguntar_si_continuar_en_el_procedimiento()

main()