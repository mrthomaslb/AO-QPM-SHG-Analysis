#ifndef EFIELD_H
#define EFIELD_H
#include <string>
#include <vector>
#include <complex>
#include "laser.h"
#include "mesh.h"
#include "parameters.h"

using namespace std;

struct electricField
{
    electricField(laserPulse &forLaserShape, mesh &grid);
    electricField(laserPulse &forLaserShape, laserPulse &backLaserShape,
		  mesh &grid, parameters &par, double backPhase);

    vector<vector<double> > forEfield;
    vector<vector<double> > backEfield;
    vector<vector<complex<double> > > polarization;
};


vector<vector<double> > calc_for_elec_field(vector<double> forLaserShape,
					    int Nx);
vector<vector<double> > calc_back_elec_field(vector<double> backLaserShape,
					     int Nx);

vector<vector<complex<double> > > calc_polarization(
    vector<vector<double> > forEfield);
vector<vector<complex<double> > > calc_polarization(
    vector<vector<double> > forEfield, vector<vector<double> > backEfield,
    vector<double> xAxis, double k, double backPhase);

#endif
