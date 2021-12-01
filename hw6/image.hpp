#ifndef IMAGE_HPP

#include <string>
#include <boost/multi_array.hpp>

class image {

    std::string filename_;
    boost::multi_array<unsigned char, 2> img_;

  public:
    image(std::string filename);
    void loadImage(void);
    void Save(std::string output);
    void BoxBlur(int kernel_size);
    unsigned int Sharpness(void);
};

void Convolution(boost::multi_array<unsigned char,2>& input,
                     boost::multi_array<unsigned char,2>& output,
                     boost::multi_array<float,2>&         kernel);
#endif /* IMAGE_HPP */
