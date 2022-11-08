import uuid
import hashlib
from utilities import hashPass, isPass

class test:
    __pow = None

    def __new__(cls, a=None, b=None ):
        if a != None or b != None:
            return object().__new__(cls)
        else:
            raise TypeError("Sai rồi")
    
    def __init__(self, a=None, b=None):
        if a != None:
            self.__pow = int(a) + 2
        else:
            self.__pow = int(b)**2
            
    
    def __str__(self) -> str:
        return f'{self.__pow}'

a = test(b = 8)
print(a)


