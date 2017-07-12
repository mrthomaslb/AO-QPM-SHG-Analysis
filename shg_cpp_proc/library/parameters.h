#ifndef PARAMETERS_H
#define PARAMETERS_H
#include <string>
#include <vector>
#include "constants.h"
#include "read_configs.h"

using namespace std;

struct parameters
{
    parameters(string location);

    // Mesh
    int Nx;
    double Lx, Lt, vg;

    // Laser
    double wavelength, omega;

    // Forward laser pulse
    int trainType, order, numOfPulses;
    double FWHM, firstCenter, amplitude, timeSeparation, partialReflection;

    // Backward laser pulse
    int trainTypeBack, orderBack, numOfPulsesBack, numCollisionPt;
    double firstCollisionPt, lastCollisionPt;
    vector<double> collisionPoints;
    vector<double> firstCenterBack;
    double FWHMBack, amplitudeBack, timeSeparationBack, partialReflectionBack;

    // Crystal
    double redIndex, blueIndex;

    // Wavenumbers
    double kRed, kBlue;
};

#endif
