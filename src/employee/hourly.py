from .employee import Employee

class Hourly(Employee):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, monthlyFee, wage):
        super().__init__(name, address, category, id, paymentMethod, schedule, isInSyndicate, monthlyFee)
        self._wage = float(wage)
        self.workStatus = {"entry": None, "exit": None, "total hours": 0, "extra hours": 0}
    
    @property
    def wage(self):
        return self._wage
    @wage.setter
    def wage(self, wage):
        self._wage = wage
    
    def wageSalary(self):
        return self.wage * self.workStatus["total hours"]

    def bonusSalary(self):
        return 1.5 * self.wage * self.workStatus["extra hours"]

    def calcSalary(self):
        self.salary = self.wageSalary() + self.bonusSalary() - self.subtractFees()
        self.resetWorkingHours()

    def getWorkdayHours(self):
        return (self.workStatus["exit"] - self.workStatus["entry"]).total_seconds()/3600
    
    def getWorkdayExtraHours(self):
        return self.getWorkdayHours() - 8 if (self.getWorkdayHours() - 8) > 0 else 0

    def setWorkdayExtraHours(self):
        self.workStatus["extra hours"] = self.workStatus["extra hours"] + self.getWorkdayExtraHours()
    
    def setTotalHours(self):
        self.workStatus["total hours"] = self.workStatus["total hours"] + self.getWorkdayHours() - self.getWorkdayExtraHours()

    def resetEntryHour(self):
        self.workStatus["entry"] = None
    
    def resetWorkingHours(self):
        self.workStatus["total hours"] = 0
        self.workStatus["extra hours"] = 0
    
    def setExitHour(self, currentHour):
        self.workStatus["exit"] = currentHour
    
    def setEntryHour(self, currentHour):
        self.workStatus["entry"] = currentHour
    
    def getEntryHour(self):
        return self.workStatus["entry"]