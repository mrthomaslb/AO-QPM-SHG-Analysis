#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include "./read_configs.h"


void check_file(ifstream &stream, string location)
{
    if (!stream.is_open())
    {
        cout << "Oops! " << location << " file could not be opened!" << endl;
        exit(0);
    }
}


int read_in_int(ifstream &stream)
{
    int returnIntVal = 0;
    string line;

    getline(stream, line);

    if(is_value(line))
    {
	size_t found = line.find(":");
        string valString = line.substr(found+1);
        returnIntVal = atoi(valString.c_str());
    }
    else
	returnIntVal = read_in_int(stream);

    return returnIntVal;
}


double read_in_double(ifstream &stream)
{
    double returnDoubleVal = 0.;
    string line;

    getline(stream, line);

    if(is_value(line))
    {
	size_t found = line.find(":");
        string valString = line.substr(found+1);
        returnDoubleVal = atof(valString.c_str());
    }
    else
	returnDoubleVal = read_in_double(stream);

    return returnDoubleVal;
}


bool is_value(string newLine)
{
    // Check the first character for # and for empty lines
    if(newLine[0] == '#' || newLine.length() < 3)
    {
        return false;
    }
    else
    {
        return true;
    }
}
