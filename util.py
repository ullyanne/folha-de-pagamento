import textwrap, time

class Util:
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
                            [7] - Taxa mensal\n""")

    def errorMessage():
        print("Opção inválida")

    def validChoice(choice, options, message):
        while choice not in list(range(1, options+1)):
                print(message, end = "")
                choice = int(input())
                if choice not in list(range(1, options+1)):
                    Util.errorMessage()
                    time.sleep(1)
        return choice