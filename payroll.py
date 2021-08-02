from datetime import date
from schedule import Biweekly, LastDay, Monthly, Weekly
from util import Util
from company import Company
import time, textwrap

class Payroll:
    paymentMethod = {
        1: "Cheque pelos correios",
        2: "Cheque em mãos",
        3: "Depósito em conta bancária"
    }

    currentSchedules = 3
    schedule = {
        1: LastDay,
        2: Weekly(4),
        3: Biweekly(4)
    }
    displaySchedule = ["Mensal", "Semanal", "Bi-semanal"]
    weekdays = {
        "segunda": 0, "terça": 1, "quarta": 2, "quinta": 3, "sexta": 4
    }

    def selectSchedule():
        Company.printTable()
        time.sleep(1)
        id = int(input("Por gentileza, informe seu ID\n"))
        employee = Company.searchEmployee(id)
        if employee == False:
            return
        
        selectMessage = "Selecione uma das agendas abaixo:\n"
        for count, schedule in enumerate(Payroll.displaySchedule):
            selectMessage = selectMessage + f"    [{count+1}] - {schedule}\n"
        
        choice = ""
        choice = Util.validChoice(choice, Payroll.currentSchedules, selectMessage)
        employee.setSchedule(Payroll.schedule.get(choice))
        print("Agenda selecionada com sucesso!")
    def addSchedule():
        newSchedule = input(textwrap.dedent("""\
                        Especifique a nova agenda a ser criada
                        Exemplos:   mensal 7 -> pagamentos no dia 7 de todo mês
                                    semanal 1 quinta -> pagamentos toda semana às quintas
                                    semanal 2 terça -> pagamentos a cada 2 semanas às terças\n"""))
        newSchedule = newSchedule.lower().split()
        Payroll.currentSchedules = Payroll.currentSchedules + 1
        
        if newSchedule[0] == "mensal":
            Payroll.schedule[Payroll.currentSchedules] = Monthly(int(newSchedule[1]))
        elif newSchedule[0] == "semanal":
            if(newSchedule[2] == "sabado" or newSchedule[2] == "sábado" or newSchedule[2] == "domingo"):
                Payroll.currentSchedules = Payroll.currentSchedules - 1
                return print("Apenas são aceitos dias de semana")
            if newSchedule[1] == "1":
                Payroll.schedule[Payroll.currentSchedules] = Weekly(Payroll.weekdays[newSchedule[2]])
            elif newSchedule[1] == "2":
                Payroll.schedule[Payroll.currentSchedules] = Biweekly(Payroll.weekdays[newSchedule[2]])
        Payroll.displaySchedule.append(" ".join(newSchedule).lower())
        print("Agenda adicionada com sucesso!")
    def paymentTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Data de Pagamento ╎ Método de Pagamento        ╎")
        print("└" + 108*"╌" + "┘")
        for employee in Company.employees.values():
            print(employee, end ="")
            print(str(employee.schedule.payday) + (8 * " ") + "╎", end=" ")
            print(Payroll.paymentMethod[employee.paymentMethod] + (27 - len(Payroll.paymentMethod[employee.paymentMethod]))* " " + "╎")
        print("\n")
    def pay():
        paymentToday = 0
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Status do pagamento" + 39*" " + "╎")
        print("└" + 119*"╌" + "┘")
        for employee in Company.employees.values():
            if employee.schedule.payday == date.today():
                employee.calcSalary()
                employee.schedule.setPayday()
                if employee.salary > 0:
                    paymentToday = 1
                    print(employee, end ="")
                    status = f"{Payroll.paymentMethod[employee.paymentMethod]} enviado no valor de R${employee.salary:.2f}"
                    print(status + (58-(len(status))) * " " + "╎")
                    employee.salary = 0
        print("\n")
        if paymentToday == 0:
            print("Nenhum funcionário a ser pago hoje\n")

