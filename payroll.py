from company import Company
from datetime import date, timedelta
import calendar
# import os
# os.system('cls||clear')
class Payroll:
    paymentMethod = {
        1: "Cheque pelos correios",
        2: "Cheque em mãos",
        3: "Depósito em conta bancária"
    }

    def weekly(desiredDay=4):
        today = date.today()
        paymentDay = today + timedelta(desiredDay - today.weekday() + 7)
        return paymentDay
    
    def lastDay():
        today = date.today()
        paymentDay = calendar.monthrange(today.year, today.month)[1]
        paymentDay = today + timedelta(days=paymentDay - today.day)

        if paymentDay.weekday() == 5 or paymentDay.weekday() == 6:
            paymentDay = paymentDay - timedelta(paymentDay.weekday() - 4)

        return paymentDay

    def biweekly(desiredDay=4):
        today = date.today()
        paymentDay = today + timedelta(desiredDay - today.weekday() + 14)
        return paymentDay

    def monthly(desiredDay):
        today = date.today()
        paymentDay = date(today.year, today.month+1, desiredDay)
        return paymentDay

    schedule = {
        1: weekly,
        2: lastDay,
        3: biweekly,
        4: monthly
    }

    def paymentTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Data de Pagamento ╎ Método de Pagamento        ╎")
        print("└" + 108*"╌" + "┘")
        for employee in Company.employees.values():
            print(employee, end ="")
            print(str(employee.payday) + (8 * " ") + "╎", end=" ")
            print(Payroll.paymentMethod[employee.paymentMethod] + (27 - len(Payroll.paymentMethod[employee.paymentMethod]))* " " + "╎")
        print("\n")
    def pay():
        paymentToday = 0
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Status do pagamento" + 39*" " + "╎")
        print("└" + 119*"╌" + "┘")
        for employee in Company.employees.values():
            if employee.payday == date.today():
                employee.calcSalary()
                if employee.salary > 0:
                    paymentToday = 1
                    print(employee, end ="")
                    status = f"{Payroll.paymentMethod[employee.paymentMethod]} enviado no valor de R${employee.salary:.2f}"
                    print(status + (58-(len(status))) * " " + "╎")
                    employee.salary = 0
        print("\n")
        if paymentToday == 0:
            print("Nenhum funcionário a ser pago hoje\n")

