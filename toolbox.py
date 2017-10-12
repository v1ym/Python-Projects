#my own personal toolbox library that i can take around with me
#to make writing other scripts easier
#it's a toolbox... that's it.

from random import randint
import os

#tool for creating list of random filenames for testing on other projects
def random_filename_generator():
    filetype = "." + raw_input("Enter file type>> ")
    namelength = input("How long are the names?>> ")
    numberoffiles = input("How many files?>> ")

    try: os.makedirs("test_folder")
    except: pass

    for i in range(numberoffiles):
        letters = ""
        #generate the name
        for i in range(namelength):
            #filename in all numbers
            randomnumber = randint(0, 99)
            if randomnumber < 10:
                randomnumber = "0" + str(randomnumber)
            letters = letters + str(randomnumber)

            #filename in all letters (to do...)
            randomnumber = randint(0, 26)

            #filename in both (to do...)



            #put the name together and create the file

        #create files and assign names to them
        filename = letters + str(filetype)
        filepath = "./test_folder/" + filename
        f = open(filepath, 'w')
        f.close()
        print "file: " + filename

    print ""
    print "done"

random_filename_generator()
