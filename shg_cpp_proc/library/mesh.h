#ifndef MESH_H
#define MESH_H
#include <vector>
#include <string>
#include <cmath>
#include "matrix.h"
#include "parameters.h"

using namespace std;

struct mesh
{
    mesh(parameters par);

    int Nx, Nt;
    double Lx, Lt;
    vector<double> spaceAxis;
    vector<double> timeAxis;
    double vg;

    int calc_num_time_pts(double dx, double vg, double timeDuration);
    vector<double> calc_axis(int length, double lowVal, double highVal);
};

#endif
