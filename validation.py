from abc import ABC, abstractmethod

item_options = ['car','house', 'holiday']

class Validate(ABC):
    """
    returns boolean.
    """
    def __init__(self,input):
        self.input = input

    @abstractmethod
    def validating(self)->bool:
        pass

    def validated(self)->bool:
        if self.validating():
            return self.input
        else:
            raise TypeError


class ValueValidator(Validate):
    def __init__(self, input):
        super().__init__(input)

    def validating(self) -> bool:
        if not isinstance(self.input, (float,int)):
            raise TypeError('Invalid Type Entered, float or integer type Expected')
        elif self.input < 0:
            raise TypeError('Invalid Value Entered, positive value Expected')
        else:
            return True

    @property
    def validated(self) -> bool:
        return super().validated()


class ItemValidator(Validate):
    def __init__(self, input):
        super().__init__(input)

    def validating(self) -> bool:
        if not isinstance(self.input, str):
            raise TypeError('Invalid Type Entered, str type Expected')
        elif self.input.lower() not in item_options:
            raise TypeError('Invalid input, choose between car,house,holiday')
        else:
            return True

    @property
    def validated(self) -> bool:
        return super().validated() 


class TimeValidator(Validate):
    def __init__(self, input):
        super().__init__(input)

    def validating(self) -> bool:
        if not isinstance(self.input, (float,int)):
            raise TypeError('Invalid Type Entered, float type Expected')
        elif self.input < 0:
            raise TypeError('Invalid Value Entered, positive value Expected')
        else:
            return True

    @property
    def validated(self) -> bool:
        return super().validated()


class RateValidator(Validate):
    def __init__(self, input):
        super().__init__(input)

    def validating(self) -> bool:
        if not isinstance(self.input, (float,int)):
            raise TypeError('Invalid Type Entered, float type Expected')
        elif self.input < 0:
            raise TypeError('Invalid Value Entered, positive value Expected')
        elif self.input >1:
            raise TypeError('Invalid Value, <1 value Expected')
        else:
            return True

    @property
    def validated(self) -> bool:
        return super().validated()





