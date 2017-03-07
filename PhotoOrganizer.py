__author__ = "João Correia"
import os
from datetime import datetime
import sys,shutil
import threading
import time

class File(object):
    def __init__(self, dirName, fileName):
        self.dirName = dirName
        self.fileName = fileName
        self.creationDate = os.path.getctime(os.path.join(dirName,fileName))
        self.year = datetime.fromtimestamp(self.creationDate).year
        self.month = datetime.fromtimestamp(self.creationDate).month
        self.day = datetime.fromtimestamp(self.creationDate).day

    def __lt__(self, other):
        return self.creationDate < other.creationDate

def copyFiles(origin, destination):
    with open(origin,"rb") as file:
        b = file.read()
    file.close()
    file = None
    with open(destination,"wb") as file:
        file.write(b)
    file.close()

def timeTook(begin, end):
    print("Took %s seconds to copy files" % str((end - begin).seconds))

def getFiles(inputPath):
    outFileList = list()
    for file in os.listdir(inputPath):
        f = os.path.join(inputPath,file)
        if os.path.isfile(f):
            outFileList.append(File(inputPath,f.split(os.sep)[-1]))
    return outFileList

def createpath(ipath):
    opath = ""
    for p in ipath.split(os.sep):
        opath = opath + p + os.sep
        if not os.path.exists(opath):
            os.mkdir(opath)

if __name__ == "__main__":
    begin = datetime.now()
    print("Started at: %s" % begin.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        thread = []
        inputPath = None
        outputPath = None
        if len(sys.argv) is 5:
            if sys.argv[1] == "-i" or sys.argv[1] == "-o":
                if sys.argv[1] == "-i":
                    inputPath = sys.argv[2]
                    if sys.argv[3] == "-o":
                        outputPath = sys.argv[4]
                elif sys.argv[1] == "-o":
                    outputPath = sys.argv[2]
                    if sys.argv[3] == "-i":
                        inputPath = sys.argv[4]

            if os.path.exists(outputPath):
                shutil.rmtree(outputPath)

            #time.sleep(2)

            os.mkdir(outputPath)

            outFileList = getFiles(inputPath)
            for f in outFileList:
                if not os.path.exists(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)), str(f.day))):
                    createpath(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)), str(f.day)))
                destination = os.path.join(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)), str(f.day)), f.fileName)
                thread.append(threading.Thread(target=copyFiles,args=(os.path.join(inputPath,f.fileName), destination, ), name=destination))

            for i in range(len(thread)):
                thread[i].start()
                print(thread[i].name)
                thread[i].join()

        else:
            raise Exception("Wrong number of arguments.\nThe correct format is <programName> -i <input dir> -o <output dir>")
    except Exception as ex:
        print("ex %s" % (ex.args[0]))

    end = datetime.now()
    print("Ended at: %s" % end.strftime("%Y-%m-%d %H:%M:%S"))
    timeTook(begin, end)
