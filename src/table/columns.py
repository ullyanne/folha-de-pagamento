from abc import ABC, abstractmethod

class Columns(ABC):
    @staticmethod
    def columns():
        return "\n╎ Categoria    ╎ ID ╎ Nome " + " " * 15 + "╎ Endereço " + 7* " " + "╎"

    @staticmethod
    def border(spaces):
        return "└" + spaces*"╌" + "┘"

    @abstractmethod
    def getSpaces():
        pass

    @classmethod
    def display(cls):
        print(cls.columns())
        print(cls.border(cls.getSpaces()))
    
class EmployeesColumns(Columns):    
    @staticmethod
    def getSpaces():
        return 59

class CommissionedColumns(Columns):
    @classmethod
    def columns(cls):
        return super().columns() + " Comissão ╎" + " Vendas ╎"
    
    @staticmethod
    def getSpaces():
        return 79

class EmployeesPlusColumns(Columns):
    @classmethod
    def columns(cls):
        return super().columns() + " Método de Pagamento" + 8*" " + "╎ Sindicato ╎ ╎ ID Sindicato ╎ ╎ Taxa Mensal ╎"
    
    @staticmethod
    def getSpaces():
        return 133
    
class SyndicateColumns(Columns):
    @classmethod
    def columns(cls):
        return super().columns() + " ID Sindicato ╎"
    
    @staticmethod
    def getSpaces():
        return 74
    
class PaymentStatusColumns(Columns):
    @classmethod
    def columns(cls):
        return super().columns() + " Status do pagamento" + 39*" " + "╎"
    
    @staticmethod
    def getSpaces():
        return 119

class PaydayColumns(Columns):
    @classmethod
    def columns(cls):
        return super().columns() + " Data de Pagamento ╎ Método de Pagamento" + 8*" " + "╎"
    
    @staticmethod
    def getSpaces():
        return 108
    
class WorkedHoursColumns(Columns):
    @classmethod
    def columns(cls):
        return super().columns() + " Horas trabalhadas ╎" + " Horas extras ╎"
    
    @staticmethod
    def getSpaces():
        return 94
    
