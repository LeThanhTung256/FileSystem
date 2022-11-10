# Sc: Số sector trên 1 cluster (default = 1)
# Sb: Số sector của vùng boot sector (default = 1)
# Nf: Số lượng bảng FAT (default = 2)
# Sf: Số sector của mỗi bảng FAT (default = 32)
# Sd: Số Entry của bảng DRET (default = 512 (32 sector))
# Sv: Số sector của volume (default = 0.5GB = 1048576 sector)
import math

import constants
from utilities import hashPass, isPass, createSector, emptyEntry, deletedEntry
from item import ItemProperties, Item
class Volume:
    __Sb:int = constants.Sb # Số sector của boot sector (1 sector)
    __Nf:int = constants.Nf # Số lượng bảng FAT (2)
    __Sf:int = constants.Sf # Số lượng sector của mỗi bảng FAT (32)
    __Sd:int = constants.Sd # Số lượng entry của bảng DRET (512 entry = 32 sector)

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
            self.__Sv = int(size * pow(pow(2, 10), 3) / constants.ByPerSec)
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

            # Lưu bảng Fat (empty)
            sectorsOfRDET = int(self.__Sd * constants.ByPerEntry / constants.ByPerSec)
            # Số cluster của phần data = số secter / số sector trên cluster
            clustersOfData = int((self.__Sv - self.__Sb - self.__Nf * self.__Sf - sectorsOfRDET) / self.__Sc)
            for i in range(0, self.__Nf):
                useableBytesFAT = int(clustersOfData * 2)
                for j in range(0, self.__Sf):
                    if useableBytesFAT > constants.ByPerSec:
                        emptySector = bytes(constants.ByPerSec)
                        file.write(emptySector)
                        useableBytesFAT -= constants.ByPerSec
                    else:
                        emptyPoi = bytes(useableBytesFAT)
                        unuseable = bytes.fromhex('ff') * (constants.ByPerSec - useableBytesFAT)
                        sector = emptyPoi + unuseable
                        file.write(sector)
                        useableBytesFAT = 0
 
            # Lưu bảng thư mục gốc
            for i in range(0, sectorsOfRDET):
                emptySector = bytes(constants.ByPerSec)
                file.write(emptySector)

            file.close()

    # Hàm import file từ ngoài vào volume
    def importFile(self, fileInput: str):
        # Tìm entry trống trong RDET, nếu không sẽ trả về lỗi
        sectorEntry, indexEntry = self.__findEmptyEntryInRDET() if None not in self.__findEmptyEntryInRDET() else self.__findDeleteEntryInRDET()
        if None in (sectorEntry, indexEntry):
            raise TypeError('RDET is full')
        
        # Tìm kích thức tập tin input theo bytes
        with open(fileInput, 'rb') as file:
            file.seek(0, 2) # Đưa con trỏ về vị trí cuối file
            sizeOfFile = file.tell() # Đọc vị trí con trỏ
            file.seek(0, 0) # Đưa con trỏ về lại vị trí đầu file
        
        # Tìm vị trí các cluster trong bảng fat để lưu file nếu không có thì return lỗi
        numberOfClusters = math.ceil(sizeOfFile / (constants.ByPerSec * self.__Sc))
        clusters = self.__findEmptyClusters(numberOfClusters)
        if len(clusters) < numberOfClusters:
            raise TypeError("Volume is full")
        
        firstClus = int(self.__indexCluster(clusters[0])).to_bytes(4, 'little')

        fileFullName = fileInput.split('/')[-1]
        if fileFullName.find('.') == -1:
            fileName, tag = fileFullName, ''
        else:
            fileName, tag = fileFullName.split('.')

        # Phần tên chính lưu trong 8 bytes đầu
        fileNameBytes = bytes(fileName, 'utf-8')
        size = len(fileNameBytes)
        fileNameBytes += bytes.fromhex('20') * abs(8 - size)
        fileNameBytes = fileNameBytes[0:8]
        # Phần tên phụ lưu trong 3 bytes tiếp
        tagBytes = bytes(tag,'utf-8')
        size = len(tagBytes)
        tagBytes += bytes.fromhex('20') * abs(3 - size)
        tagBytes = tagBytes[0:3]

        # Thuộc tính tập tin, lưu trong 1 byte tiếp theo
        properties = ItemProperties().hex() 
        # 8 bytes tiếp lưu thông tin về thời gian, chưa làm
        tmp1 = bytes(8)
        # 2 bytes lưu cluster bắt đầu (phần word cao)
        staCluster1 = firstClus[2:]
        # 4 bytes tiếp lưu thông tin về thời gian, chưa làm
        tmp2 = bytes(4)
        # 2 bytes lưu cluster bắt đầu (phần word thấp)
        staCluster2 = firstClus[0:2]

        # 4 bytes cuối lưu kích thước phần nội dung tập tin
        sizeOfFile = sizeOfFile.to_bytes(4, 'little')
        
        # Tạo entry
        ent = fileNameBytes + tagBytes + properties + tmp1 + staCluster1 + tmp2 + staCluster2 + sizeOfFile
        
        # Ghi kết quả vào volume
        # - Ghi vào FAT
        self.__writeClustersIntoFAT(clusters)
        # - Ghi entry vào bảng thư mục gốc
        self.__writeEntryIntoRDET(ent, (sectorEntry, indexEntry))
        # - Ghi data
        self.__writeData(fileInput, clusters)

    # Tìm trong bảng fat cluster đang trống với số lượng cho trước
    def __findEmptyClusters(self, numberOfClusters: int):
        firstSecterOfFAT = self.__Sb
        lastSectorOfFAT = self.__Sb + self.__Sf - 1
        index = firstSecterOfFAT
        cluster = []
        while (index <= lastSectorOfFAT) and (len(cluster) < numberOfClusters):
            sector = self.__readSector(index)
            position = 0
            while (position <= constants.ByPerSec / 2 - 1) and (len(cluster) < numberOfClusters):
                if int.from_bytes(sector[position * 2: position * 2 + 2], 'little') == 0:
                    # Trừ cluster 0 và 1
                    if (index != firstSecterOfFAT) or (position not in (0, 1)):
                        cluster.append((index, position))
                position += 1
            index += 1
        return cluster

    # Tìm vị trí entry trống trong RDET
    def __findEmptyEntryInRDET(self):
        firstSectorRDET = self.__Sb + self.__Nf * self.__Sf
        lastSectorRDET = firstSectorRDET + self.__Sd * constants.ByPerEntry / constants.ByPerSec - 1
        index = firstSectorRDET
        while index <= lastSectorRDET:
            sector = self.__readSector(index)
            empty = emptyEntry(sector)
            if empty != None:
                return index, empty
            index += 1
        return None, None
    
    # Tìm vị trí entry bị xoá trong RDET
    def __findDeleteEntryInRDET(self):
        firstSectorRDET = self.__Sb + self.__Nf * self.__Sf
        lastSectorRDET = firstSectorRDET + self.__Sd * constants.ByPerEntry / constants.ByPerSec - 1
        index = firstSectorRDET
        while index <= lastSectorRDET:
            sector = self.__readSector(index)
            deleted = deletedEntry(sector)
            if deleted != None:
                return index, deleted
            index += 1 
        return None, None

    # Đọc sector theo index
    def __readSector(self, index):
        with open(self.__Name, 'rb') as vol:
            position = int(index * constants.ByPerSec)
            vol.seek(position, 0)
            sector = vol.read(constants.ByPerSec)
            vol.close()
            return sector

    # Đọc theo cluster theo index
    def __readBlock(self, index):
        # Tính vị trí byte đầu tiên của phần data
        firstBlockPosition = (self.__Sb + self.__Nf * self.__Sf + self.__Sd) * constants.ByPerSec
        position = firstBlockPosition + index * self.__Sc * constants.ByPerSec
        with open(self.__Name, 'rb') as vol:
            vol.seek(position, 0)
            cluster = vol.read(self.__Sc * constants.ByPerSec)
            vol.close()
            return cluster

    # Ghi sector theo index
    def __writeSector(self, index, sector):
        with open(self.__Name, 'r+b') as vol:
            position = index * constants.ByPerSec
            vol.seek(position, 0)
            vol.write(sector)
            vol.close()

    # Ghi cluster theo index
    def __writeBlock(self, index, cluster):
        firstBlockPosition = int(self.__Sb + self.__Nf * self.__Sf + self.__Sd) * constants.ByPerSec
        position = int(firstBlockPosition + index * self.__Sc * constants.ByPerSec)
        with open(self.__Name, 'r+b') as vol:
            vol.seek(position, 0)
            vol.write(cluster)
            vol.close()

    # Tính cluster bắt đầu từ vị trí sector của bảng fat và vị trí của nó
    def __indexCluster(self, clus) -> int:
        indexSec = clus[0] - self.__Sb
        index = indexSec * (constants.ByPerSec / 2) + clus[1]
        return index

    # Ghi mảng cluster vào bảng FAT
    def __writeClustersIntoFAT(self, clusters):
        for i in range(0, len(clusters)):
            if i != len(clusters) - 1:
                index = int(self.__indexCluster(clusters[i+1])).to_bytes(2, 'little')
            else:
                index = bytes.fromhex('ff') * 2
            sector = self.__readSector(clusters[i][0])
            newSector = sector[0:clusters[i][1] * 2] + index + sector[clusters[i][1] * 2 + 2 :]
            self.__writeSector(clusters[i][0], newSector)
            self.__writeSector(clusters[i][0] + self.__Sf, newSector)

    def __readIndexFAT(self, index):
        numberPositionInSector = constants.ByPerSec / 2
        sectorIndex = int(index // numberPositionInSector)
        position = int(index % numberPositionInSector)
        sector = self.__readSector(sectorIndex + self.__Sb)
        itemFAT = sector[position * 2: (position + 1) * 2]
        if itemFAT == bytes.fromhex('ff') * 2:
            return -1
        else:
            return int.from_bytes(itemFAT, 'little')

    # Ghi entry vào bảng thư mục gốc
    def __writeEntryIntoRDET(self, entry, poi):
        sector = self.__readSector(poi[0])
        newsector = sector[0: poi[1] * constants.ByPerEntry] + entry + sector[(poi[1] + 1) * constants.ByPerEntry:]
        self.__writeSector(poi[0], newsector)

    # Ghi file vào data
    def __writeData(self, fileIn, clusters):
        with open(fileIn, 'rb') as file:
            for i in clusters:
                if i != clusters[-1]:
                    data = file.read(self.__Sc * constants.ByPerSec)
                    index = self.__indexCluster(i)
                    self.__writeBlock(index, data)
                else:
                    data = file.read()
                    size = len(data)
                    addData = bytes.fromhex('')*(self.__Sc * constants.ByPerSec - size)
                    data += addData
                    index = self.__indexCluster(i)
                    self.__writeBlock(index, data)

    # Đọc thuộc tính của entry
    def __readPropertiesEntry(self, entry: bytes) -> Item:
        name = str(entry[0:8], 'utf-8').rstrip()
        tag = str(entry[8: 11], 'utf-8').rstrip()
        if tag != '':
            name = name + '.' + tag
        
        properties = ItemProperties(entry[11])
        firClus1 = entry[20:22]
        firClus2 = entry[26:28]
        frirstClus = int.from_bytes((firClus2 + firClus1), 'little')
        size = int.from_bytes(entry[28:], 'little')

        item = Item(name = name, type=properties, beginCluster=frirstClus, size = size,)
        return item

    # ReadEntryRDET
    def readEntrys(self):
        firstSectorRDET = self.__Sb + self.__Nf * self.__Sf
        entryPerSector = math.ceil(constants.ByPerSec / constants.ByPerEntry)
        numberSectorsRDET = math.ceil(self.__Sd / entryPerSector)
        items = []
        for i in range(0, numberSectorsRDET):
            sector = self.__readSector(firstSectorRDET + i)
            for j in range(0, entryPerSector):
                entry = sector[j * constants.ByPerEntry: (j + 1) * constants.ByPerEntry]
                if entry[0] not in (0, int.from_bytes(constants.ByteDelete, 'little')):
                    item = self.__readPropertiesEntry(entry)
                    items.append(item)
        return items
    
    # Export file 
    def exportFile(self, file: Item, filepath: str = ''):
        indexCluster = file.beginCluster
        data = self.__readBlock(indexCluster)
        while indexCluster != -1:
            indexCluster = self.__readIndexFAT(indexCluster)
            data = data + self.__readBlock(indexCluster)
        
        with open(filepath + file.name, 'wb') as file:
            file.write(data.rstrip(bytes.fromhex('00')))
            file.close()
        
                
