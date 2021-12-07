import numpy as np
from math import exp
import matplotlib.pyplot as plt
from statistics import mean
import sys

if len(sys.argv) < 3:
    print('Usage:')
    print('    python3 postprocess.py [input-file] [solution file]')
    sys.exit(0)

with open(sys.argv[1],'r') as f:
    line = f.readline()
    length = float(line.split()[0])
    width = float(line.split()[1])
    h = float(line.split()[2])

    line = f.readline()
    Tc = float(line.split()[0])
    Th = float(line.split()[1])

sol_file = sys.argv[2]
sol = np.loadtxt(sol_file,dtype = float)

ncols = int(length/h)
nrows = int(width/h)
i_idx = [0 for k in range(ncols)]
j_idx = [k for k in range(ncols)]
val = [Th for k in range(ncols)]

def T_c(x,Tc):
    return (-Tc*(exp(-10*(x*h-length/2)**2)-2))

n = 0
periodic0 = 0
for i in range(nrows-2):
    for j in range(ncols):
        i_idx.append(i+1)
        j_idx.append(j)
        if j == 0:
            periodic0 = sol[n]
        if j!=ncols-1:
            val.append(sol[n])
            n+=1
        if j == ncols-1:
            val.append(periodic0)

for j in range(ncols):
    i_idx.append(nrows-1)
    j_idx.append(j)
    val.append(T_c(j,Tc))

for k in range(len(i_idx)):
    i_idx[k]=width - i_idx[k]*h
for k in range(len(j_idx)):
    j_idx[k]=j_idx[k]*h

T_mean = mean(val)

print("Input file processed: ",sys.argv[1])
print("Mean Temperature: ",round(T_mean,5))
