from math import sqrt

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import os
import scipy.io
import scipy.linalg
from scipy.sparse import csr_matrix
import scipy.sparse.linalg

import warnings
from scipy.sparse import (spdiags, SparseEfficiencyWarning, csc_matrix,
    csr_matrix, isspmatrix, dok_matrix, lil_matrix, bsr_matrix)
warnings.simplefilter('ignore',SparseEfficiencyWarning)

class Truss:
    '''This class creates a truss system. Its inputs are files
    containing the beams and joints and an (optional) output
    location for a graph of the system.
    '''
    def __init__(self,joints_file,beams_file,output_plot=None):
        '''This is the initialization function. It takes 2 or 3
        parameters and creates self.beams and self.joints and an
        output if it is required (if there is a 3rd input
        parameter).
        '''
        self.beams = np.loadtxt(beams_file,dtype = np.int64)
        self.joints = {}
        with open(joints_file,'r') as f:
            f.readline()
            for line in f:
                self.joints[int(line.split()[0])] = \
                {'x' : float(line.split()[1]),\
                'y' : float(line.split()[2]),\
                'Fx' : float(line.split()[3]),\
                'Fy' : float(line.split()[4]),\
                'zerodisp' : int(line.split()[5])}
        if output_plot != None:
            self.PlotGeometry(output_plot)

    def PlotGeometry(self, output_plot):
        '''This method creates a plot for the truss.
        '''
        for k in range(len(self.beams)):
            point1 = self.beams[k][1]
            point2 = self.beams[k][2]
            x = [self.joints[point1]['x'],self.joints[point2]['x']]
            y = [self.joints[point1]['y'],self.joints[point2]['y']]
            plt.plot(x, y,'b')
            plt.margins(x=0.2, y=0.2)
            plt.savefig(output_plot)

    def get_num_fixed_joints(self):
        '''This method finds out the number of fixed joints.
        It will be later used to know the number of columns
        of the matrix of equations.
        '''
        num_fixed_joints = 0
        for point in self.joints:
            if self.joints[point]['zerodisp'] == 1:
                num_fixed_joints += 1
        return num_fixed_joints

    def get_matrix(self):
        '''This method creates a matrix of equations, with 2 rows
        per joint, 1 column per beam force (we already know the
        direction of the beam, so we ony need its norm) and 2
        columns per reaction force due to the fixed supports.
        '''
        fixed_joints = self.get_num_fixed_joints()
        lin = 2 * len(self.joints)
        col = len(self.beams) + 2 * fixed_joints
        if lin != col:
            raise RuntimeError("Truss geometry not suitable "+\
                               "for static equilibrium analysis")
        self.matrix = csr_matrix((lin,col))


        for k in self.beams:
            beam = k[0]
            point1 = k[1]
            point2 = k[2]
            dx = self.joints[point1]['x']-self.joints[point2]['x']
            dy = self.joints[point1]['y']-self.joints[point2]['y']
            beam_len = sqrt(dx**2 + dy**2)

            self.matrix[2*point1-2,beam-1]    = dx / beam_len
            self.matrix[2*point1-1,beam-1] = dy / beam_len

            self.matrix[2*point2-2,beam-1] = - dx / beam_len
            self.matrix[2*point2-1,beam-1] = - dy / beam_len

        fixed_nb = 0
        for point in self.joints:
            if self.joints[point]["zerodisp"] == 1:
                r_x = len(self.beams) + 2 * fixed_nb
                r_y = len(self.beams) + 2 * fixed_nb + 1
                self.matrix[2*point-2,r_x] = 1
                self.matrix[2*point-1,r_y] = 1
                fixed_nb = 1

    def get_vector(self):
        '''This method creates a vector that will be on the RHS
        of the equations, so we put a minus sign in front of the
        data that is inside it. It contains the forces Fx and Fy.
        '''
        lin = 2 * len(self.joints)
        self.vector = np.zeros((lin,1))
        for point in self.joints:
            self.vector[2*point-2][0] = - self.joints[point]['Fx']
            self.vector[2*point-1][0] = - self.joints[point]['Fy']

    def solve_matrix(self):
        '''This method solves the equations for the 2D truss and
        gives back a vector with values for the unknown forces.
        '''
        self.get_matrix()
        self.get_vector()
        x = scipy.sparse.linalg.spsolve(self.matrix, self.vector)
        array_sum = np. sum(x)
        if np. isnan(array_sum) == True:
            raise RuntimeError("Cannot solve the linear system,"\
                               " unstable truss?")
        for k in range(len(x)):
            x[k] = "{:.3f}".format(x[k])
        return x

    def __repr__(self):
        '''This is the method that creates a nice print of an
        object of the class Truss.
        '''
        string = " Beam       Force\n"
        string += "-----------------\n"
        x = self.solve_matrix()
        for k in self.beams:
            beam = k[0]
            string += "    {}".format(beam)
            num_str = "{:.3f}\n".format(x[beam-1])
            len0 = 13 - len(num_str)
            string += " "*len0
            string += num_str
        return string
