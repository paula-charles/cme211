#include <cmath>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>

#include "COO2CSR.hpp"
#include "matvecops.hpp"
#include "CGSolver.hpp"

int main(int argc, char *argv[]){
  if (argc < 3) {
    std::cout << "Usage:"<<std::endl;
    std::cout << " ./main <input matrix file name> <output solution file name>"<<std::endl;
    return 0;
  }

 /* Create the COO matrix by reading the input file */

  double val0;
  int i0, j0;

  std::ifstream f(argv[1]);

  std::vector<double> val;
  std::vector<int> i_idx;
  std::vector<int> j_idx;

  if (f.is_open()) {
    int row,col;
    f >> row >> col;
    if (row!=col){
      std::cout << "The matrix is not square" << std::endl;
      return 0;
    }

    while (f >> i0 >> j0 >> val0){
      if (val0!=0){
        val.push_back(val0);
        i_idx.push_back(i0);
        j_idx.push_back(j0);
      }
    }
    f.close();
  }

  /* Transform COO matrix to CSR matrix */

  COO2CSR(val,i_idx,j_idx);

  /* Create solution vector: x*/
  /* Create RHS vector: b*/

  std::vector<double> b;
  std::vector<double> x;

  for (unsigned int n = 0; n <i_idx.size()-1; n++){
    b.push_back(0);
    x.push_back(1);
  }

  /* Set up the tolerance*/

  double tol = 0.00001;

  /* RUN the CG code*/

  int niter = CGSolver(val,i_idx,j_idx,b,x,tol);

  /* Write the updated solution vector in the solution file */

  std::ofstream g(argv[2]);
  if (g.is_open()){
    for (unsigned n=0;n<x.size();n++)
      g<< std::setprecision(4) << std::scientific << x[n] << std::endl;
    g.close();
  }

  /* print the success or failure message */

  if (niter == -1) {
    std::cout<<"FAILURE"<<std::endl;
    return 0;
  }

  std::cout<<"SUCCESS: CG solver converged in "<<niter<<" iterations."<<std::endl;

  return 0;
}

//--functionality_0
//--spot check passed.
//--END

//--codequality_0
//--watch import order.
//--END

//--documentation_0
//--good so far.
//--END
