#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP

#include <vector>

/* Functions that implement basic calculations for matrixes and vectors:
 *
 * - addition : sum of vectors. It returns a vector.
 *
 * - substraction: substraction of 2 vectors. It returns a vector.
 *
 * - mult_matrix_vec: mult. between a matrix and a vector. It returns
 * a vector.
 *
 * - mult_vect: mult. of the transpose of a vector with another vector.
 * It returns a scalar (double).
 *
 * - L2norm: calculates the L2norm of a vector. It returns a double.
 *
 * - mult_vect_scal: multiplication of a vector by a double. It returns
 * a vector.
 */

std::vector<double> addition(std::vector<double> a, std::vector<double> b);

std::vector<double> substraction(std::vector<double> a, std::vector<double> b);

std::vector<double> mult_matrix_vec(std::vector<double> &val,
                                    std::vector<int>    &row_ptr,
                                    std::vector<int>    &col_idx,
                                    std:: vector<double> &v);

double mult_vect(std::vector<double> a, std::vector<double> b);

double L2norm(std::vector<double> v);

std::vector<double> mult_vect_scal(std::vector<double> v,double a);

#endif /* MATVECOPS_HPP */
