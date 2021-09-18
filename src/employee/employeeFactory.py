from ..tools import Util
from ..payroll import Biweekly, LastDay, Weekly
from ..company import Company
from ..syndicate import Syndicate
from . import Commissioned, Hourly, Salaried

class EmployeeFactory():
    @staticmethod
    def createEmployee(category, name, address, id, paymentMethod, isInSyndicate, monthlyFee):
        if category == 1:
            wage = input("Insira quanto o empregado recebe por hora: R$")
            newEmployee = Hourly(name, address, "Horista", id, paymentMethod, Weekly(4), isInSyndicate, monthlyFee, wage)
        elif category == 2:
            fixedSalary = input("Insira o salário fixo mensal: R$")
            newEmployee = Salaried(name, address, "Assalariado", id, paymentMethod, LastDay(None), isInSyndicate, monthlyFee, fixedSalary)
        elif category == 3:
            fixedSalary = input("Insira o salário fixo mensal: R$")
            commissionPercent = float(input("Insira o percentual de comissão []%: "))
            newEmployee = Commissioned(name, address, "Comissionado", id, paymentMethod, Biweekly(4), isInSyndicate, monthlyFee, fixedSalary, commissionPercent)
        return newEmployee
    
    @classmethod
    def updateCategory(cls, employee):
        category = ""
        category = Util.validChoice(category, 3, Util.newEmpType)
        newEmployee = cls.createEmployee(category, employee.name, employee.address, employee.id, employee.paymentMethod, employee.isInSyndicate, employee.fee.monthlyFee)
        
        if employee.isInSyndicate:
            Syndicate.addEmployee(newEmployee, employee.fee, employee.syndId, employee.isInSyndicate)
        
        Company.removeEmployee(employee.id)
        Company.addEmployee(newEmployee)