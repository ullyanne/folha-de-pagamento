import time
import datetime
import textwrap

class Company:
    id = 0
    employees = []

    def addEmployee(new):
        Company.employees.append(new)
        print("Empregado adicionado com sucesso!")
        Company.id = Company.id+1
    
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎")
        print("└" + 59*"╌" + "┘")
        for employee in Company.employees:
            print(employee)
        print("\n")

    def removeEmployee():
        Company.printTable()
        time.sleep(1)
        id = input("Informe o ID do funcionário que deseja remover\n")
        id = int(id)

        for employee in Company.employees:
            if employee.id == id:
                if employee.isInSyndicate:
                    Syndicate.removeEmployee(employee.syndId)
                Company.employees.remove(employee)
                return print("Empregado removido com sucesso!")
        print("Funcionário não encontrado")

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
    
    def create():
        category = ""
        paymentMethod = ""
        isInSyndicate = None

        name = input("Insira o nome do novo empregado:\n")
        address = input("Insira o endereço do novo empregado:\n")
        id = Company.id

        while category not in ["1", "2", "3"]:
            category = input(textwrap.dedent("""\
                                                Insira o tipo do novo empregado:
                                                    [1] - Horista
                                                    [2] - Assalariado
                                                    [3] - Comissionado\n"""))
            
            if category not in ["1", "2", "3"]:
                print("Tipo inválido")
                time.sleep(1)

        while paymentMethod not in ["1", "2", "3"]:
            paymentMethod = input(textwrap.dedent("""\
                                                    Qual é o método de pagamento desejado?
                                                        [1] - Cheque pelos correios
                                                        [2] - Cheque em mãos
                                                        [3] - Depósito em conta bancária\n"""))
            if paymentMethod not in ["1", "2", "3"]:
                print("Método de pagamento inválido")
                time.sleep(1)
        
        while isInSyndicate not in [True, False]:
            isInSyndicate = input("Pertence ao sindicato? [S/n]\n")
            isInSyndicate = isInSyndicate.upper()
            
            if isInSyndicate == "S":
                isInSyndicate = True
                monthlyFee = int(input("Insira o valor da taxa mensal cobrada pelo sindicato:\n"))
            elif isInSyndicate == "N":
                isInSyndicate = False
            else:
                print("Resposta inválida")
                time.sleep(1)

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
        
        if newEmployee.isInSyndicate:
            newEmployee.monthlyFee = monthlyFee
            Syndicate.addEmployee(newEmployee)

        return newEmployee

    def search():
        valid = False
        id = int(input("Informe o ID do funcionário\n"))
        
        for employee in Company.employees:
            if employee.id == id:
                valid = True
                return employee
        
        print("Funcionário não encontrado")
        valid = False
        return valid

    #a alterar
    def edit():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Método de Pagamento        ", end = "")
        print("╎ Sindicato ╎ ╎ ID Sindicato ╎ ╎ Taxa Mensal ╎")
        print("└" + 133*"╌" + "┘")

        for employee in Company.employees:
            print(employee, end = "")
            print(Payroll.paymentMethod[employee.paymentMethod] + (27 - len(Payroll.paymentMethod[employee.paymentMethod]))* " " + "╎", end = "")
            print(" Ativo     ", end="") if employee.isInSyndicate == True else print(" Inativo   ", end = "")
            print("╎ ╎ " + str(employee.syndId) + (13 - len(str(employee.syndId)))* " " + "╎ ", end = "")
            print("╎ " + str(employee.monthlyFee) + (12 - len(str(employee.monthlyFee)))* " " + "╎")
        
        print("\n")
        time.sleep(1)
        employee = Employee.search()
        
        if employee == False:
            return

        option = ""

        while option not in ["1", "2", "3", "4", "5", "6", "7"]:
            option = input(textwrap.dedent("""\
                Qual dado deseja alterar?
                    [1] - Categoria
                    [2] - Nome
                    [3] - Endereço
                    [4] - Método de pagamento
                    [5] - Status no sindicato
                    [6] - ID no sindicato
                    [7] - Taxa mensal\n"""))
            
            if option not in ["1", "2", "3", "4", "5", "6", "7"]:
                print("Opção inválida")
                time.sleep(1)

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
            
            
            if category == "1":
                wage = input("Insira quanto o empregado recebe por hora:\n")
                newEmployee = Hourly(employee.name, employee.address, "Horista", employee.id, employee.paymentMethod, employee.isInSyndicate, wage)
            elif category == "2":
                fixedSalary = input("Insira o salário fixo mensal:\n")
                newEmployee = Salaried(employee.name, employee.address, "Assalariado", employee.id, employee.paymentMethod, employee.isInSyndicate, fixedSalary)
            elif category == "3":
                fixedSalary = input("Insira o salário fixo mensal:\n")
                comissionPercent = int(input("Insira o percentual de comissão:\n"))
                newEmployee = Commissioned(employee.name, employee.address, "Comissionado", employee.id, employee.paymentMethod, employee.isInSyndicate, fixedSalary, comissionPercent)
            
            if employee.isInSyndicate:
                    newEmployee.serviceFee = employee.serviceFee
                    newEmployee.syndId = employee.syndId
                    newEmployee.monthlyFee = employee.monthlyFee
                    Syndicate.removeEmployee(employee.syndId)
                    Syndicate.employees.append(newEmployee)
            Company.employees.remove(employee)
            Company.employees.append(newEmployee)
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
                employee.isInSyndicate = True
                monthlyFee = int(input("Insira o valor da taxa mensal cobrada pelo sindicato\n"))
                employee.monthlyFee = monthlyFee
                Syndicate.addEmployee(employee)
            else:
                Syndicate.removeEmployee(employee.syndId)
                employee.isInSyndicate = False
                employee.syndId = " "
                employee.monthlyFee = 0
                employee.serviceFee = []
        elif option == "6":
            if employee.isInSyndicate == True:
                employee.syndId = employee.syndId + 999
            else:
                return print("Funcionário não pertence ao sindicato")
        elif option == "7":
            if employee.isInSyndicate == False:
                return print("Operação não permitida")
            newMonthlyFee = input("Insira o novo valor da taxa mensal\n")
            employee.monthlyFee = newMonthlyFee
        
        print("Operação realizada com sucesso!")

class Syndicate:
    syndId = 999
    employees = []

    def addEmployee(new):
        new.syndId = Syndicate.syndId
        Syndicate.syndId = Syndicate.syndId-1
        Syndicate.employees.append(new)
    
    def removeEmployee(syndId):
        for employee in Syndicate.employees:
            if employee.syndId == syndId:
                Syndicate.employees.remove(employee)
    
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ ID Sindicato ╎" )
        print("└" + 74*"╌" + "┘")
        for employee in Syndicate.employees:
            print(employee, end="")
            syndId = str(employee.syndId)
            print(syndId + (13 - len(syndId))* " " + "╎")
        print("\n")
        time.sleep(1)
    
    def addServiceFee():
        Syndicate.printTable()
        syndId = int(input("Informe o ID do funcionário no sindicato\n"))
        for employee in Syndicate.employees:
            if employee.syndId == syndId:
                serviceFee = int(input("Informe o valor da taxa de serviço a ser cobrada\n"))
                employee.serviceFee.append(serviceFee)
                return print("Taxa de serviço atribuída com sucesso!")
        print("ID no sindicato inválido")

#cartão de ponto
class WorkedHours:
    entries = []

    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Horas trabalhadas ╎")
        print("└" + 79*"╌" + "┘")
        for entry in WorkedHours.entries:
            print(entry, end="")
            totalHours = entry.workStatus["total hours"]
            if totalHours == None:
                print("Em serviço" + 8* " " + "╎")
            else: 
                totalHours = int(totalHours)
                print(totalHours, end="")
                print((18 - len(str(totalHours)))* " " + "╎")
        print("\n")

    def punchIn():
        Company.printTable()
        time.sleep(1)
        id = int(input("Por gentileza, informe seu ID\n"))

        for employee in Company.employees:
            if employee.id == id:
                if employee.category != "Horista" : return print("Operação não permitida")
                currentHour = str(input("Insira a data e o horário atual no seguinte formato: AAAA-MM-DD HH:MM\n"))
                currentHour = datetime.datetime.strptime(currentHour, "%Y-%m-%d %H:%M")

                if employee.workStatus["entry"] == None:
                    employee.workStatus["entry"] = currentHour
                    WorkedHours.entries.append(employee)
                    print("Ponto de entrada lançado com sucesso!")
                else:
                    employee.workStatus["exit"] = currentHour
                    employee.workStatus["total hours"] = (employee.workStatus["exit"] - employee.workStatus["entry"]).total_seconds()/3600
                    employee.workStatus["entry"] = None
                    print("Ponto de saída lançado com sucesso!")
                
                return
        print("Funcionário não encontrado")

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
        
        for employee in Company.employees:
            if employee.category == "Comissionado":
                print(employee, end="")
                comission = str(employee.comissionPercent)
                print(comission + (9 - len(comission))* " " + "╎")
        print("\n")
        time.sleep(1)

    def postSale():
        Commissioned.printTable()
        id = int(input("Informe o ID do funcionário\n"))
    
        for employee in Company.employees:
            if employee.id == id and employee.category == "Comissionado":
                date = str(input("Insira a data de venda no seguinte formato: AAAA-MM-DD\n"))
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
                sale = int(input("Insira o valor da venda\n"))
                employee.salary = employee.salary + employee.comissionPercent/100 * sale
                return print("Venda lançada com sucesso!")
        print("Funcionário não encontrado")

class Payroll:
    paymentMethod = {
    "1": "Cheque pelos correios",
    "2": "Cheque em mãos",
    "3": "Depósito em conta bancária"
    }

def greetings():
    now = datetime.datetime.now().hour
    if now >= 6 and now < 12:
        print(">>>> Bom dia,", end="")
    elif now >= 12 and now < 18:
        print(">>>> Boa tarde,", end="")
    else:
        print(">>>> Boa noite,", end="")
    print(" seja bem-vindo(a) ao sistema de Folha de Pagamento <<<<\n")
    time.sleep(1)

def menu():
    greetings()
    choice = ""
    while choice != "8":
        choice = input(textwrap.dedent("""\
                ==========================================
                O que deseja fazer, hoje?
                    [1] - Adicionar um empregado
                    [2] - Remover um empregado
                    [3] - Lançar um cartão de ponto
                    [4] - Lançar um resultado de venda
                    [5] - Lançar uma taxa de serviço
                    [6] - Alterar detalhes de um empregado
                    [7] - Listar os empregados cadastrados
                    [8] - Sair\n"""))
        if choice == "1":
            newEmployee = Employee.create()
            Company.addEmployee(newEmployee)
        elif choice == "2":
            Company.removeEmployee()
        elif choice == "3":
            option = ""
            while option not in ["1", "2"]:
                option = input(textwrap.dedent("""\
                            Escolha uma opção abaixo:
                                [1] - Bater ponto
                                [2] - Listar cartão de ponto de hoje\n"""))
                if option not in ["1", "2"]:
                    print("Opção inválida")
                    time.sleep(1)
            WorkedHours.punchIn() if option == "1" else WorkedHours.printTable()
        elif choice == "4":
            Commissioned.postSale()
        elif choice == "5":
            Syndicate.addServiceFee()
        elif choice == "6":
            Employee.edit()
        elif choice == "7":
            Company.printTable()
        
        if choice!= "8" : time.sleep(1)
        
    print("Até mais :)")

menu()
