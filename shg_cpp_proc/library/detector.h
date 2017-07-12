#ifndef DETECTOR_H
#define DETECTOR_H
#include <string>
#include <vector>
#include "mesh.h"
#include "parameters.h"


using namespace std;

struct detectors
{

    detectors(mesh &grid, parameters &par);

    // Index of the crystal end position iX and time center iT
    int iX, iT;

    vector<vector<double> > diagonal;
    vector<vector<double> > crystalExit;

    void storeInfo(vector<vector<double> > &shgInfo, int index);
};

#endif
