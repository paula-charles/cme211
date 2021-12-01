CXX:= g++ -std=c++11
CXXflags := -Wall -Wconversion -Wextra -pedantic
TARGET := main
OBJS:= main.o hw6.o image.o
INCS:= main.hpp hw6.hpp image.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) -ljpeg

%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CPPFLAGS) $(CXXFLAGS)

.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET) *~
