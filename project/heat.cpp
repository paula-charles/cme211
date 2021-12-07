#include <fstream>
#include <iostream>
#include <math.h>
#include <string>

#include "heat.hpp"
#include "COO2CSR.hpp"

void HeatEquation2D::AddUnknown(int i0, int j0, int i1, int j1, double val){
  int j = j0 + i0*ncols;
  int i = j1 + i1*ncols;
  A.AddEntry(nrows,ncols,i,j,val);
}

void HeatEquation2D::InitializeBandX(int length, double init, double init2){
  for (int i=0;i<length;i++){
    b.push_back(init);
    x.push_back(init2);
  }
}

void HeatEquation2D::AddUnknownB(int i, int j, double val){
  b[j+i*ncols] = val;
}

double HeatEquation2D::T_c(double Tc, int j,double l, double h){
  double T_c;
  T_c = -Tc *(exp(-10.*pow((double)j*h-l/2.,2.))-2.);
  return T_c;
}

int HeatEquation2D::Setup(std::string inputfile){
  std::ifstream f(inputfile);
  double len,wid,h;
  double Tc,Th;
  
  if (f.is_open()){
    f >> len >> wid >> h;
    f >> Tc >> Th;
    f.close();
  }

  if (floor(len/h)!=ceil(len/h)){return 1;}
  if (floor(wid/h)!=ceil(wid/h)){return 1;}

  nrows = (int)(wid / h)-2;
  ncols = (int)(len / h)-1;
  A.Initialize(ncols,nrows,0.);
  InitializeBandX(nrows*ncols,0.,1.);

  for (int i=0;i<nrows;i++){
    for (int j=0;j<ncols;j++){
      int min_j = j-1;
      int max_j = j+1;
      if (max_j == ncols)
        max_j = 0;
      if (min_j == -1)
        min_j = ncols-1;
      AddUnknown(i,min_j,i,j,1.);
      AddUnknown(i,max_j,i,j,1.);
      AddUnknown(i,j,i,j,-4.);

      if (i > 0)
        AddUnknown(i-1,j,i,j,1.);
      if (i < nrows-1){
        AddUnknown(i+1,j,i,j,1.);
      }
      if (i==0)
        AddUnknownB(i,j,-Th);
      if (i==nrows-1){
        AddUnknownB(i,j,-T_c(Tc,j,len,h));
      }
    }
  }
  A.ConvertToCSR();
  return 0;
}

int HeatEquation2D::Solve(std::string soln_prefix){
  int solver;
  double tol = 0.00001;
  solver = A.get_CGSolver(b,x,tol,soln_prefix);
  if (solver==-1){return 1;}
  std::cout<<"SUCCESS: CG solver converged in "<<solver<<" iterations."<<std::endl;
  return 0;
}
