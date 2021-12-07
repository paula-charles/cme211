#include <iostream>
#include <vector>
#include <string>
#include <cmath>

std::vector<double> addition(std::vector<double> a, std::vector<double> b) {

  /* This function sums 2 vectors a and b into a vector c */

  std::vector<double> c;

  if (a.size()!= b.size()) {
    std::cout << "Addition: The vectors don't have the same size." << std::endl;
    return c;
  }

  for(unsigned int n = 0; n < a.size(); n++)
    c.push_back(a[n]+b[n]);
  return c;
}


std::vector<double> substraction(std::vector<double> a, std::vector<double> b) {

  /* This function returns c = a - b */

  std::vector<double> c;

  if (a.size()!= b.size()) {
    std::cout << "Substraction: The vectors don't have the same size." << std::endl;
    return c;
  }

  for(unsigned int n = 0; n < a.size(); n++)
    c.push_back(a[n]-b[n]);
  return c;
}

std::vector<double> mult_matrix_vec(std::vector<double> &val,
                                    std::vector<int>    &row_ptr,
                                    std::vector<int>    &col_idx,
                                    std::vector<double> &v) {

  /* This function multiplies a CSR matrix by a vector v */

  std:: vector<double> res;
  if (v.size()!= row_ptr.size()-1) {
    std::cout << "Mult vect matrix: size issue." << std::endl;
    return res;
  }
  unsigned int ind = (unsigned int)row_ptr[0];
  for (unsigned int m = 1; m< row_ptr.size();m++){
    double result = 0;
    unsigned int ind2 = (unsigned int)row_ptr[m];
    for (unsigned n = ind; n<ind2;n++)
      result = result + val[n]*v[(unsigned int)col_idx[n]];
    ind = ind2;
    res.push_back(result);
  }
  return res;
}

double mult_vect(std::vector<double> a,
                 std::vector<double> b) {

  /* This function multiplies transpose of a vector a with a vector b */

  double result = 0;
  if (a.size()!=b.size()){
    std::cout<<"The vectors don't have the same size!"<<std::endl;
    return 0;
  }
  for(unsigned int n = 0; n < a.size(); n++)
    result = result + a[n]*b[n];
  return result;
}

double L2norm(std::vector<double> v) {

  /* This function calculates the L2 norm of vector v */

  double norm = mult_vect(v,v);
  norm = pow(norm,0.5);
  return norm; 
}

std::vector<double> mult_vect_scal(std::vector<double> v,double a){

  /* This function multiplies a vector v and a scalar a */

  std::vector<double> w;
  for(unsigned int n = 0; n < v.size(); n++)
    w.push_back(a*v[n]);
  return w;
}
