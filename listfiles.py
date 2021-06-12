
from os import listdir
from os.path import isfile, join
mypath = "./posts"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in onlyfiles:
    print(f)
    print(f+".wav")
    file1 = open("./posts/"+f,"r")
    fileText = file1.readlines()
    print(file1.readlines())

    print(" ".join(line.strip() for line in fileText))


