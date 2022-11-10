# Chứa thông tin thư mục/ tập tin
from enum import Enum
from typing import List

class TypeItem(Enum):
    FOLDER = 'folder'
    FILE = "file"

class ItemProperties:
    def __init__(
        self,
        readOnly: bool = False,
        hidden: bool = False,
        system: bool = False,
        volLabel: bool = False,
        directory: bool = False,
        hex: bytes = None
        ):
        if hex == None:
            self.__readOnly = readOnly
            self.__hidden = hidden
            self.__system = system
            self.__volLabel = volLabel
            self.__directory = directory
            self.__archive = False if self.__directory else True
        else:
            values = int.from_bytes(hex, 'little')
            self.__archive = bool(values // pow(2, 5))
            values = values % pow(2, 5)

            self.__directory = bool(values // pow(2, 4))
            values = values % pow(2, 4)

            self.__volLabel = bool(values // pow(2, 3))
            values = values % pow(2, 3)

            self.__system = bool(values // pow(2, 2))
            values = values % pow(2, 2)

            self.__hidden = bool(values // 2)
            values = values % 2
            self.__readOnly = bool(values)
            
    def __str__(self):
        return f'''
        readOnly: {self.__readOnly}
        hidden: {self.__hidden}
        system: {self.__system}
        volLabel: {self.__volLabel}
        directory: {self.__directory}
        archive: {self.__archive}
        '''

    def hex(self):
        tmp = 0
        tmp += int(self.__readOnly)
        tmp += int(self.__hidden) * 2
        tmp += int(self.__system) * pow(2, 2)
        tmp += int(self.__volLabel) * pow(2, 3)
        tmp += int(self.__directory) * pow(2, 4)
        tmp += int(self.__archive) * pow(2, 5)
        return tmp.to_bytes(1, 'little')

class Item:
    def __init__(self, type: ItemProperties, beginCluster: int, name: str, size: int, path: str = '', children: List = None):
        self.type = type
        self.name = name
        self.path = path
        self.beginCluster = beginCluster
        self.children = children
        self.size = size
    
    def __str__(self):
        return f'{self.name}'
      