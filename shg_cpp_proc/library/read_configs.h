#ifndef READ_CONFIGS_H
#define READ_CONFIGS_H
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

using namespace std;

void check_file(ifstream &stream, string location);

double read_in_double(ifstream &stream);

int read_in_int(ifstream &stream);

bool is_value(string newLine);

#endif
