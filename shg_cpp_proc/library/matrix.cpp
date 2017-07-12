#include <vector>
#include <complex>
#include <cmath>
#include <string>
#include <iostream>
#include <fstream>
#include "./matrix.h"

template <typename Type> vector<Type> generate_blank_matrix(
    int N1)
{
    vector<Type> blank;

    blank.resize(N1);

    initialize_matrix<Type>(blank, 0.);

    return blank;
}

template <typename Type> vector<vector<Type> > generate_blank_matrix(
    int N1, int N2)
{
    vector<vector<Type> > blank;

    blank.resize(N1);
    for(int i = 0; i<N1; i++)
	blank[i].resize(N2);

    initialize_matrix<Type>(blank, 0.);

    return blank;
}

template <typename Type> vector<vector<vector<Type> > > generate_blank_matrix(
    int N1, int N2, int N3)
{
    vector<vector<vector<Type> > > blank;

    blank.resize(N1);
    for(int i = 0; i<N1; i++)
    {
	blank[i].resize(N2);
	for(int j = 0; j<N2; j++)
	    blank[i][j].resize(N3);
    }

    initialize_matrix<Type>(blank, 0.);

    return blank;
}

template <typename Type> void initialize_matrix(
    vector<Type> &matrix, Type val)
{
    for(int i = 0; i<matrix.size(); i++)
	matrix[i] = val;
}


template <typename Type> void initialize_matrix(
    vector<vector<Type> > &matrix, Type val)
{
    for(int i = 0; i<matrix.size(); i++)
	for(int j = 0; j<matrix[0].size(); j++)
	    matrix[i][j] = val;
}


template <typename Type> void initialize_matrix(
    vector<vector<vector<Type> > > &matrix, Type val)
{
    for(int i = 0; i<matrix.size(); i++)
	for(int j = 0; j<matrix[0].size(); j++)
	    for(int k = 0; k<matrix[0][0].size(); k++)
		matrix[i][j][k] = val;
}


template <typename Type> void save_matrix(
    vector<Type> &matrix, string location)
{
    ofstream File;
    File.open(location.c_str(), ofstream::out);

    // Check that the file opens correctly.
    if(File.fail())
    {
        cout << "Error saving file at " << location << "." <<endl;
        return;
    }

    // Save matrix
    for(int i = 0; i<matrix.size(); i++)
	File << matrix[i] << endl;

    File.close();
}


template <typename Type> void save_matrix(
    vector<vector<Type> > &matrix, string location)
{
    ofstream File;
    File.open(location.c_str(), ofstream::out);

    // Check that the file opens correctly.
    if(File.fail())
    {
        cout << "Error saving file at " << location << "." <<endl;
        return;
    }

    // Save matrix
    for(int i = 0; i<matrix.size(); i++)
    {
	for(int j = 0; j<matrix[0].size(); j++)
	    File << matrix[i][j] << "\t";

	File << endl;
    }

    File.close();
}


template <typename Type> void save_matrix(
    vector<vector<vector<Type> > > &matrix, string location)
{
    ofstream File;
    File.open(location.c_str(), ofstream::out);

    // Check that the file opens correctly.
    if(File.fail())
    {
        cout << "Error saving file at " << location << "." <<endl;
        return;
    }

    // Save matrix
    for(int k = 0; k<matrix[0][0].size(); k++)
	for(int i = 0; i<matrix.size(); i++)
	{
	    for(int j = 0; j<matrix[0].size(); j++)
		File << matrix[i][j][k] << "\t";

	    File << endl;
	}

    File.close();
}


// Function declrations so that the template files can be separated
template vector<int> generate_blank_matrix(int N1);
template vector<double> generate_blank_matrix(int N1);
template vector<complex<double> > generate_blank_matrix(int N1);
template vector<vector<int> > generate_blank_matrix(
    int N1, int N2);
template vector<vector<double> > generate_blank_matrix(
    int N1, int N2);
template vector<vector<complex<double> > > generate_blank_matrix(
    int N1, int N2);
template vector<vector<vector<int> > > generate_blank_matrix(
    int N1, int N2, int N3);
template vector<vector<vector<double> > > generate_blank_matrix(
    int N1, int N2, int N3);
template vector<vector<vector<complex<double> > > > generate_blank_matrix(
    int N1, int N2, int N3);

template void initialize_matrix(
    vector<int> &matrix, int val);
template void initialize_matrix(
    vector<double> &matrix, double val);
template void initialize_matrix(
    vector<complex<double> > &matrix, complex<double> val);
template void initialize_matrix(
    vector<vector<int> > &matrix, int val);
template void initialize_matrix(
    vector<vector<double> > &matrix, double val);
template void initialize_matrix(
    vector<vector<complex<double> > > &matrix, complex<double> val);
template void initialize_matrix(
    vector<vector<vector<int> > > &matrix, int val);
template void initialize_matrix(
    vector<vector<vector<double> > > &matrix, double val);
template void initialize_matrix(
    vector<vector<vector<complex<double> > > > &matrix, complex<double> val);

template void save_matrix(
    vector<int> &matrix, string location);
template void save_matrix(
    vector<double> &matrix, string location);
template void save_matrix(
    vector<complex<double> > &matrix, string location);
template void save_matrix(
    vector<vector<int> > &matrix, string location);
template void save_matrix(
    vector<vector<double> > &matrix, string location);
template void save_matrix(
    vector<vector<complex<double> > > &matrix, string location);
template void save_matrix(
    vector<vector<vector<int> > > &matrix, string location);
template void save_matrix(
    vector<vector<vector<double> > > &matrix, string location);
template void save_matrix(
    vector<vector<vector<complex<double> > > > &matrix, string location);
