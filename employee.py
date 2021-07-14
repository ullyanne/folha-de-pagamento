import time, datetime, textwrap
from company import Company
from syndicate import Syndicate
from payroll import Payroll

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
        if category == "1":
            wage = input("Insira quanto o empregado recebe por hora:\n")
            newEmployee = Hourly(name, address, "Horista", id, paymentMethod, isInSyndicate, wage)
        elif category == "2":
            fixedSalary = input("Insira o salário fixo mensal:\n")
            newEmployee = Salaried(name, address, "Assalariado", id, paymentMethod, isInSyndicate, fixedSalary)
        elif category == "3":
            fixedSalary = input("Insira o salário fixo mensal:\n")
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
        
    #a alterar
    def edit(employee, option):
        if option == "1":
            category = ""

            while category not in ["1", "2", "3"]:
                category = input(textwrap.dedent("""\
                                                    Escolha a nova categoria:
                                                        [1] - Horista
                                                        [2] - Assalariado
                                                        [3] - Comissionado\n"""))
                
                if category not in ["1", "2", "3"]:
                    print("Tipo inválido")
                    time.sleep(1)
            
            newEmployee = Employee.create(category, employee.name, employee.address, employee.id, employee.paymentMethod, employee.isInSyndicate)
            
            if employee.isInSyndicate:
                Syndicate.addEmployee(newEmployee, employee.monthlyFee, employee.syndId, employee.serviceFee)
                Syndicate.removeEmployee(employee.syndId)
            
            Company.removeEmployee(employee.id)
            Company.addEmployee(newEmployee)
        elif option == "2":
            newName = input("Insira o novo nome\n")
            employee.name = newName
        elif option == "3":
            newAddress = input("Insira o novo endereço\n")
            employee.address = newAddress
        elif option == "4":
            paymentMethod = ""
            while paymentMethod not in ["1", "2", "3"]:
                paymentMethod = input(textwrap.dedent("""\
                                                        Escolha o novo método de pagamento
                                                            [1] - Cheque pelos correios
                                                            [2] - Cheque em mãos
                                                            [3] - Depósito em conta bancária\n"""))
                if paymentMethod not in ["1", "2", "3"]:
                    print("Método de pagamento inválido")
                    time.sleep(1)
            employee.paymentMethod = paymentMethod
        elif option == "5":
            if employee.isInSyndicate == False:
                monthlyFee = int(input("Insira o valor da taxa mensal cobrada pelo sindicato\n"))
                employee.monthlyFee = monthlyFee
                Syndicate.addEmployee(employee, monthlyFee, Syndicate.genSyndId(), True, 0)
            else:
                Syndicate.removeEmployee(employee)
        elif option == "6":
            if employee.isInSyndicate == True:
                employee.syndId = Syndicate.genSyndId()
            else:
                return print("Funcionário não pertence ao sindicato")
        elif option == "7":
            if employee.isInSyndicate == False:
                return print("Operação não permitida")
            newMonthlyFee = input("Insira o novo valor da taxa mensal\n")
            employee.monthlyFee = newMonthlyFee
        
        print("Operação realizada com sucesso!")

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
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
                sale = int(input("Insira o valor da venda\n"))
                employee.salary = employee.salary + employee.comissionPercent/100 * sale
                print("Venda lançada com sucesso!")
        except:
            print("Funcionário não encontrado")
