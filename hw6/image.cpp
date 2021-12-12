#include <string>
#include <boost/multi_array.hpp>
#include <iostream>
#include <iomanip>

#include "hw6.hpp"
#include "image.hpp"

image::image(std::string filename):filename_(filename){}

void image::loadImage(void){
  ReadGrayscaleJPEG(filename_,img_);
}

void image::Save(std::string output = ""){
  if (output == "")
    WriteGrayscaleJPEG(filename_,img_);
  else
    WriteGrayscaleJPEG(output,img_);
}

void Convolution(boost::multi_array<unsigned char,2>& input,
                     boost::multi_array<unsigned char,2>& output,
                     boost::multi_array<float,2>&         kernel){

  if (kernel.shape()[0] != kernel.shape()[1]){
    std::cout<<"The kernel is not square"<<std::endl;
    std::exit(EXIT_FAILURE);
  };

  if (kernel.shape()[0] % 2 == 0){
    std::cout<<"The kernel size is even"<<std::endl;
    std::exit(EXIT_FAILURE);
  };

  unsigned int nrows_k = (unsigned int)kernel.shape()[0];
  unsigned int add_rows = (unsigned int)floor(nrows_k/2);
  unsigned int nrows_input = (unsigned int)input.shape()[0];
  unsigned int ncol_input = (unsigned int)input.shape()[1];

  boost::multi_array<float,2> a(boost::extents[nrows_input+nrows_k-1][ncol_input+nrows_k-1]);
  for (unsigned int i = add_rows; i<add_rows+nrows_input;i++){
    for (unsigned int j = add_rows; j<add_rows+ncol_input;j++)
      a[i][j]=(float)input[i-add_rows][j-add_rows];
    for (unsigned int j = 0; j<add_rows;j++)
      a[i][j]=(float)input[i-add_rows][0];
    for (unsigned int j = add_rows+ncol_input; j<add_rows+add_rows+ncol_input;j++){
      a[i][j]=(float)input[i-add_rows][ncol_input-1];
    }
  }

  for (unsigned int i = 0; i<add_rows;i++){
    for (unsigned int j = add_rows; j<add_rows+ncol_input;j++)
      a[i][j] = (float)input[0][j-add_rows];
    for (unsigned int j = 0; j<add_rows;j++)
      a[i][j] = (float)input[0][0];
    for (unsigned int j = add_rows+ncol_input; j<add_rows+add_rows+ncol_input;j++)
      a[i][j]=(float)input[0][ncol_input-1];
  }

  for (unsigned int i = add_rows+nrows_input; i<add_rows+add_rows+nrows_input;i++){
    for (unsigned int j = add_rows; j<add_rows+ncol_input;j++)
      a[i][j] = (float)input[nrows_input-1][j-add_rows];
    for (unsigned int j = 0; j<add_rows;j++)
      a[i][j] = (float)input[nrows_input-1][0];
    for (unsigned int j = add_rows+ncol_input; j<add_rows+add_rows+ncol_input;j++)
      a[i][j]=(float)input[nrows_input-1][ncol_input-1];
  }

  float conv;
  for (unsigned int i = 0; i < nrows_input; i++){
    for (unsigned int j = 0; j < ncol_input; j++){
      conv =0;
      for (unsigned int i2 = 0; i2<nrows_k; i2++){
        for (unsigned int j2 = 0; j2<nrows_k; j2++){
          conv = conv + (float)kernel[i2][j2]*(float)a[i+i2][j+j2];
        }
      }
      conv = std::max(conv,(float)0);
      conv = std::min(conv,(float)255);
      output[i][j]=(unsigned char)floor(conv);
    }
  }

}

void image::BoxBlur(int kernel_size){
  unsigned int kernel_s = (unsigned int)kernel_size;
  boost::multi_array<float, 2> kernel(boost::extents[kernel_s][kernel_s]);
  for (unsigned int i = 0; i < kernel_s; i++) {
    for (unsigned int j = 0; j < kernel_s; j++) {
      kernel[i][j] = (float)1/((float)kernel_size*(float)kernel_size);
    }
  }
  Convolution(img_,img_,kernel);
}

unsigned int image::Sharpness(void){
  unsigned int maximum = 0;

  unsigned int nrows_input = (unsigned int)img_.shape()[0];
  unsigned int ncol_input = (unsigned int)img_.shape()[1];

  boost::multi_array<unsigned char, 2> output(boost::extents[nrows_input][ncol_input]);

  boost::multi_array<float, 2> kernel(boost::extents[3][3]);
  kernel[0][0] = 0;
  kernel[0][1] = 1;
  kernel[0][2] = 0;
  kernel[1][0] = 1;
  kernel[1][1] = -4;
  kernel[1][2] = 1;
  kernel[2][0] = 0;
  kernel[2][1] = 1;
  kernel[2][2] = 0;

  Convolution(img_,output,kernel);

  for (unsigned int n = 0; n < output.num_elements(); n++) {
    if ((unsigned int)output.data()[n]>maximum)
      maximum = (unsigned int)output.data()[n];
  }
  return maximum;
}


//--codequality_0
//--Looks great
//--END
