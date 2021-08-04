import time, datetime
from company import Company
from employee import Hourly

#cartão de ponto
class WorkedHours:
    entries = []

    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Horas trabalhadas ╎" + " Horas extras ╎")
        print("└" + 94*"╌" + "┘")
        for entry in WorkedHours.entries:
            print(entry, end="")
            totalHours = entry.workStatus["total hours"] + entry.workStatus["extra hours"]
            if entry.workStatus["entry"] != None:
                print("Em serviço" + 8* " " + "╎")
            else: 
                print(int(totalHours), end="")
                print((18 - len(str(int(totalHours))))* " " + "╎", end=" ")
                print(int(entry.workStatus["extra hours"]), end="")
                print((13 - len(str(int(entry.workStatus["extra hours"]))))* " " + "╎")
        print("\n")

    def punchIn():
        Hourly.printTable()
        time.sleep(1)
        id = int(input("Por gentileza, informe seu ID\n"))
        
        employee = Company.searchEmployee(id)
        if employee == False:
            return
        
        if employee.category != "Horista": return print("Operação não permitida")
        else:
            currentHour = datetime.datetime.now()

            if employee.workStatus["entry"] == None:
                employee.workStatus["entry"] = currentHour
                if employee not in WorkedHours.entries:
                    WorkedHours.entries.append(employee)
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

