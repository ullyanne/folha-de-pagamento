import time, datetime
from employee import Employee, Commissioned
from workedHours import WorkedHours
from company import Company
from syndicate import Syndicate
from util import Util
from payroll import Payroll

class Menu:
    def employeeMenu():
        option = ""
        option = Util.validChoice(option, 5, Util.employeeMenu)
        if option != 5:
            Menu.employeeOptions.get(option)()
    def addEmployee():
        category = 0
        paymentMethod = 0
        isInSyndicate = None

        name = input("Insira o nome do novo empregado:\n")
        address = input("Insira o endereço do novo empregado:\n")
        id = Company.genId()
        category = Util.validChoice(category, 3, Util.employeeType)
        paymentMethod = Util.validChoice(paymentMethod, 3, Util.paymentMethod)
        
        while isInSyndicate not in [True, False]:
            isInSyndicate = input("Pertence ao sindicato? [S/n]\n").upper()
            
            if isInSyndicate == "S":
                isInSyndicate = True
                monthlyFee = float(input("Insira o valor da taxa mensal cobrada pelo sindicato: R$"))
                syndId = Syndicate.genSyndId()
            elif isInSyndicate == "N":
                isInSyndicate = False
            else:
                print("Resposta inválida")
                time.sleep(1)
        
        newEmployee = Employee.create(category, name, address, id, paymentMethod, isInSyndicate)
        
        
        if newEmployee.isInSyndicate:
            newEmployee.fee.monthlyFee = monthlyFee
            Syndicate.addEmployee(newEmployee, newEmployee.fee, syndId, isInSyndicate)
        
        Company.addEmployee(newEmployee)
        print("Empregado adicionado com sucesso!")
    def delEmployee():
        Company.printTable()
        id = int(input("Informe o ID do funcionário que deseja remover\n"))

        try:
            Company.removeEmployee(id)
            print("Empregado removido com sucesso!")
        except:
            print("Funcionário não encontrado")
    def workedHours():
        option = ""
        option = Util.validChoice(option, 2, Util.workedHours)
        WorkedHours.punchIn() if option == 1 else WorkedHours.printTable()
    def postSale():
        Commissioned.postSale()
    def addServiceFee():
        Syndicate.addServiceFee()
    def editEmployee():
        Employee.printTable()
        id = int(input("Informe o ID do funcionário\n"))
        
        if id in Company.employees:
            option = ""
            option = Util.validChoice(option, 8, Util.editEmployee)
            if option != 8:
                Company.employees[id].edit(option)
        else:
            print("Funcionário não encontrado")
    def printEmployees():
        Company.printTable()
    def payroll():
        option = ""
        option = Util.validChoice(option, 3, Util.payroll)
        if option != 3:
            Payroll.pay() if option == 1 else Payroll.paymentTable()
    def schedules():
        option = ""
        option = Util.validChoice(option, 3, Util.schedules)
        if option != 3:
            Payroll.selectSchedule() if option == 1 else Payroll.addSchedule()
    def quit():
        print("Até mais :)")

    selectOption = {
        1: employeeMenu,
        2: workedHours,
        3: postSale,
        4: addServiceFee,
        5: payroll,
        6: schedules,
        7: quit
    }

    employeeOptions = {
        1: addEmployee,
        2: delEmployee,
        3: editEmployee,
        4: printEmployees
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
        Menu.greetings()
        choice = ""
        while choice != 7:
            choice = ""
            choice = Util.validChoice(choice, 7, Util.menu)
            Menu.selectOption.get(choice)()
            if choice != 7 : time.sleep(1)

Menu.menu()
