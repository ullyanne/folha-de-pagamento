import time
from random import randint

class Syndicate:
    employees = {}

    @staticmethod
    def genSyndId():
        syndId = 0

        while syndId in Syndicate.employees:
            syndId = randint(0, 1000)
        return syndId

    @classmethod
    def addEmployee(cls, employee, fee, syndId, isInSyndicate):
        employee.fee = fee
        employee.syndId = syndId
        employee.isInSyndicate = isInSyndicate
        cls.employees[employee.syndId] = employee
    
    @classmethod
    def removeEmployee(cls, employee):
        del cls.employees[employee.syndId]
        employee.isInSyndicate = False
        employee.syndId = " "
        employee.fee.reset()
    
    @staticmethod
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ ID Sindicato ╎" )
        print("└" + 74*"╌" + "┘")
        for employee in Syndicate.employees.values():
            print(employee, end="")
            syndId = str(employee.syndId)
            print(syndId + (13 - len(syndId))* " " + "╎")
        print("\n")
        time.sleep(1)
    
    @staticmethod
    def addServiceFee():
        Syndicate.printTable()
        syndId = int(input("Informe o ID do funcionário no sindicato\n"))
        
        if syndId in Syndicate.employees:
            fees = float(input("Informe o valor da taxa de serviço a ser cobrada: R$"))
            Syndicate.employees[syndId].fee.serviceFee = fees
            print("Taxa de serviço atribuída com sucesso!")
            return True
        else:
            print("ID no sindicato inválido")
            return False
    
    @staticmethod
    def updateMonthlyFee(employee):
        if employee.isInSyndicate == False:
            print("Operação não permitida")
            return False
        monthlyFee = float(input("Insira o novo valor da taxa mensal: R$"))
        employee.fee.monthlyFee = monthlyFee
        print("Operação realizada com sucesso!")
        return True
    
    @staticmethod
    def updateSyndId(employee):
        if employee.isInSyndicate == False:
            print("Funcionário não pertence ao sindicato")
            return False
        
        employee.syndId = Syndicate.genSyndId()
        print("Operação realizada com sucesso!")
        return True

    @classmethod
    def updateSyndStatus(cls, employee):
        if employee.isInSyndicate == False:
            monthlyFee = float(input("Insira o valor da taxa mensal cobrada pelo sindicato: R$"))
            employee.fee.monthlyFee = monthlyFee
            cls.addEmployee(employee, employee.fee, Syndicate.genSyndId(), True)
        else:
            cls.removeEmployee(employee)