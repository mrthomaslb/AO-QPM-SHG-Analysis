#include <string>
#include <vector>
#include <complex>
#include <cmath>
#include "constants.h"
#include "electric_field.h"
#include "mesh.h"
#include "parameters.h"
#include "derivative.h"
#include "shg.h"

vector<vector<double> > calc_shg_square(vector<vector<complex<double> > > &shg)
{
    vector<vector<double> > shgSq (shg.size(),vector<double> (shg[0].size()));

    for(int i = 0; i<shg.size(); i++)
	for(int j = 0; j<shg[0].size(); j++)
	    shgSq[i][j] = pow(abs(shg[i][j]),2);

    return shgSq;
}


vector<vector<complex<double> > > calc_shg(
    electricField &eField, mesh &grid, parameters &par)
{
    return calc_shg_field(
	calc_source(eField.polarization, grid.spaceAxis, grid.timeAxis,
		    par.kRed, par.kBlue, par.omega),
	grid.timeAxis[1] - grid.timeAxis[0]);
}


vector<vector<complex<double> > > calc_source(
    vector<vector<complex<double> > > &pol, vector<double> &xAxis,
    vector<double> &tAxis, double kRed, double kBlue, double wRed)
{

    vector<vector<complex<double> > > source(
	xAxis.size(),vector<complex<double> > (tAxis.size()));

    complex<double> I (0.0, 1.0);

    double deltaK = 2*kRed - kBlue;

    vector<vector<complex<double> > > secondDerPolarization =
	second_der_low_res_2d(xAxis,tAxis,pol,1);
    vector<vector<complex<double> > > firstDerPolariation =
	first_der_low_res_2d(xAxis,tAxis,pol,1);

    for(int i = 0; i<xAxis.size(); i++)
        for(int j = 0; j<tAxis.size(); j++)
            source[i][j] = - I * PI / pow(c,2.) / kBlue *
                (secondDerPolarization[i][j] -
		 4.*I*wRed*firstDerPolariation[i][j] -
		 4.*pow(wRed,2.)*pol[i][j]) * exp(-I*deltaK*xAxis[i]);

    return source;
}


vector<vector<complex<double> > > calc_shg_field(
    vector<vector<complex<double> > > source, double dt)
{

    vector<vector<complex<double> > > shg(
	source.size(),vector<complex<double> > (source[0].size()));

    for(int i = 0; i<source.size(); i++)
    {
	for(int j = 0; j<source[0].size(); j++)
	{
	    // No signal before entering the crystal
	    if(i==0)
	    {
		shg[i][j] = 0.;
	    }
	    // Rest of the crystal
	    else
	    {
		if(j==0)
		    shg[i][j] = 0.;
		else
		    shg[i][j] = shg[i-1][j-1]-0.5*dt*(source[i][j] +
  		      source[i-1][j-1]);
	    }
	}
    }

    return shg;
}
