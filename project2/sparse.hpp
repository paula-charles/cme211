#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <vector>

#include "COO2CSR.hpp"

class SparseMatrix
{
  private:
    std::vector<int> i_idx;
    std::vector<int> j_idx;
    std::vector<double> a;
    int ncols;
    int nrows;

    /* TODO: Add any additional private data attributes and/or methods  you need */


  public:

    void Initialize(int ncols, int nrows, double init);

    /* Method to add entry to matrix in COO format */
    void AddEntry(int nrows, int ncols, int i, int j, double val);

    /* Method to convert COO matrix to CSR format using provided function */
    void ConvertToCSR();
    int get_CGSolver(std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             std::string soln_prefix);
};
#endif /* SPARSE_HPP */
