import time
from random import randint

class Syndicate:
    employees = {}

    def genSyndId():
        syndId = 0

        while syndId in Syndicate.employees:
            syndId = randint(0, 1000)
        return syndId

    def addEmployee(employee, fee, syndId, isInSyndicate):
        employee.fee = fee
        employee.syndId = syndId
        employee.isInSyndicate = isInSyndicate
        Syndicate.employees[employee.syndId] = employee
    
    def removeEmployee(employee):
        del Syndicate.employees[employee.syndId]
        employee.isInSyndicate = False
        employee.syndId = " "
        employee.fee.monthlyFee = 0
        employee.fee.serviceFee = []
        employee.fee.lastPaymentMonth = None
    
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
            fees = float(input("Informe o valor da taxa de serviço a ser cobrada: R$"))
            Syndicate.employees[syndId].fee.serviceFee.append(fees)
            print("Taxa de serviço atribuída com sucesso!")
        else:
            print("ID no sindicato inválido")
