from random import randint

class Company:
    employees = {}

    def genId():
        id = 0
        while id in Company.employees:
            id = randint(0, 99)
        return id

    def addEmployee(new):
        Company.employees[new.id] = new
    
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎")
        print("└" + 59*"╌" + "┘")
        for employee in Company.employees.values():
            print(employee)
        print("\n")

    def removeEmployee(id):
        del Company.employees[id]
    
    def searchEmployee(id):
        try:
            employee = Company.employees[id]
            return employee
        except:
            print("Funcionário não encontrado")
            return False

