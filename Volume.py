# Sc: Số sector trên 1 cluster (default = 1)
# Sb: Số sector của vùng boot sector (default = 1)
# Nf: Số lượng bảng FAT (default = 2)
# Sf: Số sector của mỗi bảng FAT (default = 32)
# Sd: Số Entry của bảng DRET (default = 512 (32 sector))
# Sv: Số sector của volume (default = 0.5GB = 1048576 sector)

import constants
from utilities import hashPass, isPass, createSector

class Volume:
    __Sb = constants.Sb, # Số sector của boot sector (1 sector)
    __Nf = constants.Nf, # Số lượng bảng FAT (2)
    __Sf = constants.Sf, # Số lượng sector của mỗi bảng FAT (32)
    __Sd = constants.Sb, # Số lượng entry của bảng DRET (512 entry = 32 sector)

    #  Khởi tạo một My File System
    def __new__(cls, password, name=None, sc=None, size=None, filepath=None):
        if filepath == None:
            return object().__new__(cls)
        else:
            with open(filepath, 'rb') as file:
                bootSector = file.read(constants.ByPerSec)
                file.close()
            passHash = bootSector[5: 85]
            if isPass(password, passHash):
                return object().__new__(cls)
            else:
                raise TypeError("Wrong password")

    def __init__(self, password, name=None, sc=None, size=None, filepath=None):
        if filepath == None:
            self.__Name = name
            self.__Sc = sc
            self.__Sv = int(size * (2*10) * 3 / constants.ByPerSec)
            passHash = hashPass(password)
            self.__Password = passHash
        else:
            with open(filepath, 'rb') as file:
                bootSector = file.read(constants.ByPerSec)
                file.close()
            self.__Sc = int.from_bytes(bootSector[0:1], 'little')
            self.__Sv = int.from_bytes(bootSector[1:5], 'little')
            self.__Password = bootSector[5:85]
            self.__Name = filepath
            

    # Hàm lưu Volume khi khởi tạo
    def create(self):
        with open(self.__Name + '.DRS', 'wb') as file:
        # Lưu boot Sector (1 byte(Sc) + 4 bytes(Sv) + 80 bytes(password))
            data = self.__Sc.to_bytes(1, 'little') + self.__Sv.to_bytes(4, 'little') + self.__Password
            bootSector = createSector(data)
            file.write(bootSector)
            file.close()
    
    def __str__(self):
        return f'''
            Sc = {self.__Sc}
            Sv = {self.__Sv}
            Name = {self.__Name}
            Password = {self.__Password}
        '''

    