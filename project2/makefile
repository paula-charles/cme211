CXX:= g++
CXXFLAGS := -O3 -Wall -Wextra -Wconversion -std=c++11
TARGET := main
OBJS:= main.o heat.o sparse.o COO2CSR.o CGSolver.o matvecops.o
INCS:= main.hpp heat.hpp sparse.hpp COO2CSR.hpp CGSolver.hpp matvecops.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CPPFLAGS) $(CXXFLAGS)

.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET) *~
