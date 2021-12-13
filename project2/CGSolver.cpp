#include <sstream>
#include <string>
#include <iomanip>
#include <iostream>
#include <fstream>

#include "CGSolver.hpp"
#include "matvecops.hpp"

int CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             std::string soln_prefix){

  /* The int success enables us to know if the solver converged.*/
  int success = 0;

  /* Initializing u0*/

  std::vector<double> u0 = x;
  std::vector<double> r0;
  r0 = substraction(b,mult_matrix_vec(val,row_ptr,col_idx,u0));

  double L2norm_r0 = L2norm(r0);

  std::vector<double> p0 = r0;

  int niter = 0;

  int nitermax = (int)row_ptr.size()-1;
  while (niter < nitermax){
    if (niter%10 == 0){
      std::ostringstream sol;
      sol << std::setfill('0') << std::setw(3) << niter;
      std::string sol_file = soln_prefix+sol.str()+".txt";
      std::ofstream g(sol_file);
      if (g.is_open()){
        for (unsigned n=0;n<u0.size();n++)
          g<< std::setprecision(4) << std::scientific << u0[n] << std::endl;
        g.close();
      }
    }
    niter = niter + 1;

    std::vector<double> q0 = mult_matrix_vec(val,row_ptr,col_idx,p0);
    double alpha = mult_vect(r0,r0)/mult_vect(p0,q0);

    u0 = addition(u0,mult_vect_scal(p0,alpha));

    std::vector<double> r1 = substraction(r0,mult_vect_scal(q0,alpha));

    double L2norm_r1 = L2norm(r1);

    if (L2norm_r1/L2norm_r0 < tol){
      success = 1;
      break;
    }

    double beta = mult_vect(r1,r1) / mult_vect(r0,r0);

    p0 = addition(r1, mult_vect_scal(p0,beta));
    r0 = r1;
  }

  /* We update the solution vector to its final value*/

  x = u0;

  std::ostringstream sol;
  sol << std::setfill('0') << std::setw(3) << niter;
  std::string sol_file = soln_prefix+sol.str()+".txt";
  std::ofstream g(sol_file);
  if (g.is_open()){
    for (unsigned n=0;n<u0.size();n++)
      g<< std::setprecision(4) << std::scientific << u0[n] << std::endl;
      g.close();
  }

  if (success == 0)
    return -1;

  return niter;
}
