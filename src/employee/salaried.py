from .employee import Employee

class Salaried(Employee):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, monthlyFee, fixedSalary):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate, monthlyFee)
        self._fixedSalary = float(fixedSalary)
    
    @property
    def fixedSalary(self):
        return self._fixedSalary
    @fixedSalary.setter
    def fixedSalary(self, fixedSalary):
        self._fixedSalary = fixedSalary

    def calcSalary(self):
        self.salary = self.fixedSalary - self.subtractFees()
