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
        for i, entry in enumerate(entries):
            if isinstance(entry, types[i]):
                result.append(True)
                valores_a_validar.pop(i)
            else:
                result.append(False)
        return [result, valores_a_validar]

class Task:
    def __init__(self, Id: int, Titulo: str, Descripcion: str):
        self.Id = Id
        self.Titulo = Titulo
        self.Status = Status.CREATED
        self.Description = Descripcion

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
        task_manager: TaskManager = TaskManager()

    def status_to_string(self, status: Status):
        opciones = {
            Status.CREATED: "Creada",
            Status.EN_PROCESO: "En Proceso",
            Status.COMPLETADA: "Completada",
            Status.DELETE: "Eliminada"
        }

        return opciones[status]


task_manager = TaskManager()

task_manager.Create("test 1", "test 1")
task_manager.Update(0, "test 2", 0)

print(task_manager.Tasks[0].Status)

task_manager.CompletarTarea(0)

print(task_manager.Tasks[0].Status)


        

