from ..table import Rows
from ..table import SyndicateColumns
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
    def isInSyndicate(cls, syndId):
        if syndId in cls.employees:
            return True
        else:
            return print("Funcionário não pertence ao sindicato")
    
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
    
    @classmethod
    def printTable(cls):
        SyndicateColumns.display()
        Rows.displaySyndicate(cls.employees.values())
    
    @classmethod
    def addServiceFee(cls, syndId):
        if cls.isInSyndicate(syndId):
            fees = float(input("Informe o valor da taxa de serviço a ser cobrada: R$"))
            Syndicate.employees[syndId].fee.serviceFee = fees
            print("Taxa de serviço atribuída com sucesso!")
    
    @classmethod
    def updateMonthlyFee(cls, employee):
        if cls.isInSyndicate(employee.syndId):
            monthlyFee = float(input("Insira o novo valor da taxa mensal: R$"))
            employee.fee.monthlyFee = monthlyFee
    
    @classmethod
    def updateSyndId(cls, employee):
        if cls.isInSyndicate(employee.syndId):
            id = Syndicate.genSyndId()
            del cls.employees[employee.syndId]
            employee.syndId = id
            cls.employees[employee.syndId] = employee

    @classmethod
    def updateSyndStatus(cls, employee):
        if employee.isInSyndicate == False:
            monthlyFee = float(input("Insira o valor da taxa mensal cobrada pelo sindicato: R$"))
            employee.fee.monthlyFee = monthlyFee
            cls.addEmployee(employee, employee.fee, Syndicate.genSyndId(), True)
        else:
            cls.removeEmployee(employee)