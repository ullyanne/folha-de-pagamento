from datetime import date
from memento import Settings as memento
from time import sleep
from schedule import Biweekly, LastDay, Monthly, Weekly
from util import Util
from company import Company
import textwrap

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
        
        if id not in Company.employees:
            return print("Funcionário não encontrado")

        employee = Company.employees[id]
        selectMessage = "Selecione uma das agendas abaixo:\n"
        for count, schedule in enumerate(Payroll.displaySchedule):
            selectMessage = selectMessage + f"    [{count+1}] - {schedule}\n"
        
        choice = ""
        choice = Util.validChoice(choice, Payroll.currentSchedules, selectMessage)
        employee.schedule = Payroll.schedule.get(choice)
        print("Agenda selecionada com sucesso!")
    
    @classmethod
    def addSchedule(cls):
        newSchedule = input(textwrap.dedent("""\
                        Especifique a nova agenda a ser criada
                        Sintaxe:    mensal [dia]; semanal [1/2] [dia da semana]
                        Exemplos:   mensal 7 -> pagamentos no dia 7 de todo mês
                                    semanal 1 quinta -> pagamentos toda semana às quintas
                                    semanal 2 terça -> pagamentos a cada 2 semanas às terças\n"""))
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
    def paymentTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Data de Pagamento ╎ Método de Pagamento        ╎")
        print("└" + 108*"╌" + "┘")
        for employee in Company.employees.values():
            print(employee, end ="")
            print(str(employee.schedule.payday) + (8 * " ") + "╎", end=" ")
            print(Company.paymentMethod[employee.paymentMethod] + (27 - len(Company.paymentMethod[employee.paymentMethod]))* " " + "╎")
        print("\n")
    
    @staticmethod
    def pay():
        paymentToday = 0
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Status do pagamento" + 39*" " + "╎")
        print("└" + 119*"╌" + "┘")
        for employee in Company.employees.values():
            
            if employee.schedule.payday == date.today():
                memento.caretaker.manage()
                employee.calcSalary()
                employee.schedule.payday = employee.schedule.calc()
                
                if employee.salary:
                    paymentToday = 1
                    print(employee, end ="")
                    status = f"{Company.paymentMethod[employee.paymentMethod]} enviado no valor de R${employee.salary:.2f}"
                    print(status + (58-(len(status))) * " " + "╎")
                    employee.salary = 0
        print("\n", end="")
        if not paymentToday:
            print("Nenhum funcionário a ser pago hoje\n")

