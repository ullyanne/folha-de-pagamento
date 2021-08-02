from schedule import Biweekly, LastDay, Weekly
import time, datetime
from company import Company
from syndicate import Syndicate
from fee import Fee
from payroll import Payroll
from util import Util

class Employee:
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate):
        self.name = name
        self.address = address
        self.category = category
        self.id = id
        self.paymentMethod = paymentMethod
        self.schedule = schedule
        self.isInSyndicate = isInSyndicate
        self.syndId = " "
        self.salary = 0
        self.fee = Fee()
    
    def __str__(self):
        return("╎ " + self.category + " " *(13-len(self.category)) + "╎ " + str(self.id) + " " * (2-len(str(self.id)))
                + " ╎ " + self.name + " " * (19-len(self.name)) + " ╎ " 
                + self.address + " " * (15-len(self.address)) + " ╎ ")
    
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

    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Método de Pagamento        ", end = "")
        print("╎ Sindicato ╎ ╎ ID Sindicato ╎ ╎ Taxa Mensal ╎")
        print("└" + 133*"╌" + "┘")

        for employee in Company.employees.values():
            print(employee, end = "")
            print(Payroll.paymentMethod[employee.paymentMethod] + (27 - len(Payroll.paymentMethod[employee.paymentMethod]))* " " + "╎", end = "")
            print(" Ativo     ", end="") if employee.isInSyndicate == True else print(" Inativo   ", end = "")
            print("╎ ╎ " + str(employee.syndId) + (13 - len(str(employee.syndId)))* " " + "╎ ", end = "")
            print("╎ " + str(employee.fee.monthlyFee) + (12 - len(str(employee.fee.monthlyFee)))* " " + "╎")
        print("\n")
        time.sleep(1)

    def editCategory(self):
        category = ""
        category = Util.validChoice(category, 3, Util.newEmpType)
        newEmployee = Employee.create(category, self.name, self.address, self.id, self.paymentMethod, self.isInSyndicate)
        
        if self.isInSyndicate:
            Syndicate.addEmployee(newEmployee, self.fee, self.syndId, self.isInSyndicate)
        
        Company.removeEmployee(self.id)
        Company.addEmployee(newEmployee)
    def editName(self):
        newName = input("Insira o novo nome\n")
        self.name = newName
    def editAddress(self):
        newAddress = input("Insira o novo endereço\n")
        self.address = newAddress
    def editPaymentMethod(self):
        paymentMethod = ""
        self.paymentMethod = Util.validChoice(paymentMethod, 3, Util.newPaymentMethod)
    def editSyndStatus(self):
        if self.isInSyndicate == False:
            monthlyFee = float(input("Insira o valor da taxa mensal cobrada pelo sindicato: R$"))
            self.setMonthlyFee(monthlyFee)
            self.isInSyndicate = True
            Syndicate.addEmployee(self, self.fee, Syndicate.genSyndId(), self.isInSyndicate)
        else:
            Syndicate.removeEmployee(self)
    def editSyndId(self):
        if self.isInSyndicate == True:
            self.syndId = Syndicate.genSyndId()
            print("Operação realizada com sucesso!")
        else:
            print("Funcionário não pertence ao sindicato")
    def editMonthlyFee(self):
        if self.isInSyndicate == False:
            return print("Operação não permitida")
        monthlyFee = float(input("Insira o novo valor da taxa mensal: R$"))
        self.setMonthlyFee(monthlyFee)
        print("Operação realizada com sucesso!")
    def edit(self, option):
        try:
            {
            1: self.editCategory,
            2: self.editName,
            3: self.editAddress,
            4: self.editPaymentMethod,
            5: self.editSyndStatus,
            6: self.editSyndId,
            7: self.editMonthlyFee
            }.get(option)()
            if option != 6 and option != 7:
                print("Operação realizada com sucesso!")
        except:
            Util.errorMessage()
    def setMonthlyFee(self, monthlyFee):
        self.fee.monthlyFee = monthlyFee
    def setServiceFee(self, fee):
        self.fee.serviceFee.append(fee)
    def setSchedule(self, schedule):
        self.schedule = schedule
    
class Hourly(Employee):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, wage):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate)
        self.wage = float(wage)
        self.workStatus = {"entry": None, "exit": None, "total hours": 0, "extra hours": 0}
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎")
        print("└" + 59*"╌" + "┘")
        for employee in Company.employees.values():
            if employee.category == "Horista": print(employee)
        print("\n")
    def calcSalary(self):
        self.salary = self.wage * self.workStatus["total hours"] + (1.5 * self.wage * self.workStatus["extra hours"])
        Fee.subtract(self)
        self.workStatus["total hours"] = 0
        self.workStatus["extra hours"] = 0

class Salaried(Employee):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, fixedSalary):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate)
        self.fixedSalary = float(fixedSalary)
    def calcSalary(self):
        self.salary = self.fixedSalary
        Fee.subtract(self)

class Commissioned(Salaried):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, fixedSalary, comissionPercent):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate, fixedSalary)
        self.fixedSalary = float(fixedSalary)
        self.comissionPercent = float(comissionPercent)
        self.sales = 0
    def calcSalary(self):
        self.salary = self.fixedSalary/2 + self.comissionPercent/100 * self.sales
        Fee.subtract(self)
        self.sales = 0
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
        time.sleep(1)
    def postSale():
        Commissioned.printTable()
        id = int(input("Informe o ID do funcionário\n"))
        employee = Company.searchEmployee(id)
        if employee == False:
            return
        
        if employee.category == "Comissionado":
            date = str(input("Insira a data de venda no seguinte formato: AAAA-MM-DD\n"))

            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
            except:
                print("Formato inválido")
                return
            
            employee.sales = float(input("Insira o valor da venda: R$"))
            
            print("Venda lançada com sucesso!")
        else:
            print("Operação não permitida")
