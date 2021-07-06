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
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 16 + "╎ Endereço " + 7* " " + "╎")
        print("└" + 60*"╌" + "┘")
        for employee in Company.employees:
            print(employee)
        print("\n")
        time.sleep(1)

    def removeEmployee():
        Company.printTable()
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
        self.syndId = None
        self.salary = 0
    
    def __str__(self):
        return("╎ " + self.category + " " *(13-len(self.category)) + "╎ " + str(self.id) + " " * (2-len(str(self.id)))
                + " ╎ " + self.name + " " * (20-len(self.name)) + " ╎ " 
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
            Syndicate.addEmployee(newEmployee)

        return newEmployee

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

#cartão de ponto
class WorkedHours:
    entries = []

    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 16 + "╎ Endereço " + 7* " " + "╎ Horas trabalhadas ╎")
        print("└" + 80*"╌" + "┘")
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
        self.comissionPercent = int(comissionPercent)
    
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 16 + "╎ Endereço " + 7* " " + "╎ Comissão ╎" )
        print("└" + 71*"╌" + "┘")
        for employee in Company.employees:
            if employee.category == "Comissionado" : print(employee, end="")
            comission = str(employee.comissionPercent)
            print(comission + (9 - len(comission))* " " + "╎")
        print("\n")
        time.sleep(1)

    def postSale():
        Commissioned.printTable()
        id = int(input("Informe o ID do funcionário\n"))
    
        for employee in Company.employees:
            if employee.id == id:
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
            print("Em breve")
        elif choice == "6":
            print("Em breve")
        elif choice == "7":
            Company.printTable()
        
        if choice!= "8" : time.sleep(1)
        
    print("Até mais :)")

menu()
