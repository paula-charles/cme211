CXX:= g++
CXXflags := -std=c++11 -Wall -Wconversion -Wextra
TARGET := main
OBJS:= main.o COO2CSR.o matvecops.o CGSolver.o
INCS:= main.hpp COO2CSR.hpp matvecops.hpp CGSolver.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CPPFLAGS) $(CXXFLAGS)

.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET) *~
