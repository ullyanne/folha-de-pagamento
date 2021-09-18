from .table import Rows
from .table import WorkedHoursColumns
from .company import Company
import datetime

#cartão de ponto
class WorkedHours:
    entries = []

    @classmethod
    def printTable(cls):
        WorkedHoursColumns.display()
        Rows.displayWorkedHours(cls.entries)
    
    @classmethod
    def addEntry(cls, employee, currentHour):
        employee.setEntryHour(currentHour)
        if employee not in cls.entries:
            cls.entries.append(employee)
        print("Ponto de entrada lançado com sucesso!")

    @classmethod
    def punchIn(cls, id):
        employee = Company.getEmployee(id)

        if employee.getEntryHour() == None:
            cls.addEntry(employee, cls.currentHour())
        else:
            employee.setExitHour(cls.currentHour())
            employee.setWorkdayExtraHours()
            employee.setTotalHours()
            employee.resetEntryHour()
            print("Ponto de saída lançado com sucesso!")

    def currentHour():
        return datetime.datetime.now()
