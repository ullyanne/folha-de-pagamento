from datetime import date

class Fee:
    def __init__(self):
        self.monthlyFee = 0
        self.serviceFee = []
        self.lastPaymentMonth = None
    def subtract(employee):
        if employee.isInSyndicate and employee.fee.lastPaymentMonth != date.today().month:
            employee.salary = employee.salary - employee.fee.monthlyFee - sum(employee.fee.serviceFee)
            employee.fee.lastPaymentMonth = date.today().month