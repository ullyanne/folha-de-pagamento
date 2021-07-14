import time, datetime, textwrap
from employee import Employee, Commissioned
from workedHours import WorkedHours
from company import Company
from syndicate import Syndicate

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
            category = ""
            paymentMethod = ""
            monthlyFee = ""
            isInSyndicate = None

            name = input("Insira o nome do novo empregado:\n")
            address = input("Insira o endereço do novo empregado:\n")
            id = Company.genId()

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
                    monthlyFee = int(input("Insira o valor da taxa mensal cobrada pelo sindicato:\n"))
                elif isInSyndicate == "N":
                    isInSyndicate = False
                else:
                    print("Resposta inválida")
                    time.sleep(1)
            newEmployee = Employee.create(category, name, address, id, paymentMethod, isInSyndicate)

            if newEmployee.isInSyndicate:
                syndId = Syndicate.genSyndId()
                Syndicate.addEmployee(newEmployee, monthlyFee, syndId, True, 0)
            
            Company.addEmployee(newEmployee)
            print("Empregado adicionado com sucesso!")
        elif choice == "2":
            Company.printTable()
            id = int(input("Informe o ID do funcionário que deseja remover\n"))

            try:
                Company.removeEmployee(id)
                print("Empregado removido com sucesso!")
            except:
                print("Funcionário não encontrado")
            time.sleep(1)

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
            Syndicate.addServiceFee()
        elif choice == "6":
            Employee.printTable()
            id = int(input("Informe o ID do funcionário\n"))
    
            if id in Company.employees:
                option = ""

                while option not in ["1", "2", "3", "4", "5", "6", "7"]:
                    option = input(textwrap.dedent("""\
                        Qual dado deseja alterar?
                            [1] - Categoria
                            [2] - Nome
                            [3] - Endereço
                            [4] - Método de pagamento
                            [5] - Status no sindicato
                            [6] - ID no sindicato
                            [7] - Taxa mensal\n"""))
                    
                    if option not in ["1", "2", "3", "4", "5", "6", "7"]:
                        print("Opção inválida")
                        time.sleep(1)
                Employee.edit(Company.employees[id], option)
            else:
                print("Funcionário não encontrado")
        elif choice == "7":
            Company.printTable()
        
        if choice!= "8" : time.sleep(1)
        
    print("Até mais :)")

menu()
