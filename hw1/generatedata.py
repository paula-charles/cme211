import sys
import random

if len(sys.argv) < 5:
    print("Usage:")
    print("$ python3 generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file>")
    sys.exit()

reference_length = sys.argv[1]
nreads = sys.argv[2]
read_length = sys.argv[3]
reference_file = sys.argv[4]
reads_file = sys.argv[5]

reference_length = int(reference_length)
nreads = int(nreads)
read_length = int(read_length)

#function to match a number between 0 and 3 to one of the 4 letters
def random_assignement(k):
    if k == 0:
        return "A"
    if k == 1:
        return "C"
    if k == 2:
        return "G"
    return "T"

#function to create a reference with the last 25% repeated
def create_reference(length):
    random_part = ""
    repeated_part = ""
    random_part_length = int(length*0.75)
    for k in range(random_part_length):
        random_num = random.randint(0,3)
        random_letter = random_assignement(random_num)
        random_part += random_letter
        if k >= length/2:
            repeated_part += random_letter
    return random_part + repeated_part

#function to create a read that will only appear once
#the output is the read followed by a space and its position

def create_read_once(reference, read_length):
    length = len(reference)
    start_pos = random.randint(0,length/2-1)
    return reference[start_pos+read_length] + "{}".format(start_pos)

#function to create a read that will appear twice
#the output is the read and its 2 positions

def create_read_twice(reference, read_length):
    length = len(reference)
    start_pos = random.randint(length/2,length*3/4-read_length)
    start_pos_2 = int(start_pos+length/4)
    return reference[start_pos:start_pos+read_length] + " {} {}".format(start_pos, start_pos_2)

#function to create a random read
#it will be helpful for the reads that never appear

def create_random_read(read_length):
    random_read = ""
    for k in range(read_length):
        random_num = random.randint(0,3)
        random_read += random_assignement(random_num)
    return random_read

#function to create a read that is not in the reference

def create_read_never(reference, read_length):
    read = create_random_read(read_length)
    while reference.find(read) != -1:
        read = create.random_read(read_length)
    return read + " -1"

#function that chooses the type of read we want
#this function increments the total number of reads per type

def create_read(reference,read_length):
    random_number=random.random()
    if random_number < 0.75:
        global number_read_once
        number_read_once += 1
        return create_read_once(reference,read_length)
    if random_number < 0.85:
        global number_read_twice
        number_read_twice += 1
        return create_read_twice(reference,read_length)
    global number_read_never
    number_read_never+=1
    return create_read_never(reference,read_length)

number_read_once = 0
number_read_twice = 0
number_read_never = 0

reference0 = create_reference(reference_length)

ref_file = open(reference_file,"w")
reads_file = open(reads_file,"w")
align_file = open("alignments.txt","w")

ref_file.write(reference0 + "\n")
ref_file.close()

for k in range(nreads):
    read0 = create_read(reference0,read_length)
    reads_file.write(read0.split()[0]+"\n")
    align_file.write(read0+"\n")

reads_file.close()
align_file.close()

print("reference length: {}".format(reference_length))
print("number reads: {}".format(nreads))
print("read length: {}".format(read_length))
print("aligns 0: {}".format(number_read_never/nreads))
print("aligns 1: {}".format(number_read_once/nreads))
print("aligns 2: {}".format(number_read_twice/nreads))
