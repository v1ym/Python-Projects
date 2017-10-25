#my own personal toolbox library that i can take around with me.
#it's a toolbox.
from random import randint
import os

#for creating list of random filenames for testing on other projects
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

#import settings from other txt or ini file
def import_settings(filepath):
    f = open(filepath, 'r')
    filecontent = f.readlines()
    f.close()

    #read the settings.ini file
    data = []
    for i in filecontent:
        string = i[:-1]
        data.append(string.split(':'))

    #create a dict for all the settings to go into
    global settings
    settings = {}
    for i in data:
        settings.update({i[0]:i[1]})

    #convert all key values from strings to floats
    for i in settings:
        settings[i] = float(settings[i])
