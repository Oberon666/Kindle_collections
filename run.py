import os, platform, hashlib, json, shutil

disk = str()
#------------------------------------------------------
class collection:
    def __init__(self, path):
        self.nameCollection = os.path.basename(path)
        self.pathCollection = path
        self.hashBookList = list()
        self.searchBooks(self.pathCollection)

    def searchBooks(self, path):
        for file in os.listdir(path):
            if os.path.isdir(os.path.join(path, file)):
                self.searchBooks(os.path.join(path, file))
            else:
                _, extension = os.path.splitext(file)
                if extension in self.formats:
                    self.hashBookList.append(self.createHash(str(os.path.join('/mnt/us/documents', self.nameCollection, file)).replace("\\","/")))

    def createHash(self, _fileName):
        myHash = hashlib.sha1()
        myHash.update(_fileName.encode())
        return('*' + myHash.hexdigest())

    formats = ['.mobi', '.pdf', '.azw3', '.rtf']
    nameCollection = str()
    pathCollection = str()
    hashBookList = list()
#------------------------------------------------------
def initDir():
    global disk
    if platform.system() == 'Linux':
        disk = os.path.join('/media', 'Kindle') # default.
    elif platform.system() == 'Windows':
        disk = 'h' + ':\\' # default.
    return str(os.path.join(disk, 'documents'))
#------------------------------------------------------
def addCollectionList(_dirToBook):
    if not os.path.exists(_dirToBook):
        raise 'not valid path _dirToBook'
    collectionList = list()
    for folder in os.listdir(_dirToBook):
        folderWithPatch = os.path.join(_dirToBook, folder)
        if os.path.isdir(folderWithPatch):
           collectionList.append(collection(folderWithPatch))
    return collectionList
#------------------------------------------------------
def writeFile(_collectionList):
    fullData = dict()
    for collection in _collectionList:
        dataDict = dict()
        dataDict['items'] = collection.hashBookList
        dataDict['lastAccess'] = 1414779993
        collectionData = '[' + collection.nameCollection + ']@ru-RU' # @en-EN
        fullData[collectionData] = dataDict
    systemDir = os.path.join(disk, 'system')
    with open(os.path.join(systemDir, 'collections.json'), 'w', encoding='utf-8') as file:
        file.write(json.dumps(fullData))
#------------------------------------------------------
def main():
    collectionList = addCollectionList(initDir())
    writeFile(collectionList)
#------------------------------------------------------
if __name__ == '__main__':
    main()
