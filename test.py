# with open('test.txt', 'r+b') as file:
#     file.seek(14, 0)
#     file.write(b'afnsl')
#     file.close()

import os
from item import ItemProperties

with open('1.DRS', 'rb') as file:
    file.seek(0, 2)
    print(file.tell())



