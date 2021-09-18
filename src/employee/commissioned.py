import datetime
from .salaried import Salaried
from ..tools import Settings as memento

class Commissioned(Salaried):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, monthlyFee, fixedSalary, commissionPercent):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate, monthlyFee, fixedSalary)
        self._fixedSalary = float(fixedSalary)
        self._commissionPercent = float(commissionPercent)
        self._sales = 0
    
    @property
    def commissionPercent(self):
        return self._commissionPercent
    @commissionPercent.setter
    def commissionPercent(self, commissionPercent):
        self._commissionPercent = commissionPercent
    
    @property
    def sales(self):
        return self._sales
    @sales.setter
    def sales(self, sales):
        self._sales = sales
    
    def halfFixedSalary(self):
        return self.fixedSalary/2
    
    def calcCommission(self):
        return self.commissionPercent/100 * self.sales

    def calcSalary(self):
        self.salary = self.halfFixedSalary() + self.calcCommission() - self.subtractFees()
        self.resetSales()

    def resetSales(self):
        self.sales = 0

    def postSale(self):
        date = str(input("Insira a data de venda no seguinte formato: AAAA-MM-DD\n"))
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        except:
            print("Formato inválido")
            return
        
        self.sales = float(input("Insira o valor da venda: R$"))
        memento.caretaker.manage()
        print("Venda lançada com sucesso!")