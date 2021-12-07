import matplotlib
matplotlib.use('Agg')

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

X2 = [k*h for k in range(ncols)]
Y2 = [0 for k in range(ncols)]

T_mean = mean(val)

for j in range(ncols):
    i0 = 0
    diff = 1000
    for k in range(ncols*nrows):
        if j_idx[k]==j:
            if abs(val[k]-T_mean) < diff:
                i0 = i_idx[k]
                diff = abs(val[k]-T_mean)
    Y2[j]=i0

for k in range(len(Y2)):
    Y2[k]=width - Y2[k]*h

for k in range(len(i_idx)):
    i_idx[k]=width - i_idx[k]*h
for k in range(len(j_idx)):
    j_idx[k]=j_idx[k]*h

X = np.reshape(j_idx,(nrows, ncols))
Y = np.reshape(i_idx,(nrows, ncols))
Z = np.reshape(val,(nrows, ncols))

plt.pcolor(X, Y, Z)
plt.colorbar()
plt.plot(X2, Y2, '-k')
plt.axis([0, length, -width, 2*width])
plt.savefig("Pseudocolor plot.pdf")

print("Input file processed: ",sys.argv[1])
print("Mean Temperature: ",round(T_mean,5))
