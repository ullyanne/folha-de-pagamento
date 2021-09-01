from schedule import Biweekly, LastDay, Weekly
from memento import Settings as memento
from time import sleep
from company import Company
from syndicate import Syndicate
from fee import Fee
from util import Util
import datetime

class Employee:
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate):
        self._name = name
        self._address = address
        self._category = category
        self._id = id
        self._paymentMethod = paymentMethod
        self._schedule = schedule
        self._isInSyndicate = isInSyndicate
        self._syndId = " "
        self._salary = 0
        self._fee = Fee()
    
    def __str__(self):
        return("╎ " + self._category + " " *(13-len(self._category)) + "╎ " + str(self._id) + " " * (2-len(str(self._id)))
                + " ╎ " + self._name + " " * (19-len(self._name)) + " ╎ " 
                + self._address + " " * (15-len(self._address)) + " ╎ ")
    
    @staticmethod
    def create(category, name, address, id, paymentMethod, isInSyndicate):
        if category == 1:
            wage = input("Insira quanto o empregado recebe por hora: R$")
            newEmployee = Hourly(name, address, "Horista", id, paymentMethod, Weekly(4), isInSyndicate, wage)
        elif category == 2:
            fixedSalary = input("Insira o salário fixo mensal: R$")
            newEmployee = Salaried(name, address, "Assalariado", id, paymentMethod, LastDay(None), isInSyndicate, fixedSalary)
        elif category == 3:
            fixedSalary = input("Insira o salário fixo mensal: R$")
            comissionPercent = float(input("Insira o percentual de comissão []%: "))
            newEmployee = Commissioned(name, address, "Comissionado", id, paymentMethod, Biweekly(4), isInSyndicate, fixedSalary, comissionPercent)
        return newEmployee

    @property
    def name(self):
        return self._name
    def updateName(self):
        newName = input("Insira o novo nome\n")
        self._name = newName
    
    @property
    def address(self):
        return self._address
    def updateAddress(self):
        newAddress = input("Insira o novo endereço\n")
        self._address = newAddress
    
    @property
    def id(self):
        return self._id
    
    @property
    def paymentMethod(self):
        return self._paymentMethod
    def updatePaymentMethod(self):
        paymentMethod = ""
        self._paymentMethod = Util.validChoice(paymentMethod, 3, Util.newPaymentMethod)
    
    @property
    def salary(self):
        return self._salary
    @salary.setter
    def salary(self, salary):
        if salary > 0:
            self._salary = salary

    @property
    def category(self):
        return self._category
    def updateCategory(self):
        category = ""
        category = Util.validChoice(category, 3, Util.newEmpType)
        newEmployee = Employee.create(category, self.name, self.address, self.id, self.paymentMethod, self.isInSyndicate)
        
        if self.isInSyndicate:
            Syndicate.addEmployee(newEmployee, self.fee, self.syndId, self.isInSyndicate)
        
        Company.removeEmployee(self.id)
        Company.addEmployee(newEmployee)

    @property
    def isInSyndicate(self):
        return self._isInSyndicate
    @isInSyndicate.setter
    def isInSyndicate(self, isInSyndicate):
        self._isInSyndicate = isInSyndicate
    def updateSyndStatus(self):
        Syndicate.updateSyndStatus(self)
    
    @property
    def syndId(self):
        return self._syndId
    @syndId.setter
    def syndId(self, syndId):
        self._syndId = syndId
    def updateSyndId(self):
        if Syndicate.updateSyndId(self) == True:
            memento.caretaker.manage()
    
    @property
    def fee(self):
        return self._fee
    @fee.setter
    def fee(self, fee):
        self._fee = fee
    def updateMonthlyFee(self):
        if Syndicate.updateMonthlyFee(self) == True:
            memento.caretaker.manage()
    
    @property
    def schedule(self):
        return self._schedule
    @schedule.setter
    def schedule(self, schedule):
        self._schedule = schedule

class Hourly(Employee):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, wage):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate)
        self._wage = float(wage)
        self.workStatus = {"entry": None, "exit": None, "total hours": 0, "extra hours": 0}
    
    @property
    def wage(self):
        return self._wage
    @wage.setter
    def wage(self, wage):
        self._wage = wage
    
    @staticmethod
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎")
        print("└" + 59*"╌" + "┘")
        for employee in Company.employees.values():
            if employee.category == "Horista": print(employee)
        print("\n", end="")
        sleep(1)
    
    def calcSalary(self):
        self.salary = self.wage * self.workStatus["total hours"] + (1.5 * self.wage * self.workStatus["extra hours"]) - self.fee.subtract(self.isInSyndicate)
        self.workStatus["total hours"] = 0
        self.workStatus["extra hours"] = 0

class Salaried(Employee):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, fixedSalary):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate)
        self._fixedSalary = float(fixedSalary)
    
    @property
    def fixedSalary(self):
        return self._fixedSalary
    @fixedSalary.setter
    def fixedSalary(self, fixedSalary):
        self._fixedSalary = fixedSalary

    def calcSalary(self):
        self.salary = self.fixedSalary - self.fee.subtract(self.isInSyndicate)

class Commissioned(Salaried):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, fixedSalary, comissionPercent):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate, fixedSalary)
        self._fixedSalary = float(fixedSalary)
        self._comissionPercent = float(comissionPercent)
        self._sales = 0
    
    @property
    def comissionPercent(self):
        return self._comissionPercent
    @comissionPercent.setter
    def comissionPercent(self, comissionPercent):
        self._comissionPercent = comissionPercent
    
    @property
    def sales(self):
        return self._sales
    @sales.setter
    def sales(self, sales):
        self._sales = sales
    
    def calcSalary(self):
        self.salary = self.fixedSalary/2 + self.comissionPercent/100 * self.sales - self.fee.subtract(self.isInSyndicate)
        self.sales = 0
    
    @staticmethod
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Comissão ╎" + " Vendas ╎")
        print("└" + 79*"╌" + "┘")
        
        for employee in Company.employees.values():
            if employee.category == "Comissionado":
                print(employee, end="")
                comission = str(employee.comissionPercent)
                sales = str(employee.sales)
                print(comission + "%" + (8 - len(comission))* " " + "╎", end=" ")
                print(sales + (7 - len(sales)) * " " + "╎")
        print("\n")
        sleep(1)

    def postSale(self):
        date = str(input("Insira a data de venda no seguinte formato: AAAA-MM-DD\n"))
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        except:
            print("Formato inválido")
            return
        
        self.sales = float(input("Insira o valor da venda: R$"))
        memento.caretaker.manage()
        print("Venda lançada com sucesso!")