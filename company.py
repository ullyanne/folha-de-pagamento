from random import randint
from time import sleep

class Company:
    employees = {}
    paymentMethod = {
        1: "Cheque pelos correios",
        2: "Cheque em mãos",
        3: "Depósito em conta bancária"
    }
    
    @staticmethod
    def genId():
        id = 0
        while id in Company.employees:
            id = randint(0, 99)
        return id

    @classmethod
    def addEmployee(cls, employee):
        cls.employees[employee.id] = employee
    
    @classmethod
    def removeEmployee(cls, id):
        del cls.employees[id]
    
    @staticmethod
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎")
        print("└" + 59*"╌" + "┘")
        for employee in Company.employees.values():
            print(employee)
        print("\n", end="")
    
    @staticmethod
    def printCompleteTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Método de Pagamento        ", end = "")
        print("╎ Sindicato ╎ ╎ ID Sindicato ╎ ╎ Taxa Mensal ╎")
        print("└" + 133*"╌" + "┘")

        for employee in Company.employees.values():
            print(employee, end = "")
            print(Company.paymentMethod[employee.paymentMethod] + (27 - len(Company.paymentMethod[employee.paymentMethod]))* " " + "╎", end = "")
            print(" Ativo     ", end="") if employee.isInSyndicate == True else print(" Inativo   ", end = "")
            print("╎ ╎ " + str(employee.syndId) + (13 - len(str(employee.syndId)))* " " + "╎ ", end = "")
            print("╎ " + str(employee.fee.monthlyFee) + (12 - len(str(employee.fee.monthlyFee)))* " " + "╎")
        print("\n")
        sleep(1)