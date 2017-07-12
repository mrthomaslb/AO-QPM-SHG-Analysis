#ifndef MATRIX_H
#define MATRIX_H
#include <vector>
#include <complex>
#include <cmath>
#include <string>
#include <iostream>
#include <fstream>

using namespace std;

template <typename Type> vector<Type> generate_blank_matrix(
    int N1);
template <typename Type> vector<vector<Type> > generate_blank_matrix(
    int N1, int N2);
template <typename Type> vector<vector<vector<Type> > > generate_blank_matrix(
    int N1, int N2, int N3);

template <typename Type> void initialize_matrix(
    vector<Type> &matrix, Type val);
template <typename Type> void initialize_matrix(
    vector<vector<Type> > &matrix, Type val);
template <typename Type> void initialize_matrix(
    vector<vector<vector<Type> > > &matrix, Type val);

template <typename Type> void save_matrix(
    vector<Type> &matrix, string location);
template <typename Type> void save_matrix(
    vector<vector<Type> > &matrix, string location);
template <typename Type> void save_matrix(
    vector<vector<vector<Type> > > &matrix, string location);

#endif
