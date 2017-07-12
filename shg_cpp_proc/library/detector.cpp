#include <string>
#include <vector>
#include "mesh.h"
#include "detector.h"


detectors::detectors(mesh &grid, parameters &par)
{
    // Find the position index of the center of the forward pulse in time
    iT = -1;

    for(int i = 0; i<grid.Nt; i++)
	if((grid.timeAxis)[i]<=par.firstCenter)
	    iT++;

    // Find the position index of the end of the crystal in space
    iX = -1;

    for(int i = 0; i<grid.Nx; i++)
	if((grid.spaceAxis)[i]<=par.Lx)
	    iX++;

    diagonal.resize(grid.Nx);
    for(int i = 0; i<grid.Nx; i++)
	diagonal[i].resize(par.numCollisionPt);

    crystalExit.resize(grid.Nt);
    for(int i = 0; i<grid.Nt; i++)
	crystalExit[i].resize(par.numCollisionPt);
}


void detectors::storeInfo(vector<vector<double> > &shgInfo, int index)
{
    for(unsigned int i = 0; i<diagonal.size(); i++)
	diagonal[i][index] = shgInfo[i][i+iT];

    for(unsigned int i = 0; i<crystalExit.size(); i++)
	crystalExit[i][index] = shgInfo[iX][i];
}
