from random import randint

average = 0
total_numbers = 30

setaverage = 20.0
random_range = 40

random_range = input("What's the highest range of random number you would like? ")
setaverage = input("What would you like the average to be? ")
#total_numbers = input("How many numbers would you like in each list? ")
print ""

for i in range(1):
    while (average != setaverage):
        numbers = []
        for i in range(total_numbers/2):
        #replacement in case your average is too close to the upper range
        #for i in range(1):
            numbers.append(randint(0, random_range))

        for i in range((total_numbers/2) - 1):
        #replacement in case your average is too close to the upper range
        #for i in range(total_numbers - 2):
            curraverage = sum(numbers)/float(len(numbers))
            if curraverage >= setaverage:
                numbers.append(randint(0, setaverage))
            else:
                numbers.append(randint(setaverage, random_range))

        lastnumber = 0
        curraverage = sum(numbers)/float(len(numbers))

        if curraverage < setaverage:
            lastnumber = (((setaverage - curraverage) / (1 / float(total_numbers))) + curraverage)
        elif curraverage > setaverage:
            lastnumber = (curraverage - ((curraverage - setaverage) / (1 / float(total_numbers))))
        else:
            lastnumber = setaverage

        lastnumber = int(lastnumber)
        if lastnumber > random_range:
            lastnumber = random_range
        elif lastnumber < 0:
            lastnumber = 0

        numbers.append(lastnumber)

        average = sum(numbers)/float(len(numbers))

    print numbers

print ""
print "Here is %i lists with the average of each being %r" % (1, setaverage)


f = open('./numbers.txt', 'w')
for i in numbers:
    f.write(str(i) + '\n')
