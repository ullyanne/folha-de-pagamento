from abc import ABC, abstractmethod
import calendar
from datetime import date, timedelta

class Schedule(ABC):
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
    
    def isPayday(self):
        if date.today() == self.payday:
            return True

    @abstractmethod
    def calc():
        pass

class LastDay(Schedule):
    @staticmethod
    def monthDays(today):
        return calendar.monthrange(today.year, today.month)[1]
    
    @staticmethod
    def lastDayOfMonth(today, monthDays):
        return today + timedelta(days=monthDays - today.day)
    
    @staticmethod
    def previousBusinessDay(payday):
        return payday - timedelta(payday.weekday() - 4)

    @staticmethod
    def notBusinessDay(payday):
        if payday.weekday() == 5 or payday.weekday() == 6:
            return True
    
    def calc(self):
        today = date.today() + timedelta(days=1)
        payday = self.lastDayOfMonth(today, self.monthDays(today))

        if self.notBusinessDay(payday):
            payday = self.previousBusinessDay(payday)

        return payday

class Monthly(Schedule):
    def dateNextMonth(self, today):
        return date(today.year, today.month+1, self.desiredDay)
    
    def calc(self):
        today = date.today()
        payday = self.dateNextMonth(today)
        return payday

class Weekly(Schedule):
    def weekdayNextWeek(self, today):
        return today + timedelta((self.desiredDay - today.weekday())%7 + 7)
    
    def calc(self):
        today = date.today()
        payday = self.weekdayNextWeek(today)
        return payday

class Biweekly(Schedule):
    def weekdayNextTwoWeeks(self, today):
        return today + timedelta((self.desiredDay - today.weekday())%7 + 14)
    
    def calc(self):
        today = date.today()
        payday = self.weekdayNextTwoWeeks(today)
        return payday