import datetime
from company import Company

#cartão de ponto
class WorkedHours:
    entries = []

    @staticmethod
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Horas trabalhadas ╎" + " Horas extras ╎")
        print("└" + 94*"╌" + "┘")
        for entry in WorkedHours.entries:
            print(entry, end="")
            totalHours = entry.workStatus["total hours"] + entry.workStatus["extra hours"]
            if entry.workStatus["entry"] != None:
                print("Em serviço" + 23* " " + "╎")
            else: 
                print(int(totalHours), end="")
                print((18 - len(str(int(totalHours))))* " " + "╎", end=" ")
                print(int(entry.workStatus["extra hours"]), end="")
                print((13 - len(str(int(entry.workStatus["extra hours"]))))* " " + "╎")
        print("\n", end="")
    
    @classmethod
    def punchIn(cls, id):
        employee = Company.employees[id]
        currentHour = datetime.datetime.now()

        if employee.workStatus["entry"] == None:
            employee.workStatus["entry"] = currentHour
            if employee not in cls.entries:
                cls.entries.append(employee)
            print("Ponto de entrada lançado com sucesso!")
        else:
            employee.workStatus["exit"] = currentHour
            hours = (employee.workStatus["exit"] - employee.workStatus["entry"]).total_seconds()/3600
            extraHours = 0

            if hours > 8:
                extraHours = hours - 8
                employee.workStatus["extra hours"] = employee.workStatus["extra hours"] + extraHours
            
            employee.workStatus["total hours"] = employee.workStatus["total hours"] + hours - extraHours
            employee.workStatus["entry"] = None
            print("Ponto de saída lançado com sucesso!")

