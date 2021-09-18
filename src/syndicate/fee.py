from datetime import date

class Fee:
    def __init__(self, monthlyFee=0):
        self._monthlyFee = monthlyFee
        self._serviceFee = []
        self._lastPaymentMonth = None
    
    def reset(self):
        self._monthlyFee = 0
        self._serviceFee = []
        self._lastPaymentMonth = None
    
    @property
    def monthlyFee(self):
        return self._monthlyFee
    
    @monthlyFee.setter
    def monthlyFee(self, monthlyFee):
        self._monthlyFee = monthlyFee
    
    @property
    def serviceFee(self):
        return sum(self._serviceFee)
    
    @serviceFee.setter
    def serviceFee(self, serviceFee):
        self._serviceFee.append(serviceFee)
    
    @property
    def lastPaymentMonth(self):
        return self._lastPaymentMonth
    
    @lastPaymentMonth.setter
    def lastPaymentMonth(self, month):
        self._lastPaymentMonth = month
    
    def subtract(self, isInSyndicate):
        fees = 0
        if isInSyndicate and self.lastPaymentMonth != date.today().month:
            fees = self.monthlyFee + self.serviceFee
            self.lastPaymentMonth = date.today().month
        return fees
