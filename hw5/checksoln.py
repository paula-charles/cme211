import numpy as np
import sys

if len(sys.argv) < 3:
    print('Usage:')
    print('    python checksoln.py <maze file> <solution file>[joints file] [beams file]')
    sys.exit(0)

maze_file = sys.argv[1]
maze_solution = sys.argv[2]
sol = np.loadtxt(maze_solution)

def is_the_solution_avoiding_walls(maze_file,maze_solution):
    maze = set()
    with open(maze_file,'r') as f:
        f.readline()
        for line in f:
            maze.add((line.split()[0],line.split()[1])) 

    sol1 = set()
    with open(maze_solution,'r') as f:
        for line in f:
            sol1.add((line.split()[0],line.split()[1]))

    if len(maze.intersection(sol1))!=0:
        return False
    else:
        return True
    
def is_the_solution_moving_properly(sol):
    for k in range(len(sol)-1):
        if sol[k][0]==sol[k+1][0] and sol[k][1]==sol[k+1][1]+1:
            pass
        elif sol[k][0]==sol[k+1][0] and sol[k][1]==sol[k+1][1]-1:
            pass
        elif sol[k][0]==sol[k+1][0]+1 and sol[k][1]==sol[k+1][1]:
            pass
        elif sol[k][0]==sol[k+1][0]-1 and sol[k][1]==sol[k+1][1]:
            pass
        else:
            return False
    return True

def is_the_solution_staying_inside(maze_file,sol):
    with open(maze_file,'r') as f:
        line = f.readline()
        row = int(line.split()[0])
        col = int(line.split()[1])
    for k in sol:
        if k[0]<0 or k[0]>=row:
            return False
        if k[1]<0 or k[1]>=col:
            return False
    return True

def is_the_solution_entering_and_exiting_properly(maze_file,sol):
    with open(maze_file,'r') as f:
        line = f.readline()
        row = int(line.split()[0])
    if int(sol[0][0])!=0:
        return False
    if int(sol[len(sol)-1][0])!= row-1:
        return False
    return True

if is_the_solution_avoiding_walls(maze_file,maze_solution) and\
is_the_solution_moving_properly(sol) and\
is_the_solution_staying_inside(maze_file,sol) and\
is_the_solution_entering_and_exiting_properly(maze_file,sol):
    print('Solution is valid!')

else:
    print("Solution is not valid...")
