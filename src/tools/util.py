import textwrap
from time import sleep

class Util:
    employeeMenu = textwrap.dedent("""\
                                    Selecione uma opção abaixo:
                                        [1] - Adicionar um empregado
                                        [2] - Remover um empregado
                                        [3] - Alterar detalhes de um empregado
                                        [4] - Listar os empregados cadastrados
                                        [5] - Retornar\n""")
    menu = textwrap.dedent("""\
                                ==========================================
                                O que deseja fazer, hoje?
                                    [1] - Gerenciar empregados
                                    [2] - Lançar um cartão de ponto
                                    [3] - Lançar um resultado de venda
                                    [4] - Lançar uma taxa de serviço
                                    [5] - Folha de pagamento
                                    [6] - Agendas de pagamento
                                    [7] - Desfazer ação
                                    [8] - Refazer ação
                                    [9] - Sair\n""")
    employeeType = textwrap.dedent("""\
                                        Insira o tipo do novo empregado:
                                            [1] - Horista
                                            [2] - Assalariado
                                            [3] - Comissionado\n""")
    newEmpType = textwrap.dedent("""\
                                        Escolha a nova categoria:
                                            [1] - Horista
                                            [2] - Assalariado
                                            [3] - Comissionado\n""")
    paymentMethod = textwrap.dedent("""\
                                        Qual é o método de pagamento desejado?
                                            [1] - Cheque pelos correios
                                            [2] - Cheque em mãos
                                            [3] - Depósito em conta bancária\n""")
    newPaymentMethod = textwrap.dedent("""\
                                            Escolha o novo método de pagamento
                                                [1] - Cheque pelos correios
                                                [2] - Cheque em mãos
                                                [3] - Depósito em conta bancária\n""")
    workedHours = textwrap.dedent("""\
                            Escolha uma opção abaixo:
                                [1] - Bater ponto
                                [2] - Listar cartão de ponto de hoje\n""")
    editEmployee = textwrap.dedent("""\
                        Qual dado deseja alterar?
                            [1] - Categoria
                            [2] - Nome
                            [3] - Endereço
                            [4] - Método de pagamento
                            [5] - Status no sindicato
                            [6] - ID no sindicato
                            [7] - Taxa mensal
                            [8] - Retornar\n""")
    payroll = textwrap.dedent("""\
                        Escolha uma opção abaixo:
                            [1] Rodar folha de pagamento
                            [2] Listar próximos pagamentos
                            [3] Retornar\n""")
    schedules = textwrap.dedent("""\
                                Escolha uma opção abaixo:
                                    [1] Selecionar agenda de pagamento
                                    [2] Criar agenda de pagamento
                                    [3] Retornar\n""")
    newSchedules = textwrap.dedent("""\
                        Especifique a nova agenda a ser criada
                        Sintaxe:    mensal [dia]; semanal [1/2] [dia da semana]
                        Exemplos:   mensal 7 -> pagamentos no dia 7 de todo mês
                                    semanal 1 quinta -> pagamentos toda semana às quintas
                                    semanal 2 terça -> pagamentos a cada 2 semanas às terças\n""")
    
    @staticmethod
    def errorMessage():
        print("Opção inválida")
    
    @staticmethod
    def validIntChoice(choice):
        try:
            choice = int(choice)
            return choice
        except:
            pass
    
    @staticmethod
    def validChoice(choice, options, message):
        while choice not in list(range(1, options+1)):
                print(message, end = "")
                choice = input()
                choice = Util.validIntChoice(choice)
                if choice not in list(range(1, options+1)):
                    Util.errorMessage()
                    sleep(1)
        return choice

    def isInstance(employee, type):
        if isinstance(employee, type):
            return True
        return print("Operação não permitida")