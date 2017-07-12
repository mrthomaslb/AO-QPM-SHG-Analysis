# Compiler
CXX = /usr/local/bin/g++-7

# Compilation flags
CPPFLAGS = -O2 -std=c++11 -Wall -Wextra -fopenmp

# Classes folder
CFOLD = ../library/

# List of objects
OBJS = detector.o derivative.o electric_field.o laser.o main.o matrix.o mesh.o	\
parameters.o read_configs.o shg.o

shg: $(OBJS)
	$(CXX) $(CPPFLAGS) -o ./shg $(OBJS)

main.o: main.cpp
	$(CXX) -std=c++11 -O2 -fopenmp -c main.cpp

# All objects
%.o: $(CFOLD)%.cpp $(CFOLD)%.h
	$(CXX) $(CPPFLAGS) -c $<

# Clean
clean:
	rm -f *.o
	rm -f *.dat
	rm -f *.run
