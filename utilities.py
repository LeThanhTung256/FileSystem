import uuid
import hashlib

import constants

# Kiểm tra một chuỗi có phải là một số thực k
def isNumber(str):
    try:
        float(str)
        return True
    except:
        return False

# Hash password bằng sha512 thêm salt
def hashPass(password: str):
    salt = uuid.uuid4().bytes # Random mạng 16 byte
    # Return 1 mảng 80 bytes
    return hashlib.sha512(password.encode() + salt).digest() + salt

# Hàm kiểm tra pass
def isPass(password: str, passhash):
    salt = passhash[64:]
    return passhash == hashlib.sha512(password.encode() + salt).digest() + salt

# Hàm tạo một bản ghi cho 1 sector(512) với một mảng bytes
def createSector(data: bytes):
    size = len(data)
    return data + bytes(constants.ByPerSec - size)

# Lấy vị trí entry trống trong sector của RDET
def emptyEntry(sector):
    maxEntry = constants.ByPerSec / constants.ByPerEntry - 1
    index = 0
    while index <= maxEntry:
        firstByteOfEntry = sector[index * constants.ByPerEntry]
        if firstByteOfEntry.to_bytes(1, 'little') == bytes(1):
            return index
        index += 1
    return None

# Tìm vị trí entry bị xoá trong sector của DRET
def deletedEntry(sector):
    maxEntry = constants.ByPerSec / constants.ByPerEntry - 1
    index = 0
    while index <= maxEntry:
        firstByteOfEntry = sector[index * constants.ByPerEntry]
        if firstByteOfEntry.to_bytes(1, 'little') == constants.ByteDelete:
            return index
        index += 1
    return None
    
