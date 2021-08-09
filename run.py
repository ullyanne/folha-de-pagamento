import datetime
from time import sleep
from employee import Employee, Commissioned
from workedHours import WorkedHours
from company import Company
from syndicate import Syndicate
from util import Util
from payroll import Payroll

class Menu:
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
                sleep(1)
        
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
        Commissioned.printTable()
        
        id = int(input("Informe o ID do funcionário\n"))
        
        if id in Company.employees:
            employee = Company.employees[id]
            if employee.category == "Comissionado":
                employee.postSale()
            else:
                print("Operação não permitida")
        else:
            print("Funcionário não encontrado")
    def addServiceFee():
        Syndicate.addServiceFee()
    def updateEmployee():
        Company.printCompleteTable()
        id = int(input("Informe o ID do funcionário\n"))
        
        if id not in Company.employees:
            return print("Funcionário não encontrado")
        option = ""
        option = Util.validChoice(option, 8, Util.editEmployee)
        if option != 8:
            employee = Company.employees[id]
            try:
                {
                1: employee.updateCategory,
                2: employee.updateName,
                3: employee.updateAddress,
                4: employee.updatePaymentMethod,
                5: employee.updateSyndStatus,
                6: employee.updateSyndId,
                7: employee.updateMonthlyFee
                }.get(option)()
                if option != 6 and option != 7:
                    print("Operação realizada com sucesso!")
            except:
                Util.errorMessage()
            if option != 8: sleep(1)
    def employeeMenu():
        option = ""
        option = Util.validChoice(option, 5, Util.employeeMenu)
        if option != 5:
            try:
                {
                1: Menu.addEmployee,
                2: Menu.delEmployee,
                3: Menu.updateEmployee,
                4: Company.printTable
                }.get(option)()
            except:
                Util.errorMessage()
            if option != 3: sleep(1)
    def payroll():
        option = ""
        option = Util.validChoice(option, 3, Util.payroll)
        if option != 3:
            Payroll.pay() if option == 1 else Payroll.paymentTable()
            sleep(1)
    def schedules():
        option = ""
        option = Util.validChoice(option, 3, Util.schedules)
        if option != 3:
            Payroll.selectSchedule() if option == 1 else Payroll.addSchedule()
            sleep(1)
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

    def greetings():
        now = datetime.datetime.now().hour
        if now >= 6 and now < 12:
            print(">>>> Bom dia,", end="")
        elif now >= 12 and now < 18:
            print(">>>> Boa tarde,", end="")
        else:
            print(">>>> Boa noite,", end="")
        print(" seja bem-vindo(a) ao sistema de Folha de Pagamento <<<<\n")
        sleep(1)
    
    def menu():
        Menu.greetings()
        choice = ""
        while choice != 7:
            choice = ""
            choice = Util.validChoice(choice, 7, Util.menu)
            Menu.selectOption.get(choice)()
            if choice == 2 or choice == 3 or choice == 4: sleep(1)

Menu.menu()
