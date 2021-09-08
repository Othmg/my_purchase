
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(order=True)
class ISConstructor(ABC):
    #def __init__(self,amnt, time):
    amnt : float
    time : float
    cat : str


@dataclass(order=True,frozen = True)
class BSConstructor(ABC):
    #def __init__(self,amnt, time):
    amnt : float
    time : float
    cat : str


@dataclass(order=True)
class RevAcc(ISConstructor):
    def __init__(self, amnt, time, cat):
        super().__init__(amnt, time,cat)


@dataclass(order=True)
class ExpAcc(ISConstructor):
    def __init__(self, amnt, time,cat):
        super().__init__(amnt, time,cat)


@dataclass(order=True,frozen = True)
class CashAcc(BSConstructor):
    def __init__(self, amnt, time, cat):
        super().__init__(amnt, time,cat)


@dataclass(order=True,frozen = True)
class InvAcc(BSConstructor):
    def __init__(self, amnt, time, cat):
        super().__init__(amnt, time,cat)


@dataclass(order=True, frozen = True)
class LoanAcc(BSConstructor):
    def __init__(self, amnt, time, cat):
        super().__init__(amnt, time,cat)






