#include <string>
#include <vector>
#include <cmath>
#include <iostream>
#include "constants.h"
#include "read_configs.h"
#include "parameters.h"

double o1 = 2.7359;
double o2 = 0.01878;
double o3 = 0.01822;
double o4 = 0.01354;

double parameters::redIndexCalc(double lambda){
    double n;
    n = sqrt(o1 + o2/(pow(lambda,2)-o3) - o4*pow(lambda,2));
    return n;
}

double parameters::blueIndexCalc(double lambda, double theta){
    double e1 = 2.3753;
    double e2 = 0.01224;
    double e3 = 0.01667;
    double e4 = 0.01516;

    double no;
    double ne;
    double n;

    no = sqrt(o1 + o2/(pow(lambda,2)-o3) - o4*pow(lambda,2));
    ne = sqrt(e1 + e2/(pow(lambda,2)-e3) - e4*pow(lambda,2));

    double tan = sin(theta) / cos(theta);
    double cot = cos(theta) / sin(theta);

    n = sqrt(pow(ne / sqrt( pow(ne/no,2) + pow(tan,2) ),2)  +  pow(no / sqrt( pow(no/ne,2) + pow(cot,2) ),2));    
    return n;
}

parameters::parameters(string location)
{
    // Load parameters from config file
    ifstream file;
    file.open(location.c_str());
    check_file(file, location);

    Nx = read_in_int(file);
    Lx = read_in_double(file);
    Lt = read_in_double(file);
    vg = read_in_double(file);

    wavelength = read_in_double(file);
    trainType = read_in_int(file);
    order = read_in_int(file);
    FWHM = read_in_double(file);
    firstCenter = read_in_double(file);
    amplitude = read_in_double(file);
    numOfPulses = read_in_int(file);
    timeSeparation = read_in_double(file);
    partialReflection = read_in_double(file);
    trainTypeBack = read_in_int(file);
    orderBack = read_in_int(file);
    FWHMBack = read_in_double(file);
    numCollisionPt = read_in_int(file);
    firstCollisionPt = read_in_double(file);
    lastCollisionPt = read_in_double(file);
    amplitudeBack = read_in_double(file);
    numOfPulsesBack = read_in_int(file);
    timeSeparationBack = read_in_double(file);
    partialReflectionBack = read_in_double(file);

    theta = read_in_double(file);

    redIndex = redIndexCalc(wavelength*100);
    blueIndex = blueIndexCalc(200*wavelength, theta);

    file.close();

    // Calculate array of collision points to simulate
    collisionPoints.resize(numCollisionPt);
    double dd = (lastCollisionPt - firstCollisionPt)/(numCollisionPt-1);
    for(int i = 0; i<numCollisionPt; i++)
	collisionPoints[i] = i*dd + firstCollisionPt;

    // Calculate the angular frequency of the laser
    omega = 2*PI*c/wavelength;

    // Wavenumbers
    kRed = 2*PI*redIndex/wavelength;
    kBlue = 4*PI*blueIndex/wavelength;

    // Calculate the array of first center points for backward pulse
    double collisionTime = 0.;

    firstCenterBack.resize(numCollisionPt);

    for(int i = 0; i<numCollisionPt; i++)
    {
	collisionTime = collisionPoints[i]/vg+firstCenter;
	firstCenterBack[i] = collisionTime - (Lx-collisionPoints[i])/vg;

	if(firstCenterBack[i] < 0)
	    cout << "Error: firstCenterBack is smaller than zero. You need to "
		"increase firstCenter." << endl;
    }
}
