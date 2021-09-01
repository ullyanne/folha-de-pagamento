from company import Company
from workedHours import WorkedHours
from syndicate import Syndicate
from copy import deepcopy

class Originator():
    def __init__(self):
        self._state = []

    def createState(self):
        self._state = []
        company, workedhours, syndicate = deepcopy((Company.employees, WorkedHours.entries, Syndicate.employees))
        self._state.append(company)
        self._state.append(workedhours)
        self._state.append(syndicate)
    
    def save(self):
        return Memento(self._state)

    def restore(self, memento):
        self._state = memento.state
        company, workedhours, syndicate = deepcopy((self._state[0], self._state[1], self._state[2]))
        Company.employees = company
        WorkedHours.entries = workedhours
        Syndicate.employees = syndicate
        print("Operação realizada com sucesso!")

class Memento():
    def __init__(self, state):
        self._state = state

    @property
    def state(self):
        return self._state

class Caretaker():
    def __init__(self, originator):
        self._mementos = []
        self._redo = []
        self._originator = originator

    def backup(self):
        if len(self._mementos) == 11:
            self._mementos.pop(0)
        self._mementos.append(self._originator.save())

    def manage(self):
        self._redo = []
        self.backup()
        self._originator.createState()

    def undo(self):
        if not len(self._mementos):
            return print("Nenhuma ação a ser desfeita!")

        currentState = self._originator.save()
        self._redo.append(currentState)

        memento = self._mementos.pop()
        try:
            self._originator.restore(memento)
        except:
            self.undo()
    
    def redo(self):
        if not len(self._redo):
            return print("Nenhuma ação a ser refeita!")
        self._mementos.append(self._originator.save())
        self._originator.restore(self._redo.pop())
        self._originator.createState()

class Settings():
    originator = Originator()
    caretaker = Caretaker(originator)