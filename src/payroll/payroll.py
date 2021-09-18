from time import sleep
from ..table import Rows
from ..table import PaydayColumns, PaymentStatusColumns
from ..tools import Settings as memento
from ..tools import Util
from .schedule import Biweekly, LastDay, Monthly, Weekly
from ..company import Company

class Payroll:
    schedule = {
        1: LastDay(None),
        2: Weekly(4),
        3: Biweekly(4)
    }
    currentSchedules = 3
    displaySchedule = ["Mensal", "Semanal", "Bi-semanal"]
    weekdays = {
        "segunda": 0, "terça": 1, "quarta": 2, "quinta": 3, "sexta": 4
    }

    @staticmethod
    def selectSchedule():
        Company.printTable()
        sleep(1)
        id = int(input("Por gentileza, informe seu ID\n"))
        
        if Company.isInCompany(id):
            employee = Company.getEmployee(id)
            selectMessage = "Selecione uma das agendas abaixo:\n"
            for count, schedule in enumerate(Payroll.displaySchedule):
                selectMessage = selectMessage + f"    [{count+1}] - {schedule}\n"
            
            choice = ""
            choice = Util.validChoice(choice, Payroll.currentSchedules, selectMessage)
            employee.schedule = Payroll.schedule.get(choice)
            print("Agenda selecionada com sucesso!")
    
    @classmethod
    def addSchedule(cls):
        newSchedule = input(Util.newSchedules)
        newSchedule = newSchedule.lower().split()
        cls.currentSchedules = cls.currentSchedules + 1
        
        try:
            if newSchedule[0] == "mensal":
                cls.schedule[cls.currentSchedules] = Monthly(int(newSchedule[1]))
            elif newSchedule[0] == "semanal":
                if(newSchedule[2] == "sabado" or newSchedule[2] == "sábado" or newSchedule[2] == "domingo"):
                    cls.currentSchedules = cls.currentSchedules - 1
                    return print("Apenas são aceitos dias de semana")
                if newSchedule[1] == "1":
                    cls.schedule[cls.currentSchedules] = Weekly(cls.weekdays[newSchedule[2]])
                elif newSchedule[1] == "2":
                    cls.schedule[cls.currentSchedules] = Biweekly(cls.weekdays[newSchedule[2]])
                else:
                    cls.currentSchedules = cls.currentSchedules - 1
                    return print(f"Argumento {newSchedule[1]} não aceito")
        except:
            cls.currentSchedules = cls.currentSchedules - 1
            return print("A quantidade de argumentos fornecida não é suficiente para criar a agenda")
        cls.displaySchedule.append(" ".join(newSchedule).capitalize())
        print("Agenda adicionada com sucesso!")
    
    @staticmethod
    def paydayTable():
        PaydayColumns.display()
        Rows.displayPayday(Company.employees.values(), Company.paymentMethod)

    @staticmethod
    def pay():
        paymentToday = False
        PaymentStatusColumns.display()
        for employee in Company.employees.values():
            if employee.schedule.isPayday():
                memento.caretaker.manage()
                employee.calcSalary()
                employee.newPayday()
                if employee.salary:
                    paymentToday = True
                    Rows.displayPaymentStatus(employee, Company.paymentMethod)
                    employee.salary = 0
        print("\n", end="")
        if not paymentToday:
            print("Nenhum funcionário a ser pago hoje\n")

