from time import sleep

class Rows():
    def displayEmployees(employees):
        for employee in employees:
            print(employee)
        print("\n", end="")
    
    def displayEmployeesPlus(employees, paymentMethod):
        for employee in employees:
            print(employee, end = "")
            print(paymentMethod[employee.paymentMethod] + (27 - len(paymentMethod[employee.paymentMethod]))* " " + "╎", end = "")
            print(" Ativo     ", end="") if employee.isInSyndicate == True else print(" Inativo   ", end = "")
            print("╎ ╎ " + str(employee.syndId) + (13 - len(str(employee.syndId)))* " " + "╎ ", end = "")
            print("╎ " + str(employee.fee.monthlyFee) + (12 - len(str(employee.fee.monthlyFee)))* " " + "╎")
        print("\n")
        sleep(1)

    def displayHourly(employees):
        for employee in employees:
            if employee.category == "Horista" : print(employee)

        print("\n", end="")
    
    def displayCommissioned(employees):
        for employee in employees:
            if employee.category == "Comissionado":
                print(employee, end="")
                commission = str(employee.commissionPercent)
                sales = str(employee.sales)
                print(commission + "%" + (8 - len(commission))* " " + "╎", end=" ")
                print(sales + (7 - len(sales)) * " " + "╎")
        print("\n")
        sleep(1)

    def displaySyndicate(employees):
        for employee in employees:
            print(employee, end="")
            syndId = str(employee.syndId)
            print(syndId + (13 - len(syndId))* " " + "╎")
        print("\n")
        sleep(1)
    
    def displayPaymentStatus(employee, paymentMethod):
        print(employee, end ="")
        status = f"{paymentMethod[employee.paymentMethod]} enviado no valor de R${employee.salary:.2f}"
        print(status + (58-(len(status))) * " " + "╎")

    def displayPayday(employees, paymentMethod):
        for employee in employees:
            print(employee, end ="")
            print(str(employee.schedule.payday) + (8 * " ") + "╎", end=" ")
            print(paymentMethod[employee.paymentMethod] + (27 - len(paymentMethod[employee.paymentMethod]))* " " + "╎")
        print("\n")

    def displayWorkedHours(entries):
        for entry in entries:
            print(entry, end="")
            totalHours = entry.workStatus["total hours"] + entry.workStatus["extra hours"]
            if entry.workStatus["entry"] != None:
                print("Em serviço" + 23* " " + "╎")
            else: 
                print(int(totalHours), end="")
                print((18 - len(str(int(totalHours))))* " " + "╎", end=" ")
                print(int(entry.workStatus["extra hours"]), end="")
                print((13 - len(str(int(entry.workStatus["extra hours"]))))* " " + "╎")
        print("\n", end="")