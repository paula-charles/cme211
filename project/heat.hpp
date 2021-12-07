#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b, x;
    int nrows,ncols;

    /* TODO: Add any additional private data attributes and/or methods you need */

  public:
    void AddUnknown(int i0, int j0, int i1, int j1, double val);
    void InitializeBandX(int length, double init, double init2);
    void AddUnknownB(int i, int j, double val);

    /* Method to setup Ax=b system */
    int Setup(std::string inputfile);

    /* Method to solve system using CGsolver */
    int Solve(std::string soln_prefix);

    /* TODO: Add any additional public methods you need */
    double T_c(double Tc, int j,double l, double h);
};

#endif /* HEAT_HPP */
