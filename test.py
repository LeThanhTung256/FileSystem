import uuid
import hashlib
from utilities import hashPass, isPass

h = hashPass('1111')
print(isPass('1111', h))

