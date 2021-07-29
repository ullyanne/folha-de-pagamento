import time
import datetime
from company import Company
from employee import Employee

#cartão de ponto
class WorkedHours:
    entries = []

    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Horas trabalhadas ╎")
        print("└" + 79*"╌" + "┘")
        for entry in WorkedHours.entries:
            print(entry, end="")
            totalHours = entry.workStatus["total hours"]
            if totalHours == None:
                print("Em serviço" + 8* " " + "╎")
            else: 
                totalHours = int(totalHours)
                print(totalHours, end="")
                print((18 - len(str(totalHours)))* " " + "╎")
        print("\n")

    def punchIn():
        Company.printTable()
        time.sleep(1)
        id = int(input("Por gentileza, informe seu ID\n"))
        employee = Company.employees[id]

        if employee not in Company.employees.values(): print("Funcionário não encontrado")
        elif employee.category != "Horista": return print("Operação não permitida")
        else:
            currentHour = str(input("Insira a data e o horário atual no seguinte formato: AAAA-MM-DD HH:MM\n"))
            
            try:
                currentHour = datetime.datetime.strptime(currentHour, "%Y-%m-%d %H:%M")
            except:
                print("Formato inválido")
                return

            if employee.workStatus["entry"] == None:
                employee.workStatus["entry"] = currentHour
                WorkedHours.entries.append(employee)
                print("Ponto de entrada lançado com sucesso!")
            else:
                employee.workStatus["exit"] = currentHour
                employee.workStatus["total hours"] = (employee.workStatus["exit"] - employee.workStatus["entry"]).total_seconds()/3600
                employee.workStatus["entry"] = None
                print("Ponto de saída lançado com sucesso!")

