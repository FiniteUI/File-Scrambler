# File-Scrambler
This is a simple personal project to "scramble" files, so they cannot be viewed without the Unscrambler script and the proper parameters.

**FileScrambler.py** takes a file, generates a random seed, and breaks the file up into several smaller files in a random directory structure inside the Files\Data.
subdirectory of the main script folder. The number of files generated is random, but depends on the size of the file. Each generated file, at the moment, has a maximum size of 1/32
of the original file size, and a minimum size of 1/1024 of the original file size. The directory and file names are random. 

The script also generates a data file in the Files\Output folder, which includes the seed and some other information about the file needed for recreating it.

**FileUnscrambler.py** takes the data file, and pieces the original file back together using it. The new file is placed in the Files\Output folder.

I may modify this in the future to make the amount of data in each file random, as well as a few other things to further obfuscate the file.

The random elements of this program are generated using my [Squirrel Noise 5](https://github.com/FiniteUI/Squirrel-Noise-5) library.

