#include <vector>
#include <string>
#include <cmath>
#include "matrix.h"
#include "parameters.h"
#include "mesh.h"

mesh::mesh(parameters par)
{
    vg = par.vg;
    Nx = int(par.Nx*1.1);
    Lx = par.Lx*1.1;
    Lt = par.Lt*1.1;

    Nt = calc_num_time_pts(par.Lx/par.Nx, vg, Lt);
    spaceAxis = calc_axis(Nx, 0., Lx);
    timeAxis = calc_axis(Nt, 0., Lt);
}


int mesh::calc_num_time_pts(double dx, double vg, double timeDuration)
{
    return int(floor(timeDuration*vg/dx));
}


vector<double> mesh::calc_axis(int length, double lowVal, double highVal)
{
    vector<double> axis(length);

    for(int i = 0; i<length; i++)
	axis[i] = lowVal + i*(highVal-lowVal)/(length-1);

    return axis;
}
