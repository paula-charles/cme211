#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char *argv[]){
  if (argc < 3) {
    std::cout << "Usage:"<<std::endl;
    std::cout << " ./mazesolver <maze file> <solution file>"<<std::endl;
    return 0;
  }
  #define max_nrows 201
  #define max_ncols 201
  int maze[max_nrows][max_ncols];
  int row, col;
  
  std::ifstream f(argv[1]);
  
  if (f.is_open()) {
    f >> row >> col;
    if (row>max_nrows or col>max_ncols) {
      std::cout << "The maze is too large" << std::endl;
      return 0;
    }
    for (int i=0; i<row; i++){
      for (int j=0; j<col; j++){
        maze[i][j] = 0;
      }
    }

    int row0,col0;
    
    while (f>>row0>>col0) {
      maze[row0][col0] = 1;
    }
    f.close();
  }
  std::ofstream g(argv[2]);

  if (g.is_open()){
    int j = 0;
    int i = 0;
    while (maze[i][j] == 1){
      j++; 
    }
    enum direction{
      left,
      right,
      up,
      down
    };
    direction d = down;
    g<<i<<" "<<j<<std::endl;

    while (i<row-1) {
      switch(d){
        case(left):
          if (i>0 and maze[i-1][j]==0){
            i--;
            d = up;
          }
          else if (j>0 and maze[i][j-1]==0){
            j--;
            d = left;
          }
          else if (maze[i+1][j]==0){
            i++;
            d=down;
          }
          else {
            j++;
           d=right;
          }
          break;
    
        case(right):
          if (maze[i+1][j]==0){
            i++;
            d=down;
          }
          else if (j<col-1 and maze[i][j+1]==0){
            j++;
            d=right;
          }
          else if (i>0 and maze[i-1][j]==0){
            i--;
            d = up;
          }
          else {
            j--;
            d = left;
          }
          break;

        case(up):
          if (j<col-1 and maze[i][j+1]==0){
            j++;
            d=right;
          }
          else if (i>0 and maze[i-1][j]==0){
            i--;
            d = up;
          }
          else if (j>0 and maze[i][j-1]==0){
            j--;
            d = left;
          }
          else {
            i++;
            d=down;
          }
          break;

        case(down):
          if (j>0 and maze[i][j-1]==0){
            j--;
            d = left;
          }
          else if (maze[i+1][j]==0){
            i++;
            d=down;
          }
          else if (j>0 and maze[i][j-1]==0){
            j--;
            d = left;
          }
          else if (j<col-1 and maze[i][j+1]==0){
            j++;
            d=right;
          }
          else {
            i--;
            d = up;
          }
          break;
         
      }
      g<<i<<" "<<j<<std::endl;
    }
    g.close();
  }
}       
