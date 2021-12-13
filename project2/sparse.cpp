#include <iostream>
#include <vector>
#include <string>
#include <cmath>

#include "sparse.hpp"
#include "COO2CSR.hpp"
#include "CGSolver.hpp"

void SparseMatrix::Initialize(int ncols, int nrows, double init){
  for (int i = 0;i<nrows*ncols;i++){
    for (int j =0;j<nrows*ncols;j++){
      a.push_back(init);
      i_idx.push_back(i);
      j_idx.push_back(j);
    }
  }
}

void SparseMatrix::AddEntry(int nrows, int ncols, int i, int j, double val){
  int index = i*nrows*ncols+j;
  a[index] = a[index] + val;
}

void SparseMatrix::ConvertToCSR(){
  COO2CSR(a,i_idx,j_idx);
}

int SparseMatrix::get_CGSolver(std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             std::string soln_prefix){
  int n;
  std::vector<double> a_bis;
  for (unsigned int i=0;i<a.size();i++)
    a_bis.push_back(-a[i]);
  std::vector<double> b_bis;
  for (unsigned int i=0;i<b.size();i++)
    b_bis.push_back(-b[i]);
  n = CGSolver(a_bis,i_idx,j_idx,b_bis,x,tol,soln_prefix);
  return n;
}
