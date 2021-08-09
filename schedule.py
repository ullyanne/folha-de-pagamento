import calendar
from datetime import date, timedelta

class Schedule:
    def __init__(self, desiredDay):
        self._desiredDay = desiredDay
        self._payday = self.calc()
    
    @property
    def desiredDay(self):
        return self._desiredDay
    
    @property
    def payday(self):
        return self._payday
    @payday.setter
    def payday(self, payday):
        self._payday = payday
class LastDay(Schedule):
    @staticmethod
    def calc():
        today = date.today() + timedelta(days=1)
        
        payday = calendar.monthrange(today.year, today.month)[1]
        payday = today + timedelta(days=payday - today.day)

        if payday.weekday() == 5 or payday.weekday() == 6:
            payday = payday - timedelta(payday.weekday() - 4)

        return payday
class Monthly(Schedule):
    def calc(self):
        today = date.today()
        payday = date(today.year, today.month+1, self.desiredDay)
        return payday
class Weekly(Schedule):
    def calc(self):
        today = date.today()
        payday = today + timedelta((self.desiredDay - today.weekday())%7 + 7)
        return payday
class Biweekly(Schedule):
    def calc(self):
        today = date.today()
        today.weekday() 
        payday = today + timedelta((self.desiredDay - today.weekday())%7 + 14)
        return payday