# Folha de Pagamento
Sistema de Folha de Pagamento em Python para a disciplina de Projeto de Software

O objetivo do projeto é construir um sistema de folha de pagamento. O sistema consiste do
gerenciamento de pagamentos dos empregados de uma empresa. Além disso, o sistema deve
gerenciar os dados destes empregados, a exemplo os cartões de pontos. Empregados devem receber
o salário no momento correto, usando o método que eles preferem, obedecendo várias taxas e
impostos deduzidos do salário.

## Install
```sh
sudo apt-get install python3
```

## Run
```sh
git clone https://github.com/ullyanne/folha-de-pagamento.git
cd folha-de-pagamento
python run.py
```
## Design pattern
- Extract Method
- [Factory Method](src/employee/employeeFactory.py)
- [Memento](src/tools/memento.py)
- Move Method
- Replace Temp With Query
- Template Method

## Code Smells

- **Duplicate Code** 

    :pencil: Uso da mesma estrutura de tabela em diversas classes

    `employee.py`:
    ```py
    def printTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎")
        print("└" + 59*"╌" + "┘")
        ...
    ```

    `payroll.py`:
    ```py
    def paymentTable():
        print("\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎ Data de Pagamento ╎ Método de Pagamento        ╎")
        print("└" + 108*"╌" + "┘")
        ...
    ```

    :pushpin: Solução: [Template Method](src/table/columns.py)
    
    ---

    :pencil: Múltiplas ocorrências de checagem de funcionário e, caso não encontrado no sistema, exibição de mensagem de erro

    `run.py`:
    ```py
    def updateEmployee():
        ...
        if id not in Company.employees:
            return print("Funcionário não encontrado")
        ...
    ```

    `payroll.py`:
    ```py
    def selectSchedule():
        ...
        if id not in Company.employees:
            return print("Funcionário não encontrado")
        ...
    ```

    :pushpin: Solução: [Extract Method](https://github.com/ullyanne/folha-de-pagamento/blob/693c2a85e46f4cdaa9545683317747019864b5ea/src/company.py#L21)


***

- **Feature Envy**

    :pencil: As informações do funcionário eram acessadas constantemente, em vez de métodos da instância serem invocados
    
    `workedHours.py`:
    ```py
    def punchIn():
        ...
        employee.workStatus["exit"] = currentHour
        hours = (employee.workStatus["exit"] - employee.workStatus["entry"]).total_seconds()/3600
        extraHours = 0

        if hours > 8:
            extraHours = hours - 8
            employee.workStatus["extra hours"] = employee.workStatus["extra hours"] + extraHours
        
        employee.workStatus["total hours"] = employee.workStatus["total hours"] + hours - extraHours
        employee.workStatus["entry"] = None
    ```

    :pushpin: Solução: [Move Method](https://github.com/ullyanne/folha-de-pagamento/blob/693c2a85e46f4cdaa9545683317747019864b5ea/src/workedHours.py#L23)

    ```py
    def punchIn():
        employee.setExitHour(cls.currentHour())
        employee.setWorkdayExtraHours()
        employee.setTotalHours()
        employee.resetEntryHour()
    ```

***

- **If Statements**

    :pencil: Ifs em excesso

    `run.py`:
    ```py
    def workedHours():
        ...
        if option == 1:
            ...
            if id in Company.employees:
                employee = Company.employees[id]
                if employee.category != "Horista":
                    return print("Operação não permitida")
            else:
                return print("Funcionário não encontrado")
            WorkedHours.punchIn(id)
            memento.caretaker.manage()
        else:
            WorkedHours.printTable()
    ```

    :pushpin: Solução: [Dispatch Table](https://github.com/ullyanne/folha-de-pagamento/blob/693c2a85e46f4cdaa9545683317747019864b5ea/run.py#L147)
    ```py
    def workedHoursMenu():
        ...
        {
            1: cls.punchIn,
            2: WorkedHours.printTable
        }.get(option)()
    
    def punchIn():
        ...
        if Company.isInCompany(id) and Util.isInstance(Company.getEmployee(id), Hourly):
            WorkedHours.punchIn(id)
            memento.caretaker.manage()
    ```

***

- **Long Method**
    
    :pencil: Expressões extensas e de difícil compreensão

    `schedule.py`:
    ```py
    def calc():
    today = date.today() + timedelta(days=1)
    
    payday = calendar.monthrange(today.year, today.month)[1]
    payday = today + timedelta(days=payday - today.day)

    if payday.weekday() == 5 or payday.weekday() == 6:
        payday = payday - timedelta(payday.weekday() - 4)

    return payday
    ``` 

    `schedule.py`:
    ```py
    def calc():
        today = date.today()
        today.weekday() 
        payday = today + timedelta((self.desiredDay - today.weekday())%7 + 14)
        return payday
    ``` 
    
    `workedHours.py`:
    ```py
    def punchIn():
        currentHour = datetime.datetime.now()
        if ...:
            employee.workStatus["entry"] = currentHour
            ...
        else:
            employee.workStatus["exit"] = currentHour
            hours = (employee.workStatus["exit"] - employee.workStatus["entry"]).total_seconds()/3600
            extraHours = 0
            if hours > 8:
                extraHours = hours - 8
                employee.workStatus["extra hours"] = employee.workStatus["extra hours"] + extraHours
        ...
    ```

    `employee.py`:

    ```py
    def calcSalary():
        self.salary = self.wage * self.workStatus["total hours"] + (1.5 * self.wage * self.workStatus["extra hours"]) - self.fee.subtract(self.isInSyndicate)
        self.workStatus["total hours"] = 0
        self.workStatus["extra hours"] = 0
    ```

    :pushpin: Solução: Extract Method

    [`schedule.py:`]()
    ```py
    def calc():
        today = date.today() + timedelta(days=1)
        payday = self.lastDayOfMonth(today, self.monthDays(today))

        if self.notBusinessDay(payday):
            payday = self.previousBusinessDay(payday)

        return payday
    ```

    [`schedule.py:`]()
    ```py
    def calc():
        today = date.today()
        payday = self.weekdayNextWeek(today)
        return payday
    ```

    :pushpin: Solução: Replace Temp With Query

    [`workedHours.py`:]()
    ```py
    def punchIn():
        ...
        if ...:
                cls.addEntry(employee, cls.currentHour())
        else:
            employee.setExitHour(cls.currentHour())
            employee.setWorkdayExtraHours()
            ...
    ```
    
    [`workedHours.py`:]()
    ```py
    def currentHour():
        return datetime.datetime.now()
    ```

    [`hourly.py`:]()
    ```py
    def getWorkdayExtraHours():
        return self.getWorkdayHours() - 8 if (self.getWorkdayHours() - 8) > 0 else 0
    ```

    [`hourly.py`:]()
    ```py
    def calcSalary():
        self.salary = self.wageSalary() + self.bonusSalary() - self.subtractFees()
        self.resetWorkingHours()
    ```


## Functions
|   Função   |  Título  |    Descrição    | Status |
|    :---:   |  :---:   |      :---:      |  :---: |
|1| Adição de um empregado| Um novo empregado é adicionado ao sistema. Os seguintes atributos são fornecidos: nome, endereço, tipo (hourly, salaried, commissioned) e os atributos associados (salário horário, salário mensal, comissão). Um número de empregado (único) deve ser escolhido automaticamente pelo sistema.| :white_check_mark: |
|2| Remoção de um empregado| Um empregado é removido do sistema.| :white_check_mark: |
|3| Lançar um Cartão de Ponto| O sistema anotará a informação do cartão de ponto e a associará ao empregado correto.| :white_check_mark: |
|4| Lançar um Resultado de Venda| O sistema anotará a informação do resultado da venda e a associará ao empregado correto.| :white_check_mark: |
|5| Lançar uma taxa de serviço|O sistema anotará a informação da taxa de serviço e a associará ao empregado correto.| :white_check_mark: |
|6| Alterar detalhes de um empregado| Os seguintes atributos de um empregado podem ser alterados: nome, endereço, tipo (hourly, salaried, commisioned), método de pagamento, se pertence ao sindicato ou não, identificação no sindicato, taxa sindical. | :white_check_mark: |
|7| Listar os empregados cadastrados \[extra] | O sistema listará todos os empregados cadastrados. | :white_check_mark: |
|8| Rodar a folha de pagamento para hoje | O sistema deve achar todos os empregados que devem ser pagos no dia indicado, deve calcular o valor do salário e deve providenciar o pagamento de acordo com o método escolhido pelo empregado. | :white_check_mark: |
|9| Undo/redo | Qualquer transação associada as funcionalidades 1 a 8 (exceto a extra) deve ser desfeita (undo) ou refeita (redo). | :white_check_mark: |
|10| Agenda de pagamento | Cada empregado é pago de acordo com uma "agenda de pagamento". Empregados podem selecionar a agenda de pagamento que desejam. Por default, as agendas "semanalmente", "mensalmente" e "bi-semanalmente" são usadas, como explicado na descrição geral. | :white_check_mark: |
|11| Criação de Novas Agendas de Pagamento | A direção da empresa pode criar uma nova agenda de pagamento e disponibilizá-la para os empregados escolherem, se assim desejarem. Uma agenda é especificada através de um string. Alguns exemplos mostram as possibilidades: "mensal 1": dia 1 de todo mês, "mensal 7": dia 7 de todo mês, "mensal $": último dia útil de todo mês, "semanal 1 segunda": toda semana às segundas-feiras, "semanal 1 sexta": toda semana às sextas-feiras, "semanal 2 segunda": a cada 2 semanas às segundas-feiras. | :white_check_mark: |
## :mag::woman_technologist: 
Para mais informações, [confira](Folha_de_Pagamento.pdf) o documento completo do projeto.