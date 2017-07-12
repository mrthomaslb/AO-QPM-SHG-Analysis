#ifndef LASER_H
#define LASER_H
#include <vector>
#include <string>
#include <cmath>
#include <iostream>
#include "parameters.h"
#include "mesh.h"

using namespace std;

struct laserPulse
{
    laserPulse(parameters &par, double center, mesh &grid, int pulseDirection);

    vector<double> laserShape;
};

vector<double> calc_gaussian_shape(double amplitude, vector<double> timeAxis,
				   double center, double FWHM, int order);

vector<double> pulse_train_gen(int numOfPulses, vector<double> amplitude,
			       vector<double> timeAxis, vector<double> centers,
			       vector<double> FWHM, vector<int> orders);

vector<double> calc_etalon_shape(double firstAmplitude, vector<double> timeAxis,
				 double firstCenter, double FWHM,
				 double timeSeparation,
				 double partialReflection, int numOfPulses,
				 int order);

vector<double> calc_pulse_train(double amplitude, vector<double> timeAxis,
				double firstCenter, double FWHM,
				int numOfPulses, double timeSeparation,
				int order);
#endif
