#random tester
#imports array of random numbers, then counts how many times
#each of them appears and writes the results to a txt file

#tests the truly random nature of python's randint

from random import randint

#generate random numbers
randomnumbers = []
for i in range(1000):
    randomnumbers.append(randint(0,10))

#write them all to a text file
f = open('./random_numbers.txt', 'w')
for i in randomnumbers:
    f.write(str(i) + '\n')
f.close()

#read those random numbers back from file
f = open('./random_numbers.txt', 'r')
content = f.readlines()
f.close()

data = []
for i in content:
    data.append(i[:-1])

dicts = []
keys = ['num', 'count']

#create names
for i in range(10):
    dicts.append("No" + str(i))

#create dictionaries
dic = {
    name: {key: [] for key in keys}
    for name in dicts
}

#assign nums based on name
for i in dic:
    dic[i]['num'] = i[2:]
    dic[i]['count'] = 0

#table header
print "Name\tNumber\tCount"

#count how many times the number shows up in the list
for i in data:
    for l in dic:
        if dic[l]['num'] == str(i):
            dic[l]['count'] += 1

#write results to txt file
f = open('./results.txt', 'w')
f.write('Name\tNumber\tCount\n')
for i in dic:
    num = dic[i]['num']
    count = str(dic[i]['count'])
    results = i + "\t" + num + "\t" + count
    print results
    f.write(results + '\n')

f.close()
