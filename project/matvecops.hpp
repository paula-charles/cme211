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

std::vector<double> addition(const std::vector<double> &a,
                             const std::vector<double> &b);

std::vector<double> substraction(const std::vector<double> &a,
                                 const std::vector<double> &b);

std::vector<double> mult_matrix_vec(const std::vector<double> &val,
                                    const std::vector<int>    &row_ptr,
                                    const std::vector<int>    &col_idx,
                                    const std:: vector<double> &v);

double mult_vect(const std::vector<double> &a, const std::vector<double> &b);

double L2norm(const std::vector<double> &v);

std::vector<double> mult_vect_scal(const std::vector<double> &v,double a);

#endif /* MATVECOPS_HPP */
