# file scrambler
# takes a file
# breaks it up
# and stores it in a directory
# but in lots of different files
# we could use a random generator (noise) to generate a directory structure for it
# where it has subdirectories, subsubdirectories (etc), files, and locations in the files
# use the seed and the directory as a way to access it

#maybe different scripts for read/write

#store file
#get file

#determine size, blocking
#determine directory structure
#write

#need an algorithm to map an arbitrary file to a structure
#build a tree, that is essentially random

#get seed
#first grab a random number 1 and 100, use it as a power of 2 for our blocking
#generate a random boolean for a new directory or not (give it a random name)
#keep doing that until we get a false for a file
#generate a random file name
#with a random size?
#generate a random location in the file
#store the next chunk of data there

#we may also need an indicator for valid data, so we can use the same files for multiple main files

import noise_squirrel5
import pathlib
import os
import random
import math

# file = 'E:\#A - PROGRAMMING PROJECTS\File Scrambler\download (2).png'
# validFile = True

#grab file from user
validFile = False
while not validFile:
    file = input("Enter the path to the file: ")

    #validate file
    if os.path.exists(file):
        validFile = os.path.isfile(file)

    if not validFile:
        print("Error: Invalid file path entered.")

# path = 'E:\#A - PROGRAMMING PROJECTS\File Scrambler\Files'
# validPath = True
#grab directory to store it in
#validPath = False
# while not validPath:
#     path = input("Enter the path to store the file: ")

#     #validate file
#     if os.path.exists(path):
#         validPath = os.path.isdir(path)

#     if not validPath:
#         print("Error: Invalid path entered.")
path = os.path.join(os.path.dirname(__file__), 'Files')

#generate noise generator
seed = random.randint(0x00000000, 0xFFFFFFFF)
#print(f"Seed: {seed}")
noise = noise_squirrel5.noise_squirrel5(seed)

#determine blocking
#depends on the size of the file, larger files can have larger blocks
#for the max we will use 1/32 the file size
#for min we will use 1/1024 the file size
bytes = os.path.getsize(file)
scale = math.log2(bytes)
scale = math.ceil(scale)
max = scale - 5
min = scale - 10
blocking = noise.randomIntRange(min, max)
blockSize = int(math.pow(2, blocking))


dataPath = os.path.join(path, 'Data')
if not os.path.isdir(dataPath):
    os.makedirs(dataPath)

#now, start processing the file and traversing the directory
files = 0
with open(file, "rb") as f:
    while (byte := f.read(blockSize)):

        #generate a random integer
        pathInt = noise.randomInt()
        #print(pathInt)
        bi = bin(pathInt)
        bi = bi[2:len(bi)]
        bi = bi.ljust(32, '0')
        #print(bi)

        last = 0
        newPath = dataPath
        for i in range (1, 4):
            end = i * 8
            piece = bi[last:end]
            last = end
            #print(piece)
            h = hex(int(piece, 2))
            h = h[2:len(h)]
            newPath = os.path.join(newPath, str(h))
            #print(newPath)

        #now we've got our path, create a file
        fileName = noise.randomInt()

        #and choose a location in the file... maybe later

        #create directory
        if not os.path.isdir(newPath):
            os.makedirs(newPath)
        
        #now write file
        newFile = os.path.join(newPath, str(fileName))
        #print(newFile)
        with open(newFile, "wb+") as nf:
            nf.write(byte)
        files += 1

#write data file

dataFilePath = os.path.join(path, 'Output')
if not os.path.isdir(dataFilePath):
            os.makedirs(dataFilePath)

baseFile = pathlib.Path(file).name
baseFile = os.path.splitext(baseFile)[0]
baseFile = baseFile + '.dat'
dataFilePath = os.path.join(dataFilePath, baseFile)
with open(dataFilePath, "w+") as df:
    df.write(f"Original File::{file}\n")
    df.write(f"New Path::{path}\n")
    df.write(f"Blocks::{blocking}\n")
    df.write(f"Block Size::{blockSize}\n")
    df.write(f"Seed::{seed}\n")
    df.write(f"Generated Files::{files}")

print(f'File scramble complete. Data File: {dataFilePath}')

        
