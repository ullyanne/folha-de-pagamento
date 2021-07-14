import time
from random import randint

class Syndicate:
    employees = {}

    def genSyndId():
        syndId = 0

        while syndId in Syndicate.employees:
            syndId = randint(0, 1000)
        return syndId

    def addEmployee(new, monthlyFee, syndId, isInSyndicate, serviceFee):
        new.monthlyFee = monthlyFee
        new.syndId = syndId
        new.isInSyndicate = isInSyndicate
        new.serviceFee = serviceFee
        Syndicate.employees[new.syndId] = new
    
    def removeEmployee(employee):
        del Syndicate.employees[employee.syndId]
        employee.isInSyndicate = False
        employee.syndId = " "
        employee.monthlyFee = 0
        employee.serviceFee = []
    
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ ID Sindicato ╎" )
        print("└" + 74*"╌" + "┘")
        for employee in Syndicate.employees.values():
            print(employee, end="")
            syndId = str(employee.syndId)
            print(syndId + (13 - len(syndId))* " " + "╎")
        print("\n")
        time.sleep(1)
    
    def addServiceFee():
        Syndicate.printTable()
        syndId = int(input("Informe o ID do funcionário no sindicato\n"))
        
        if syndId in Syndicate.employees:
            serviceFee = int(input("Informe o valor da taxa de serviço a ser cobrada\n"))
            Syndicate.employees[id].serviceFee.append(serviceFee)
            print("Taxa de serviço atribuída com sucesso!")
        else:
            print("ID no sindicato inválido")
