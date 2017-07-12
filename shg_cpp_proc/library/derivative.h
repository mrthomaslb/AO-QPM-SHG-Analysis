#ifndef DERIVATIVE_H
#define DERIVATIVE_H
#include <vector>
#include <cmath>
#include <iostream>
#include <complex>

using namespace std;

// Functions to be call from the "Outside".
template <typename Type> vector<Type> first_der_low_res_1d(
        vector<double> &x_axis, vector<Type> &y_axis);
template <typename Type> vector<Type> first_der_high_res_1d(
        vector<double> &x_axis, vector<Type> &y_axis);

template <typename Type> vector<vector<Type> > first_der_low_res_2d(
        vector<double> &x_axis, vector<double> &y_axis,
        vector<vector<Type> > &z_axis, int direction);

//template <typename Type> vector<vector<Type> > first_der_high_res_2d(
        //vector<double> &x_axis, vector<double> &y_axis,
        //vector<vector<Type> > &z_axis, int direction);

template <typename Type> vector<Type> second_der_low_res_1d(
        vector<double> &x_axis, vector<Type> &y_axis);
template <typename Type> vector<Type> second_der_high_res_1d(
        vector<double> &x_axis, vector<Type> &y_axis);

template <typename Type> vector<vector<Type> > second_der_low_res_2d(
        vector<double> &x_axis, vector<double> &y_axis,
        vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> vector<vector<Type> > second_der_high_res_2d(
        //vector<double> &x_axis, vector<double> &y_axis,
        //vector<vector<Type> > &z_axis, int Direction);

//
// --------------------------------------------------------------------------
// Internal functions declarations

/* Internal functions necessary to perform first order low resolution
 * differentiation.
 */

template <typename Type> Type first_der_3pts_forward(int x_index, double dx,
        vector<Type> &y_axis);
template <typename Type> Type first_der_3pts_centered(int x_index, double dx,
        vector<Type> &y_axis);
template <typename Type> Type first_der_3pts_backward(int x_index, double dx,
        vector<Type> &y_axis);

template <typename Type> Type first_der_3pts_forward(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
template <typename Type> Type first_der_3pts_centered(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
template <typename Type> Type first_der_3pts_backward(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);

/* Internal functions necessary to perform first order high resolution
 * differentiation.
 */
template <typename Type> Type first_der_5pts_forward(int x_index, double dx,
        vector<Type> &y_axis);
template <typename Type> Type first_der_5pts_half_forward(int x_index,double dx,
        vector<Type> &y_axis);
template <typename Type> Type  first_der_5pts_centered(int x_index, double dx,
        vector<Type> &y_axis);
template <typename Type> Type first_der_5pts_half_backward(int x_index,
        double dx, vector<Type> &y_axis);
template <typename Type> Type first_der_5pts_backward(int x_index, double dx,
        vector<Type> &y_axis);

//template <typename Type> Type first_der_5pts_forward(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> Type first_der_5pts_half_forward(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> Type first_der_5pts_centered(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> Type first_der_5pts_half_backward(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> Type first_der_5pts_backward(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);

/* Internal functions necessary to perform second order low resolution
 * differentiation.
 */
template <typename Type> Type second_der_4pts_forward(int x_index, double dx,
        vector<Type> &y_axis);
template <typename Type> Type second_der_3pts_centered(int x_index, double dx,
        vector<Type> &y_axis);
template <typename Type> Type second_der_4pts_backward(int x_index, double dx,
        vector<Type> &y_axis);

template <typename Type> Type second_der_4pts_forward(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
template <typename Type> Type second_der_3pts_centered(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
template <typename Type> Type second_der_4pts_backward(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);

/* Internal functions necessary to perform second order high resolution
 * differentiation.
 */
template <typename Type> Type second_der_6pts_forward(int x_index, double dx,
        vector<Type> &y_axis);
template <typename Type> Type second_der_6pts_half_forward(int x_index,
        double dx, vector<Type> &y_axis);
template <typename Type> Type second_der_5pts_centered(int x_index, double dx,
        vector<Type> &y_axis);
template <typename Type> Type second_der_6pts_half_backward(int x_index,
        double dx, vector<Type> &y_axis);
template <typename Type> Type second_der_6pts_backward(int x_index, double dx,
        vector<Type> &y_axis);

//template <typename Type> Type second_der_6pts_forward(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> Type second_der_6pts_half_forward(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> Type second_der_5pts_centered(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> Type second_der_6pts_half_backward(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);
//template <typename Type> Type second_der_6pts_backward(int x_index, double dx,
        //int y_index, double dy, vector<vector<Type> > &z_axis, int Direction);

// Internal function to check that the arrays are the same length
template <typename Type> void check_axis_length(vector<double> x_axis,
        vector<Type> y_axis);


// --------------------------------------------------------------------------

template <typename Type> vector<Type> first_der_low_res_1d(vector<double> &x_axis,
        vector<Type> &y_axis)
{
  // Calculate dx
  double dx = x_axis[1] - x_axis[0];

  // Length check
  check_axis_length(x_axis,y_axis);

  // Create return array
  vector<Type> derivative;
  derivative.resize(y_axis.size());

  for(int i=0; i<y_axis.size(); i++)
  {
    if(i==0)
    {
      derivative[i] = first_der_3pts_forward(i, dx, y_axis);
    }
    else if(i==y_axis.size()-1)
    {
      derivative[i] = first_der_3pts_backward(i, dx, y_axis);
    }
    else
    {
      derivative[i] = first_der_3pts_centered(i, dx, y_axis);
    }
  }

  return derivative;
}


template <typename Type> vector<vector<Type> > first_der_low_res_2d(
        vector<double> &x_axis, vector<double> &y_axis,
        vector<vector<Type> > &z_axis, int Direction )
{
  // Calculate dx
  double dx = x_axis[1] - x_axis[0];
  double dy = y_axis[1] - y_axis[0];

  int Nx = x_axis.size();
  int Ny = y_axis.size();

  // Create return array
  vector<vector<Type> > derivative;
  derivative.resize(Nx);

  for(int i = 0; i<Nx; i++)
      derivative[i].resize(Ny);

  for(int j = 0; j<Ny; j++)
  {
      for(int i = 0; i<Nx; i++)
      {
          if(i==0 && Direction==0)
              derivative[i][j] = first_der_3pts_forward(i, dx, j, dy, z_axis,
                      Direction);
          else if(i==Nx-1 && Direction == 0)
              derivative[i][j] = first_der_3pts_backward(i, dx, j, dy, z_axis,
                      Direction);
          else if(j==0 && Direction==1)
              derivative[i][j] = first_der_3pts_forward(i, dx, j, dy, z_axis,
                      Direction);
          else if(j==Ny-1 && Direction == 1)
              derivative[i][j] = first_der_3pts_backward(i, dx, j, dy, z_axis,
                      Direction);
          else
              derivative[i][j] = first_der_3pts_centered(i, dx, j, dy, z_axis,
                      Direction);
      }
  }

  return derivative;
}

template <typename Type> vector<Type> first_der_high_res_1d(vector<double> &x_axis,
        vector<Type> &y_axis)
{
  // Calculate dx
  double dx = x_axis[1] - x_axis[0];

  // Length check
  check_axis_length(x_axis,y_axis);

  // Create return array
  vector<Type> derivative;
  derivative.resize(y_axis.size());

  for(int i=0; i<y_axis.size(); i++)
  {
    if(i==0)
    {
      derivative[i] = first_der_5pts_forward(i, dx, y_axis);
    }
    else if(i==1)
    {
      derivative[i] = first_der_5pts_half_forward(i, dx, y_axis);
    }
    else if(i==y_axis.size()-2)
    {
      derivative[i] = first_der_5pts_half_backward(i, dx, y_axis);
    }
    else if(i==y_axis.size()-1)
    {
      derivative[i] = first_der_5pts_backward(i, dx, y_axis);
    }
    else
    {
      derivative[i] = first_der_5pts_centered(i, dx, y_axis);
    }
  }

  return derivative;
}


template <typename Type> vector<Type> second_der_low_res_1d(vector<double> &x_axis,
        vector<Type> &y_axis)
{
  // Calculate dx
  double dx = x_axis[1] - x_axis[0];

  // Length check
  check_axis_length(x_axis,y_axis);

  // Create return array
  vector<Type> derivative;
  derivative.resize(y_axis.size());

  for(int i=0; i<y_axis.size(); i++)
  {
    if(i==0)
    {
      derivative[i] = second_der_4pts_forward(i, dx, y_axis);
    }
    else if(i==y_axis.size()-1)
    {
      derivative[i] = second_der_4pts_backward(i, dx, y_axis);
    }
    else
    {
      derivative[i] = second_der_3pts_centered(i, dx, y_axis);
    }
  }

  return derivative;
}


template <typename Type> vector<vector<Type> > second_der_low_res_2d(
        vector<double> &x_axis, vector<double> &y_axis,
        vector<vector<Type> > &z_axis, int Direction)
{
  // Calculate dx
  double dx = x_axis[1] - x_axis[0];
  double dy = y_axis[1] - y_axis[0];

  int Nx = x_axis.size();
  int Ny = y_axis.size();

  // Create return array
  vector<vector<Type> > derivative;
  derivative.resize(Nx);
  for(int i = 0; i<Nx; i++)
      derivative[i].resize(Ny);

  for(int j = 0; j<Ny; j++)
  {
      for(int i=0; i<Nx; i++)
      {
          if(i==0 && Direction==0)
              derivative[i][j] = second_der_4pts_forward(i, dx, j, dy, z_axis,
                      Direction);
          else if(i==Nx-1 && Direction == 0)
              derivative[i][j] = second_der_4pts_backward(i, dx, j, dy, z_axis,
                      Direction);
          else if(j==0 && Direction==1)
              derivative[i][j] = second_der_4pts_forward(i, dx, j, dy, z_axis,
                      Direction);
          else if(j==Ny-1 && Direction == 1)
              derivative[i][j] = second_der_4pts_backward(i, dx, j, dy, z_axis,
                      Direction);
          else
              derivative[i][j] = second_der_3pts_centered(i, dx, j, dy, z_axis,
                      Direction);
      }
  }

  return derivative;
}


template <typename Type> vector<Type> second_der_high_res_1d(vector<double> &x_axis,
        vector<Type> &y_axis)
{
  // Calculate dx
  double dx = x_axis[1] - x_axis[0];

  // Length check
  check_axis_length(x_axis,y_axis);

  // Create return array
  vector<Type> derivative;
  derivative.resize(y_axis.size());

  for(int i=0; i<y_axis.size(); i++)
  {
    if(i==0)
    {
      derivative[i] = second_der_6pts_forward(i, dx, y_axis);
    }
    else if(i==1)
    {
      derivative[i] = second_der_6pts_half_forward(i, dx, y_axis);
    }
    else if(i==y_axis.size()-2)
    {
      derivative[i] = second_der_6pts_half_backward(i, dx, y_axis);
    }
    else if(i==y_axis.size()-1)
    {
      derivative[i] = second_der_6pts_backward(i, dx, y_axis);
    }
    else
    {
      derivative[i] = second_der_5pts_centered(i, dx, y_axis);
    }
  }

  return derivative;
}


template <typename Type> Type first_der_3pts_forward(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (-3.*y_axis[x_index] + 4.*y_axis[x_index+1] - y_axis[x_index+2]) /
      (2.*dx);
}


template <typename Type> Type first_der_3pts_forward(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction)
{
    Type val;

    if(Direction == 0)
        val = (-3.*z_axis[x_index][y_index] + 4.*z_axis[x_index+1][y_index] -
                z_axis[x_index+2][y_index])/(2.*dx);
    else
        val = (-3.*z_axis[x_index][y_index] + 4.*z_axis[x_index][y_index+1] -
                z_axis[x_index][y_index+2])/(2.*dy);

    return val;
}


template <typename Type> Type first_der_3pts_centered(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (y_axis[x_index+1] - y_axis[x_index-1])/(2.*dx);
}


template <typename Type> Type first_der_3pts_centered(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction)
{
    Type val;

    if(Direction == 0)
        val = (z_axis[x_index+1][y_index] - z_axis[x_index-1][y_index])/(2.*dx);
    else
        val = (z_axis[x_index][y_index+1] - z_axis[x_index][y_index-1])/(2.*dy);

    return val;
}


template <typename Type> Type first_der_3pts_backward(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (3.*y_axis[x_index] - 4.*y_axis[x_index-1] + y_axis[x_index-2])/(2.*dx);
}


template <typename Type> Type first_der_3pts_backward(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction)
{
    Type val;

    if(Direction == 0)
        val = (3.*z_axis[x_index][y_index] - 4.*z_axis[x_index-1][y_index] +
                z_axis[x_index-2][y_index])/(2.*dx);
    else
        val = (3.*z_axis[x_index][y_index] - 4.*z_axis[x_index][y_index-1] +
                z_axis[x_index][y_index-2])/(2.*dy);

    return val;
}


template <typename Type> Type first_der_5pts_forward(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (-25.*y_axis[x_index] + 48.*y_axis[x_index+1] - 36.*y_axis[x_index+2] +
  16.*y_axis[x_index+3] - 3.*y_axis[x_index+4]) / (12.*dx);
}


template <typename Type> Type first_der_5pts_half_forward(int x_index,
        double dx, vector<Type> &y_axis)
{
  return (-3.*y_axis[x_index-1] - 10.*y_axis[x_index] + 18.*y_axis[x_index+1] -
  6.*y_axis[x_index+2] + y_axis[x_index+3]) / (12.*dx);
}


template <typename Type> Type first_der_5pts_centered(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (y_axis[x_index-2] - 8.*y_axis[x_index-1] + 8.*y_axis[x_index+1] -
  y_axis[x_index+2]) / (12.*dx);
}


template <typename Type> Type first_der_5pts_half_backward(int x_index,
        double dx, vector<Type> &y_axis)
{
  return (-y_axis[x_index-3] + 6.*y_axis[x_index-2] - 18.*y_axis[x_index-1] +
  10.*y_axis[x_index] + 3.*y_axis[x_index+1]) / (12.*dx);
}


template <typename Type> Type first_der_5pts_backward(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (25.*y_axis[x_index] - 48.*y_axis[x_index-1] + 36.*y_axis[x_index-2] -
  16.*y_axis[x_index-3] + 3.*y_axis[x_index-4]) / (12.*dx);
}


template <typename Type> Type second_der_4pts_forward(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (2.*y_axis[x_index] - 5.*y_axis[x_index+1] + 4.*y_axis[x_index+2] -
  y_axis[x_index+3]) / pow(dx,2.);
}


template <typename Type> Type second_der_4pts_forward(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction)
{
    Type val;

    if(Direction == 0)
        val = (2.*z_axis[x_index][y_index] - 5.*z_axis[x_index+1][y_index] +
                4.*z_axis[x_index+2][y_index] - z_axis[x_index+3][y_index]) /
            pow(dx,2.);
    else
        val = (2.*z_axis[x_index][y_index] - 5.*z_axis[x_index][y_index+1] +
                4.*z_axis[x_index][y_index+2] - z_axis[x_index][y_index+3]) /
            pow(dy,2.);

    return val;
}


template <typename Type> Type second_der_3pts_centered(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (y_axis[x_index-1] - 2.*y_axis[x_index] + y_axis[x_index+1]) /
      pow(dx,2.);
}


template <typename Type> Type second_der_3pts_centered(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction)
{
    Type val;

    if(Direction==0)
        val = (z_axis[x_index-1][y_index] - 2.*z_axis[x_index][y_index] +
            z_axis[x_index+1][y_index])/ pow(dx,2.);
    else
        val = (z_axis[x_index][y_index-1] - 2.*z_axis[x_index][y_index] +
            z_axis[x_index][y_index+1])/ pow(dy,2.);

    return val;
}


template <typename Type> Type second_der_4pts_backward(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (-y_axis[x_index-3] + 4.*y_axis[x_index-2] - 5.*y_axis[x_index-1] +
  2.*y_axis[x_index])/pow(dx,2.);
}


template <typename Type> Type second_der_4pts_backward(int x_index, double dx,
        int y_index, double dy, vector<vector<Type> > &z_axis, int Direction)
{
    Type val;

    if(Direction==0)
        val = (-z_axis[x_index-3][y_index] + 4.*z_axis[x_index-2][y_index] -
                5.*z_axis[x_index-1][y_index] + 2.*z_axis[x_index][y_index]) /
            pow(dx,2.);
    else
        val = (-z_axis[x_index][y_index-3] + 4.*z_axis[x_index][y_index-2] -
                5.*z_axis[x_index][y_index-1] + 2.*z_axis[x_index][y_index]) /
            pow(dy,2.);

    return val;
}


template <typename Type> Type second_der_6pts_forward(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (45.*y_axis[x_index] - 154.*y_axis[x_index+1] + 214.*y_axis[x_index+2] -
  156.*y_axis[x_index+3] + 61.*y_axis[x_index+4] - 10.*y_axis[x_index+5]) /
  (12.*pow(dx,2.));
}


template <typename Type> Type second_der_6pts_half_forward(int x_index,
        double dx, vector<Type> &y_axis)
{
  return (10.*y_axis[x_index-1] - 15.*y_axis[x_index] - 4.*y_axis[x_index+1] +
  14.*y_axis[x_index+2] - 6.*y_axis[x_index+3] + y_axis[x_index+4]) /
  (12.*pow(dx,2.));
}


template <typename Type> Type second_der_5pts_centered(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (-y_axis[x_index-2] + 16.*y_axis[x_index-1] - 30.*y_axis[x_index] +
  16.*y_axis[x_index+1] - y_axis[x_index+2]) / (12.*pow(dx,2.));
}


template <typename Type> Type second_der_6pts_half_backward(int x_index,
        double dx, vector<Type> &y_axis)
{
  return (y_axis[x_index-4] - 6.*y_axis[x_index-3] + 14.*y_axis[x_index-2] -
  4.*y_axis[x_index-1] - 15.*y_axis[x_index] + 10.*y_axis[x_index+1]) /
  (12.*pow(dx,2.));
}


template <typename Type> Type second_der_6pts_backward(int x_index, double dx,
        vector<Type> &y_axis)
{
  return (-10.*y_axis[x_index-5] + 61.*y_axis[x_index-4] - 156.*y_axis[x_index-3] +
  214.*y_axis[x_index-2] - 154.*y_axis[x_index-1] + 45.*y_axis[x_index]) /
  (12.*pow(dx,2.));
}


//double calc_dx(vector<double> &x_axis)
//{
  //return fabs(x_axis[1]-x_axis[0]);
//}


template <typename Type> void check_axis_length(vector<double> x_axis,
        vector<Type> y_axis)
{
  if(x_axis.size() != y_axis.size())
  {
    cout << "Arrays are of different length in differentiation."
	      << endl;
  }
}


#endif // DERIVATIVE_H
