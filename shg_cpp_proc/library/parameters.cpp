#include <string>
#include <vector>
#include "constants.h"
#include "read_configs.h"
#include "parameters.h"

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
    redIndex = read_in_double(file);
    blueIndex = read_in_double(file);

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
