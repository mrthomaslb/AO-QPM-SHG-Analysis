#ifndef SHG_H
#define SHG_H
#include <string>
#include <vector>
#include <complex>
#include <cmath>
#include "constants.h"
#include "electric_field.h"
#include "mesh.h"
#include "parameters.h"
#include "derivative.h"

using namespace std;


vector<vector<double> > calc_shg_square(vector<vector<complex<double> > > &shg);

vector<vector<complex<double> > > calc_shg(
    electricField &eField, mesh &grid, parameters &par);

vector<vector<complex<double> > > calc_source(
    vector<vector<complex<double> > > &pol, vector<double> &xAxis,
    vector<double> &tAxis, double kRed, double kBlue, double wRed);

vector<vector<complex<double> > > calc_shg_field(
    vector<vector<complex<double> > > source, double dt);

#endif
