#include <iostream>
#include <string>

#include "heat.hpp"

int main(int argc, char *argv[])
{
  /* Get command line arguments */
  if (argc != 3)
  {
    std::cout << "Usage:" << std::endl;
    std::cout << "  " << argv[0] << " <input file> <soln prefix>" << std::endl;
    return 0;
  }
  std::string inputfile   = argv[1];
  std::string soln_prefix   = argv[2];

  /* Setup 2D heat equation system */
  HeatEquation2D sys;
  int status = sys.Setup(inputfile);
  if (status)
  {
    std::cerr << "ERROR: System setup was unsuccessful!" << std::endl;
    return 1;
  }

  /* Solve system using CG */
  status = sys.Solve(soln_prefix);
  if (status)
  {
    std::cerr << "ERROR: System solve was unsuccessful!" << std::endl;
    return 1;
  }

  return 0;
}

//--functionality_1
//--very good! Generally the code is performing as expected. However, the biggest system is not running within a minute.
//--However it is totally accurate. Your plotting is also giving jagged results which is unexpected.
//--END

//--codequality_0
//--code quality is good
//--I especially thought the AddUnknown helper function was a good design
//--it makes your code clear.
//--END

//--documentation_1
//--README is quite thorough. 
//--However comments around functions are quite brief.
//--END
