from MyFS import MyFileSystem
from Volume import Volume as Vol

def main():
    myFS = MyFileSystem()
    myFS.start()
    # vol = Vol(password='1', filepath='12.DRS')
    # vol.importFile('fileImport.txt')
    # items = vol.readEntrys()
    # vol.exportFile(items[-1])

if __name__ == "__main__":
    main()