#include <iostream>
#include <string>
#include <vector>
#include <complex>
#include <omp.h>
#include "../library/detector.h"
#include "../library/derivative.h"
#include "../library/electric_field.h"
#include "../library/laser.h"
#include "../library/matrix.h"
#include "../library/mesh.h"
#include "../library/parameters.h"
#include "../library/read_configs.h"
#include "../library/shg.h"

using namespace std;

int main()
{
    parameters par("../configs/parameters.cfg");

    mesh grid(par);
    save_matrix(grid.spaceAxis, "../data/xAxis.dat");
    save_matrix(grid.timeAxis, "../data/tAxis.dat");

    laserPulse forLaser(par, par.firstCenter, grid, 1);
    save_matrix(forLaser.laserShape, "../data/forLaser.dat");

    detectors shgInfo(grid, par);

#pragma omp parallel for num_threads(6)
    for(int i = 0; i<par.numCollisionPt; i++)
    {
	laserPulse backLaser(par, (par.firstCenterBack)[i], grid, -1);

	double backPhase = par.omega* ((par.firstCenterBack)[i] -
				(par.firstCenterBack)[0]);
	electricField eField(forLaser, backLaser, grid, par, backPhase);

	vector<vector<complex<double> > > shg = calc_shg(eField, grid, par);

	vector<vector<double> > shgSq = calc_shg_square(shg);

	shgInfo.storeInfo(shgSq, i);
    }

    save_matrix(shgInfo.crystalExit, "../data/crystalExit.dat");
    save_matrix(shgInfo.diagonal, "../data/diagonal.dat");

    return 0;
}
