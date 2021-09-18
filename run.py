from datetime import datetime
from time import sleep
from src import Settings as memento
from src import EmployeeFactory, Commissioned, Hourly
from src import WorkedHours, Company, Syndicate, Util, Payroll

class Menu:
    @staticmethod
    def addEmployee():
        category = 0
        paymentMethod = 0
        isInSyndicate = None
        monthlyFee = 0

        name = input("Insira o nome do novo empregado:\n")
        address = input("Insira o endereço do novo empregado:\n")
        category = Util.validChoice(category, 3, Util.employeeType)
        paymentMethod = Util.validChoice(paymentMethod, 3, Util.paymentMethod)
        
        while isInSyndicate not in [True, False]:
            isInSyndicate = input("Pertence ao sindicato? [S/n]\n").upper()
            
            if isInSyndicate == "S":
                isInSyndicate = True
                monthlyFee = float(input("Insira o valor da taxa mensal cobrada pelo sindicato: R$"))
            elif isInSyndicate == "N":
                isInSyndicate = False
            else:
                print("Resposta inválida")
                sleep(1)

        newEmployee = EmployeeFactory.createEmployee(category, name, address, Company.genId(), paymentMethod, isInSyndicate, monthlyFee)
        
        if newEmployee.isInSyndicate:
            Syndicate.addEmployee(newEmployee, newEmployee.fee, Syndicate.genSyndId(), isInSyndicate)
        
        Company.addEmployee(newEmployee)
        memento.caretaker.manage()
        print("Empregado adicionado com sucesso!")
    @staticmethod
    def delEmployee():
        Company.printTable()
        id = int(input("Informe o ID do funcionário que deseja remover\n"))
        if Company.isInCompany(id):
            Company.removeEmployee(id)
            memento.caretaker.manage()
            print("Empregado removido com sucesso!")
    @staticmethod
    def punchIn():
        Company.printHourlyTable()
        id = int(input("Por gentileza, informe seu ID\n"))
        if Company.isInCompany(id) and Util.isInstance(Company.getEmployee(id), Hourly):
            WorkedHours.punchIn(id)
            memento.caretaker.manage()
    @staticmethod
    def postSale():
        Company.printCommissionedTable()
        id = int(input("Informe o ID do funcionário\n"))
        employee = Company.getEmployee(id)
        if Company.isInCompany(id) and Util.isInstance(employee, Commissioned):
            employee.postSale()

    @staticmethod
    def addServiceFee():
        Syndicate.printTable()
        syndId = int(input("Informe o ID do funcionário no sindicato\n"))
        Syndicate.addServiceFee(syndId)
        memento.caretaker.manage()

    @staticmethod
    def payroll():
        option = ""
        option = Util.validChoice(option, 3, Util.payroll)
        if option != 3:
            Payroll.pay() if option == 1 else Payroll.paydayTable()
            sleep(1)
    @staticmethod
    def schedules():
        option = ""
        option = Util.validChoice(option, 3, Util.schedules)
        if option != 3:
            Payroll.selectSchedule() if option == 1 else Payroll.addSchedule()
            sleep(1)
    @staticmethod
    def undo():
        memento.caretaker.undo()
    @staticmethod
    def redo():
        memento.caretaker.redo()
    @staticmethod
    def quit():
        print("Até mais :)")

    @staticmethod
    def updateSyndInfo(employee, option):
        {
        6: lambda: Syndicate.updateSyndId(employee),
        7: lambda: Syndicate.updateMonthlyFee(employee)
        }.get(option)()
        if employee.isInSyndicate:
            memento.caretaker.manage()
            print("Operação realizada com sucesso!")
    
    @staticmethod
    def updateInfo(employee, option):
        {
        1: lambda: EmployeeFactory.updateCategory(employee),
        2: employee.updateName,
        3: employee.updateAddress,
        4: employee.updatePaymentMethod,
        5: lambda: Syndicate.updateSyndStatus(employee)
        }.get(option)()
        memento.caretaker.manage()
        print("Operação realizada com sucesso!")
    
    @classmethod
    def updateEmployee(cls):
        Company.printCompleteTable()
        id = int(input("Informe o ID do funcionário\n"))
        
        if Company.isInCompany(id):
            option = ""
            option = Util.validChoice(option, 8, Util.editEmployee)
            employee = Company.getEmployee(id)

            if option != 8:
                if option <= 5:
                    cls.updateInfo(employee, option)
                else:
                    cls.updateSyndInfo(employee, option)
                sleep(1)
    
    @classmethod
    def employeeMenu(cls):
        option = ""
        option = Util.validChoice(option, 5, Util.employeeMenu)
        if option != 5:
            {
            1: cls.addEmployee,
            2: cls.delEmployee,
            3: cls.updateEmployee,
            4: Company.printTable
            }.get(option)()
            if option != 3: sleep(1)
    
    @classmethod
    def workedHoursMenu(cls):
        option = ""
        option = Util.validChoice(option, 2, Util.workedHours)
        {
            1: cls.punchIn,
            2: WorkedHours.printTable
        }.get(option)()
    
    @classmethod
    def generalMenu(cls, option):
        {
            1: cls.employeeMenu,
            2: cls.workedHoursMenu,
            3: cls.postSale,
            4: cls.addServiceFee,
            5: cls.payroll,
            6: cls.schedules,
            7: cls.undo,
            8: cls.redo,
            9: cls.quit,
        }.get(option)()

    @staticmethod
    def greetings():
        now = datetime.now().hour
        if now >= 6 and now < 12:
            print(">>>> Bom dia,", end="")
        elif now >= 12 and now < 18:
            print(">>>> Boa tarde,", end="")
        else:
            print(">>>> Boa noite,", end="")
        print(" seja bem-vindo(a) ao sistema de Folha de Pagamento <<<<\n")
        sleep(1)
    
    @classmethod
    def menu(cls):
        Menu.greetings()
        memento.caretaker.manage()
        choice = ""
        while choice != 9:
            choice = ""
            choice = Util.validChoice(choice, 9, Util.menu)
            cls.generalMenu(choice)
            if choice != 1 and choice != 5 and choice != 6 and choice != 9: sleep(1)

if __name__ == "__main__":
    Menu.menu()
