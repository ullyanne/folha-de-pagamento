import time, datetime, textwrap
from company import Company
from syndicate import Syndicate
from payroll import Payroll
from util import Util

class Employee:
    def __init__(self, name, address, category, id, paymentMethod, isInSyndicate):
        self.name = name
        self.address = address
        self.category = category
        self.id = id
        self.paymentMethod = paymentMethod
        self.isInSyndicate = isInSyndicate
        self.syndId = " "
        self.salary = 0
        self.monthlyFee = 0
        self.serviceFee = []
    
    def __str__(self):
        return("╎ " + self.category + " " *(13-len(self.category)) + "╎ " + str(self.id) + " " * (2-len(str(self.id)))
                + " ╎ " + self.name + " " * (19-len(self.name)) + " ╎ " 
                + self.address + " " * (15-len(self.address)) + " ╎ ")
    
    def create(category, name, address, id, paymentMethod, isInSyndicate):
        if category == 1:
            wage = input("Insira quanto o empregado recebe por hora: R$")
            newEmployee = Hourly(name, address, "Horista", id, paymentMethod, isInSyndicate, wage)
        elif category == 2:
            fixedSalary = input("Insira o salário fixo mensal: R$")
            newEmployee = Salaried(name, address, "Assalariado", id, paymentMethod, isInSyndicate, fixedSalary)
        elif category == 3:
            fixedSalary = input("Insira o salário fixo mensal: R$")
            comissionPercent = int(input("Insira o percentual de comissão:\n"))
            newEmployee = Commissioned(name, address, "Comissionado", id, paymentMethod, isInSyndicate, fixedSalary, comissionPercent)

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
            print("╎ " + str(employee.monthlyFee) + (12 - len(str(employee.monthlyFee)))* " " + "╎")

        print("\n")
        time.sleep(1)
        
    def editCategory(self):
        category = ""
        category = Util.validChoice(category, 3, Util.newEmpType)
        newEmployee = Employee.create(category, self.name, self.address, self.id, self.paymentMethod, self.isInSyndicate)
        
        if self.isInSyndicate:
            Syndicate.addEmployee(newEmployee, self.monthlyFee, self.syndId, self.isInSyndicate, self.serviceFee)
        
        Company.removeEmployee(self.id)
        Company.addEmployee(newEmployee)
    def editName(self):
        newName = input("Insira o novo nome\n")
        self.name = newName
    def editAdress(self):
        newAddress = input("Insira o novo endereço\n")
        self.address = newAddress
    def editPaymentMethod(self):
        paymentMethod = ""
        self.paymentMethod = Util.validChoice(paymentMethod, 3, Util.newPaymentMethod)
    def editSyndStatus(self):
        if self.isInSyndicate == False:
            self.monthlyFee = int(input("Insira o valor da taxa mensal cobrada pelo sindicato: R$"))
            self.isInSyndicate = True
            Syndicate.addEmployee(self, self.monthlyFee, Syndicate.genSyndId(), self.isInSyndicate, 0)
        else:
            Syndicate.removeEmployee(self)
    def editSyndId(self):
        if self.isInSyndicate == True:
            self.syndId = Syndicate.genSyndId()
        else:
            return print("Funcionário não pertence ao sindicato")
    def editMonthlyFee(self):
        if self.isInSyndicate == False:
            return print("Operação não permitida")
        self.monthlyFee= input("Insira o novo valor da taxa mensal: R$")
    def edit(self, option):
        try:
            {
            1: self.editCategory,
            2: self.editName,
            3: self.editAdress,
            4: self.editPaymentMethod,
            5: self.editSyndStatus,
            6: self.editSyndId,
            7: self.editMonthlyFee
            }.get(option)()
            print("Operação realizada com sucesso!")
        except:
            Util.errorMessage()

class Hourly(Employee):
    def __init__(self, name, address, category, id, paymentMethod, isInSyndicate, wage):
        super().__init__(name, address, category, id, paymentMethod, isInSyndicate)
        self.wage = wage
        self.workStatus = {"entry": None, "exit": None, "total hours": None}

class Salaried(Employee):
    def __init__(self, name, address, category, id, paymentMethod, isInSyndicate, fixedSalary):
        super().__init__(name, address, category, id, paymentMethod, isInSyndicate)
        self.fixedSalary = fixedSalary

class Commissioned(Salaried):
    def __init__(self, name, address, category, id, paymentMethod, isInSyndicate, fixedSalary, comissionPercent):
        super().__init__(name, address, category, id, paymentMethod, isInSyndicate, fixedSalary)
        self.fixedSalary = fixedSalary
        self.comissionPercent = comissionPercent
    
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Comissão ╎" )
        print("└" + 70*"╌" + "┘")
        
        for employee in Company.employees.values():
            if employee.category == "Comissionado":
                print(employee, end="")
                comission = str(employee.comissionPercent)
                print(comission + (9 - len(comission))* " " + "╎")
        print("\n")
        time.sleep(1)

    def postSale():
        Commissioned.printTable()
        id = int(input("Informe o ID do funcionário\n"))
        
        try:
            employee = Company.employees[id]

            if employee.category == "Comissionado":
                date = str(input("Insira a data de venda no seguinte formato: AAAA-MM-DD\n"))

                try:
                    date = datetime.datetime.strptime(date, "%Y-%m-%d")
                except:
                    print("Formato inválido")
                    return
                
                sale = int(input("Insira o valor da venda: R$"))
                employee.salary = employee.salary + employee.comissionPercent/100 * sale
                print("Venda lançada com sucesso!")
            else:
                print("Operação não permitida")
        except:
            print("Funcionário não encontrado")
