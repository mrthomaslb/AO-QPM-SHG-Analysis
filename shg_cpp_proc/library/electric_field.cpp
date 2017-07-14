#include <string>
#include <vector>
#include <complex>
#include "laser.h"
#include "parameters.h"
#include "electric_field.h"

electricField::electricField(laserPulse &forLaser, mesh &grid)
{
    forEfield = calc_for_elec_field(forLaser.laserShape, grid.Nx);
    polarization = calc_polarization(forEfield);

    backEfield.resize(forEfield.size());
    for(unsigned int i = 0; i<forEfield.size(); i++)
    {
	backEfield[i].resize(forEfield[0].size());
	for(unsigned int j = 0; j<forEfield.size(); j++)
	    backEfield[i][j] = 0.;
    }

}


electricField::electricField(laserPulse &forLaser, laserPulse &backLaser,
			    mesh &grid, parameters &par, double backPhase)
{
    forEfield = calc_for_elec_field(forLaser.laserShape, grid.Nx);
    backEfield = calc_back_elec_field(backLaser.laserShape, grid.Nx);
    polarization = calc_polarization(forEfield, backEfield, grid.spaceAxis,
				     par.kRed, backPhase);
}


vector<vector<double> > calc_for_elec_field(vector<double> forLaserShape,
					    int Nx)
{

    vector<vector<double> > field(Nx, vector<double> (forLaserShape.size()));

    for(unsigned int i=0; i<Nx; i++)
    {
        for(unsigned int j=0; j<forLaserShape.size(); j++)
        {
            if(j<=i)
                field[i][j] = 0.;
            else
                field[i][j] = forLaserShape[j-i];
        }
    }

    return field;
}


vector<vector<double> > calc_back_elec_field(vector<double> backLaserShape,
					     int Nx)
{
    vector<vector<double> > field(Nx, vector<double> (backLaserShape.size()));

    for(unsigned int i=0; i<Nx; i++)
    {
        for(unsigned int j=0; j<backLaserShape.size(); j++)
        {
            if(j<=i)
                field[Nx-1-i][j] = 0.;
            else
                field[Nx-1-i][j] = backLaserShape[j-i];
        }
    }

    return field;
}


vector<vector<complex<double> > > calc_polarization(
    vector<vector<double> > forEfield)
{
    int Nx = forEfield.size();
    int Nt = forEfield[0].size();

    vector<vector<complex<double> > > pol(Nx, vector<complex<double> > (Nt));

    for(int i = 0; i<Nx; i++)
        for(int j = 0; j<Nt; j++)
	    pol[i][j] = complex<double> (forEfield[i][j],0);

    return pol;
}


vector<vector<complex<double> > > calc_polarization(
    vector<vector<double> > forEfield, vector<vector<double> > backEfield,
    vector<double> xAxis, double k, double backPhase)
{
    complex<double> I (0.0, 1.0);

    vector<vector<complex<double> > >  pol(
	forEfield.size(), vector<complex<double> > (forEfield[0].size()));

    for(unsigned int i = 0; i<forEfield.size(); i++)
        for(unsigned int j = 0; j<forEfield[0].size(); j++)
	    pol[i][j] = pow(forEfield[i][j] +
                   backEfield[i][j]*exp(-2.*I*k*xAxis[i]-I*backPhase),2);
//        pol[i][j] = pow(forEfield[i][j],2) +
//                forEfield[i][j]*backEfield[i][j]*exp(-2.*I*k*xAxis[i]-I*backPhase);

    return pol;
}
