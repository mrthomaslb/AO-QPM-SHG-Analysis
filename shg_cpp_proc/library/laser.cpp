#include <vector>
#include <string>
#include <cmath>
#include <iostream>
#include "parameters.h"
#include "mesh.h"
#include "laser.h"


laserPulse::laserPulse(parameters &par, double center, mesh &grid,
		       int pulseDirection)
{
    if(pulseDirection == 1)
    {
	switch(par.trainType)
	{
	case 1:
	    laserShape = calc_pulse_train(par.amplitude, grid.timeAxis,
					  center, par.FWHM, par.numOfPulses,
					  par.timeSeparation, par.order);
	    break;
	case 2:
	    laserShape = calc_etalon_shape(par.amplitude, grid.timeAxis,
					   center, par.FWHM, par.timeSeparation,
					   par.partialReflection,
					   par.numOfPulses,
					   par.order);
	    break;
	default:
	    laserShape = calc_gaussian_shape(par.amplitude,grid.timeAxis,
					     center, par.FWHM, par.order);
	    break;
	}
    }

    if(pulseDirection == -1)
    {
	switch(par.trainTypeBack)
	{
	case 1:
	    laserShape = calc_pulse_train(par.amplitudeBack, grid.timeAxis,
					  center, par.FWHMBack,
					  par.numOfPulsesBack,
					  par.timeSeparationBack,
					  par.orderBack);
	    break;
	case 2:
	    laserShape = calc_etalon_shape(par.amplitudeBack, grid.timeAxis,
					   center, par.FWHMBack,
					   par.timeSeparationBack,
					   par.partialReflectionBack,
					   par.numOfPulsesBack,
					   par.orderBack);
	    break;
	default:
	    laserShape = calc_gaussian_shape(par.amplitudeBack,grid.timeAxis,
					     center, par.FWHMBack,
					     par.orderBack);
	    break;
	}
    }
}


double calc_sigma(double FWHM, int order)
{
    return pow(FWHM,2.*order) / (pow(2.,2.*order) * log(2));
}


vector<double> calc_gaussian_shape(double amplitude, vector<double> timeAxis,
				   double center, double FWHM, int order)
{
    vector<double> shape(timeAxis.size());

    double sigma = calc_sigma(FWHM, order);

    for(int i = 0; i<timeAxis.size(); i++)
	shape[i] = amplitude * exp(- pow(timeAxis[i]-center,2.*order) / sigma);

    return shape;
}


vector<double> pulse_train_gen(int numOfPulses, vector<double> amplitude,
			       vector<double> timeAxis, vector<double> centers,
			       vector<double> FWHM, vector<int> orders)
{
    vector<double> shape(timeAxis.size());
    vector<double> gaussian(timeAxis.size());

    for(int i = 0; i<numOfPulses; i++)
    {
	gaussian = calc_gaussian_shape(amplitude[i], timeAxis, centers[i],
				       FWHM[i], orders[i]);

	for(int j = 0; j<timeAxis.size(); j++)
	    shape[j] = shape[j] + gaussian[j];
    }

    return shape;
}


vector<double> calc_etalon_shape(double firstAmplitude, vector<double> timeAxis,
				 double firstCenter, double FWHM,
				 double timeSeparation,
				 double partialReflection, int numOfPulses,
				 int order)
{
   // Create the inputs for the pulse_train_gen fct
    vector<double> amplitudes(numOfPulses);
    vector<double> centers(numOfPulses);
    vector<double> FWHMs(numOfPulses);
    vector<int> orders(numOfPulses);

    for(int i = 0; i<numOfPulses; i++)
    {
	if(i==0)
	{
	    amplitudes[i] = firstAmplitude;
	}
	else
	{
	    amplitudes[i] = pow(partialReflection,i-2)*pow(1-partialReflection,2)*
		firstAmplitude;
	}
	centers[i] = firstCenter + i*timeSeparation;
	FWHMs[i] = FWHM;
	orders[i] = order;
    }

    // Create pulse train
    vector<double> shape(timeAxis.size());

    shape = pulse_train_gen(numOfPulses, amplitudes, timeAxis, centers, FWHMs,
			    orders);

    return shape;
}

vector<double> calc_pulse_train(double amplitude, vector<double> timeAxis,
				double firstCenter, double FWHM,
				int numOfPulses, double timeSeparation,
				int order)
{
    // Create the inputs for the pulse_train_gen fct
    vector<double> amplitudes(numOfPulses);
    vector<double> centers(numOfPulses);
    vector<double> FWHMs(numOfPulses);
    vector<int> orders(numOfPulses);

    for(int i = 0; i<numOfPulses; i++)
    {
	amplitudes[i] = amplitude;
	centers[i] = firstCenter + i*timeSeparation;
	FWHMs[i] = FWHM;
	orders[i] = order;
    }

    //Create pulse train
    vector<double> shape(timeAxis.size());

    shape = pulse_train_gen(numOfPulses, amplitudes, timeAxis, centers, FWHMs,
			    orders);

    return shape;
}
