import sys
import time

if len(sys.argv) < 3:
    print("Usage:")
    print("$ python3 processdata.py <ref_file> <reads_file> <align_file>")
    sys.exit()

reference_file = sys.argv[1]
reads_file = sys.argv[2]
alignment_file = sys.argv[3]

ref_file = open(reference_file, "r")
read_file = open(reads_file, "r")

#we get the reference sequence
for line in ref_file:
    reference = line.split()[0]
ref_file.close()

#we get a list of the reads
reads_list = []
for line in read_file:
    reads_list.append(line.split()[0])
read_file.close()

# we create global variables to count the read types
number_read_once = 0
number_read_twice = 0
number_read_never = 0

#we modify this list to include the position
#if there are 2 positions, they will be displayed

#the format of one item of the list is the format of
#one line of the assignment file

time0 = time.time()

for k in range(len(reads_list)):
    read0 = reads_list[k]
    pos = reference.find(read0)
    reads_list[k] += " {}".format(pos)
    if pos != -1:
        pos2 = reference.find(read0,pos+1)
        if pos2 != -1:
            reads_list[k] += " {}".format(pos2)
            number_read_twice += 1
        else:
            number_read_once += 1
    else:
        number_read_never += 1
    reads_list[k] += "\n"

time1 = time.time()

#we calculate the number of reads, we will need it later
nreads = len(reads_list)

#we now create the alignment file
align_file = open(alignment_file, "w")

for x in reads_list:
    align_file.write(x)

align_file.close()

print("reference length: {}".format(len(reference)))
print("number reads: {}".format(nreads))
print("align 0: {}".format(number_read_never/nreads))
print("align 1: {}".format(number_read_once/nreads))
print("align 2: {}".format(number_read_twice/nreads))
print("elapsed time: {}".format(time1-time0))
