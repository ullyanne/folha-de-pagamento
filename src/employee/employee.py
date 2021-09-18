from abc import ABC, abstractmethod
from ..tools import Util
from ..syndicate import Fee

class Employee(ABC):
    def __init__(self, name, address, category, id, paymentMethod, schedule, isInSyndicate, monthlyFee):
        self._name = name
        self._address = address
        self._category = category
        self._id = id
        self._paymentMethod = paymentMethod
        self._schedule = schedule
        self._isInSyndicate = isInSyndicate
        self._syndId = " "
        self._salary = 0
        self._fee = Fee(monthlyFee)
    
    def __str__(self):
        return("╎ " + self._category + " " *(13-len(self._category)) + "╎ " + str(self._id) + " " * (2-len(str(self._id)))
                + " ╎ " + self._name + " " * (19-len(self._name)) + " ╎ " 
                + self._address + " " * (15-len(self._address)) + " ╎ ")
    
    @abstractmethod
    def calcSalary(self):
        pass

    @property
    def name(self):
        return self._name
    def updateName(self):
        newName = input("Insira o novo nome\n")
        self._name = newName
    
    @property
    def address(self):
        return self._address
    def updateAddress(self):
        newAddress = input("Insira o novo endereço\n")
        self._address = newAddress
    
    @property
    def id(self):
        return self._id
    
    @property
    def paymentMethod(self):
        return self._paymentMethod
    def updatePaymentMethod(self):
        paymentMethod = ""
        self._paymentMethod = Util.validChoice(paymentMethod, 3, Util.newPaymentMethod)
    
    @property
    def salary(self):
        return self._salary
    @salary.setter
    def salary(self, salary):
        if salary > 0:
            self._salary = salary

    @property
    def category(self):
        return self._category

    @property
    def isInSyndicate(self):
        return self._isInSyndicate
    @isInSyndicate.setter
    def isInSyndicate(self, isInSyndicate):
        self._isInSyndicate = isInSyndicate

    @property
    def syndId(self):
        return self._syndId
    @syndId.setter
    def syndId(self, syndId):
        self._syndId = syndId
    
    @property
    def fee(self):
        return self._fee
    @fee.setter
    def fee(self, fee):
        self._fee = fee
    
    @property
    def schedule(self):
        return self._schedule
    @schedule.setter
    def schedule(self, schedule):
        self._schedule = schedule

    def newPayday(self):
        self.schedule.payday = self.schedule.calc()
    
    def subtractFees(self):
        return self.fee.subtract(self.isInSyndicate)