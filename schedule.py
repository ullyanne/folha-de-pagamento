import calendar
from datetime import date, timedelta

class Schedule:
    def __init__(self, desiredDay):
        self.desiredDay = desiredDay
        self.payday = self.calc()
    def setPayday(self):
        self.payday = self.calc()
class LastDay(Schedule):
    def calc(self):
        today = date.today()
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
        if today.weekday() > self.desiredDay:
            payday = today + timedelta((today.weekday() + self.desiredDay)%6 + 7)
        else:
            payday = today + timedelta(self.desiredDay - today.weekday() + 7)
        return payday
class Biweekly(Schedule):
    def calc(self):
        today = date.today()
        today.weekday() 
        if today.weekday() > self.desiredDay:
            payday = today + timedelta((today.weekday() + self.desiredDay)%6 + 14)
        else:
            payday = today + timedelta(self.desiredDay - today.weekday() + 14)
            print(payday)
        return payday