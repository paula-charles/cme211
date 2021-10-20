import glob
import math
import os
import sys

class Airfoil:
    '''This class creates an airfoil: it is associated
    with coordinates for its panels and a name.
    '''
    def __init__(self,inputdir):
        '''This function initializes an object of class
        Airfoil. It requires the input directory name and
        will create the name of the airfoil, and a list of
        coordinates for panels of the airfoil. It also calls
        the methods defined in the class.'''
        self.inputdir = inputdir
        if os.path.isdir(self.inputdir) == False:
            raise RuntimeError("the directory {} does not "\
                              "exist.".format(self.inputdir))
#--functionality_1
#--We aren't guaranteed that the user ends their path with a '/' (use os.path.join)
#--START
        if os.path.isfile(self.inputdir+"xy.dat") == False:
            raise RuntimeError("there is no xy.dat file")
#--END
        coord_file = open(self.inputdir+"xy.dat", "r")
        self.coord = []
        self.name = coord_file.readline()
        try:
            for line in coord_file:
                x = float(line.split()[0])
                y = float(line.split()[1])
                self.coord.append([x,y])
        except ValueError:
            raise RuntimeError("the xy.dat file does not"\
                              " have the right format.")
        coord_file.close()
        self.get_edges()
        self.get_chord_len()
        self.get_cp_values()
        self.get_total_cx_cy()
        self.get_lift_coef()
        self.get_stagnation_point()
#--codequality_0
#--Creating member variables (self. variables) in your init improves readability
#--END

    def get_edges(self):
        '''This function enables us to get the coordinates
        of the trailing edge and of the leading edge. We 
        want it to be robust, so we looked for the edges
        by looking for the max and min x, and not by assuming
        their position within the file.'''
        trailing = self.coord[0][0]
        pos_trail = 0
        leading = self.coord[0][0]
        pos_lead = 0
#--codequality_0
#--This works, but you can definitely do this much simpler with min/max
#--START
        for k in range(len(self.coord)):
            if self.coord[k][0] < leading:
                leading = self.coord[k][0]
                pos_lead = k
            if self.coord[k][0] > trailing:
                trailing = self.coord[k][0]
                pos_trail = k
#--END
        self.trailing_edge = self.coord[pos_trail]
        self.leading_edge = self.coord[pos_lead]

    def get_chord_len(self):
        '''This function enables us to get the chord length.'''
        dx2 = (self.trailing_edge[0]-self.leading_edge[0])**2
        dy2 = (self.trailing_edge[1]-self.leading_edge[1])**2
        self.chord_len = math.sqrt(dx2+dy2)

    def get_cp_values(self):
        '''This function enables us to retrieve the cp values
        associated with an angle. All angles and their respective
        cp values are stored into a dictionary.'''
        inp_file = self.inputdir +"alpha"
        list_files = glob.glob(inp_file+"*")
        if len(list_files) == 0:
            raise RuntimeError("there are no alpha files")
        self.cp_data = {}
        for file_name in list_files:
            alpha = file_name[len(inp_file):][:-4]
            try:
                alpha_ok = False
                alpha = float (alpha)
                alpha_ok = True
                file = open(file_name, "r")
                self.cp_data[alpha]=[]
                line0 = file.readline()
                for line in file:
                    cp = float(line.split()[0])
                    self.cp_data[alpha].append(cp)
                file.close()
            except ValueError:
                if alpha_ok == False:
                    print(file_name + ": alpha not parseable as number")
                else:
                    self.cp_data.pop(alpha)
                    print(file_name + " does not have the right format.")
                pass

    def get_cx_cy_point(self,k,alpha):
        '''Calculates delta cx and delta cy between the points
        in position k and k+1 and for the angle alpha'''
#--codequality_0
#--You're re-computing dx and dy for each alpha, can move this outside the method for a bit more efficiency
#--START
        dx = self.coord[k+1][0]-self.coord[k][0]
        dy = self.coord[k+1][1]-self.coord[k][1]
#--END
        cp = self.cp_data[alpha][k]
        dcx = - cp * dy / self.chord_len
        dcy = cp * dx / self.chord_len
        return dcx, dcy

    def get_total_cx_cy(self):
        '''This function enables us to calculate cx and cy
        associated with an angle (total Cartesian force
        coefficients). All angles and their respective
        cx and cy are stored into a dictionary.'''
        self.cx = {}
        self.cy = {}
        for alpha in self.cp_data.keys():
            self.cx[alpha] = 0
            self.cy[alpha] = 0
            for k in range(len(self.coord)-1):
                dcx, dcy = self.get_cx_cy_point(k,alpha)
                self.cx[alpha] += dcx
                self.cy[alpha] += dcy

    def get_lift_coef(self):
        '''This function enables us to calculate the lift
        coefficient for each angle. All angles and their
        respective lift coefficients are stored into
        a dictionary.'''
        self.cl = {}
        for alpha in self.cp_data.keys():
            alpha2 = math.radians(alpha)
            self.cl[alpha] = self.cy[alpha]*math.cos(alpha2)\
            - self.cx[alpha] * math.sin(alpha2)

    def get_stagnation_point(self):
        '''This function finds the stagnation points: the
        points with the highest pressure coefficients.'''
        self.stagn = {}
        for alpha in self.cp_data.keys():
            max_cp = self.cp_data[alpha][0]
            pos = 0
            for k in range(len(self.cp_data[alpha])):
                if self.cp_data[alpha][k] > max_cp:
                    max_cp = self.cp_data[alpha][k]
                    pos = k
            self.stagn[alpha] = []
            self.stagn[alpha].append((self.coord[pos][0]+\
                                      self.coord[pos+1][0])/2)
            self.stagn[alpha].append((self.coord[pos][1]+\
                                      self.coord[pos+1][1])/2)
            self.stagn[alpha].append(max_cp)

    def __repr__(self):
        '''This function prints an Airfoil object in the format
        wanted.'''
        print("Test case: "+self.name+"\n")
        string = "alpha     cl           stagnation pt\n"+\
        "-----  -------  --------------------------\n"
        sorted_alpha = sorted(self.cl.keys())
        for alpha in sorted_alpha:
            string += "{:5.2f}".format(alpha) + "  "
            string += "{:7.4f}".format(self.cl[alpha]) + "  "
            string += "({:7.4f}, {:7.4f})  {:4.4f}"\
            .format(self.stagn[alpha][0],self.stagn[alpha][1],\
                   self.stagn[alpha][2])
            string +="\n"
        return(string)

#--functionality_0
#--Overall nice job!
#--END
