#include <string>
#include <iostream>

#include "image.hpp"

int main() {
  std::string file = "stanford.jpg";

  std::string output;
  image arr[7] = {image(file),image(file),
  image(file),image(file),image(file),
  image(file),image(file)};

  std::vector<int> v;
  v.push_back(3);
  v.push_back(7);
  v.push_back(11);
  v.push_back(15);
  v.push_back(19);
  v.push_back(23);
  v.push_back(27);

  image photo0 = image(file);
  photo0.loadImage();
  unsigned int sharp0 = photo0.Sharpness();
  std::cout<<"Original image: "<<sharp0;

  int n = 0;

  for (int t : v){
    arr[n].loadImage();
    arr[n].BoxBlur(t);
    unsigned int sharp = arr[n].Sharpness();
    if (t<10){
      std::cout<<" BoxBlur( "<<t;
      output = "BoxBlur0";
    }
    else{
      std::cout<<" BoxBlur("<<t;
      output = "BoxBlur";
    }
    std::cout<<"): "<<sharp;
    output = output+std::to_string(t)+".jpg";
    arr[n].Save(output);
    n++;
  }
  std::cout<<std::endl;
}


