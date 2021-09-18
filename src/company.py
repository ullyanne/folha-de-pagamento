from .table import Rows
from .table import EmployeesColumns, CommissionedColumns, EmployeesPlusColumns
from random import randint

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
    def isInCompany(cls, id):
        if id in cls.employees:
            return True
        else:
            return print("Funcionário não encontrado")
    
    @classmethod
    def getEmployee(cls, id):
        return cls.employees[id]

    @classmethod
    def addEmployee(cls, employee):
        cls.employees[employee.id] = employee
    
    @classmethod
    def removeEmployee(cls, id):
        del cls.employees[id]
    
    @classmethod
    def printTable(cls):
        EmployeesColumns.display()
        Rows.displayEmployees(cls.employees.values())
    
    @classmethod
    def printHourlyTable(cls):
        EmployeesColumns.display()
        Rows.displayHourly(cls.employees.values())

    @classmethod
    def printCommissionedTable(cls):
        CommissionedColumns.display()
        Rows.displayCommissioned(cls.employees.values())
    
    @classmethod
    def printCompleteTable(cls):
        EmployeesPlusColumns.display()
        Rows.displayEmployeesPlus(cls.employees.values(), cls.paymentMethod)