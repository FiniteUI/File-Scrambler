import noise_squirrel5
import pathlib
import os
import random
import math

#grab data file
validDataFile = False
while not validDataFile:
    file = input("Enter the path to the file datafile: ")

    #validate file
    if os.path.exists(file):
        validDataFile = os.path.isfile(file)

    if not validDataFile:
        print("Error: Invalid data file path entered.")

    #try and grab data
    with open(file, 'r') as f:
        content = f.read()
        content = content.splitlines()

        if len(content) != 6:
            validDataFile = False
        else:
            originalFile = content[0].split('::')[1]
            path = content[1].split('::')[1]
            blocks = int(content[2].split('::')[1])
            blocksize = int(content[3].split('::')[1])
            seed = int(content[4].split('::')[1])
            files = int(content[5].split('::')[1])

    if not validDataFile:
        print("Error: Invalid data file passed.")

#now use the seed to unscramble the file
ns = noise_squirrel5.noise_squirrel5(seed)

#need to clear up a position in the random generator to sync with the scrambler
ns.randomInt()

fileBytes = []
path = os.path.join(path, 'Data')
for b in range(files):
    #generate a random integer
    pathInt = ns.randomInt()
    #print(pathInt)
    bi = bin(pathInt)
    bi = bi[2:len(bi)]
    bi = bi.ljust(32, '0')
    #print(bi)

    #generate the file path
    last = 0
    newPath = path
    for i in range (1, 4):
        end = i * 8
        piece = bi[last:end]
        last = end
        #print(piece)
        h = hex(int(piece, 2))
        h = h[2:len(h)]
        newPath = os.path.join(newPath, str(h))
        #print(newPath)

    #now we've got our path, get the file name
    fileName = ns.randomInt()
    newFile = os.path.join(newPath, str(fileName))
    with open(newFile, 'rb') as nf:
        fileBytes.append(nf.read())

#done reading in file, now write to output
finalPath = os.path.join(os.path.dirname(file), pathlib.Path(originalFile).name)
with open(finalPath, "wb+") as nf:
    for i in fileBytes:
        nf.write(i)

print(f"File unscrambling complete. Generated file: {finalPath}")





