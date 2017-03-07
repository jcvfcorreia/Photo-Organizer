__author__ = "João Correia"
import os
from datetime import datetime
import sys,shutil

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

def getFiles(inputPath):
    outFileList = list()
    for file in os.listdir(inputPath):
        f = os.path.join(inputPath,file)
        if os.path.isfile(f):
            #print(f.split('\\')[-1])
            outFileList.append(File(inputPath,f.split('\\')[-1]))
    return outFileList

if __name__ == "__main__":
    try:
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

            os.mkdir(outputPath)

            outFileList = getFiles(inputPath)
            outFileList.sort()
            print(outputPath)
            for f in outFileList:
                if not str(f.fileName).__contains__("._"):
                    #print("%s - %s" % (f.fileName,datetime.fromtimestamp(f.creationDate)))

                    if os.path.exists(os.path.join(outputPath,str(f.year))):
                        if os.path.exists(os.path.join(os.path.join(outputPath, str(f.year)),str(f.month))):
                            if os.path.exists(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day))):
                                shutil.copyfile(os.path.join(inputPath,f.fileName), os.path.join(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day)),f.fileName))
                                print(f.year)
                                print(f.month)
                                print(f.day)
                        else:
                            os.mkdir(os.path.join(os.path.join(outputPath, str(f.year)),str(f.month)))
                            if os.path.exists(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day))):
                                shutil.copyfile(os.path.join(inputPath, f.fileName), os.path.join(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day)), f.fileName))
                            else:
                                os.mkdir(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day)))
                                shutil.copyfile(os.path.join(inputPath, f.fileName), os.path.join(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day)), f.fileName))
                    else:
                        os.mkdir(os.path.join(outputPath,str(f.year)))

                        if not os.path.exists(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month))):
                            os.mkdir(os.path.join(os.path.join(outputPath,str(f.year)), str(f.month)))

                        if not os.path.exists(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day))):
                            os.mkdir(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day)))

                        shutil.copyfile(os.path.join(inputPath, f.fileName), os.path.join(os.path.join(os.path.join(os.path.join(outputPath, str(f.year)), str(f.month)),str(f.day)), f.fileName))

                        print(f.year)
                        print(f.month)
                        print(f.day)
        else:
            raise Exception("Nº de argumentos errados.\nFormato correcto é <nome programa> -i <diretorio entrada> -o <diretorio saida>")
    except Exception as ex:
        print("ex %s" % (ex.args[0]))
