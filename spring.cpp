#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

using namespace std;

int main() {

  // declare variables
  double m, k, x, v, t_max, dt, t, a, second_t, x_2;
  vector<double> t_list, x_list, v_list;

  // mass, spring constant, initial position and velocity
  m = 1;
  k = 1;
  x = 0;
  v = 1;

  // simulation time and timestep
  t_max = 100;
  dt = 0.1;

  // Verlet integration
  for (t = 0; t <= t_max; t = t + dt) {
    
    // append current state to trajectories
    t_list.push_back(t);
    x_list.push_back(x);
    v_list.push_back(v);
    
    // Euler for initial step
    if (t == 0) {
      a = -k * x / m;
      x = x + dt * v;
      v = v + dt * a;
      x_2 = x_list.back(); //save old x value
    }
    //subsequent steps use verlet now that we have 2 previous points
    else {
      a = -k * x / m;
      x = 2*x - x_2 + pow(dt, 2) * a;
      v = 1/dt * (x - x_list.back());
      x_2 = x_list.back();
    }
  }

  // Write the trajectories to file
  ofstream fout;
  fout.open("trajectories.txt");
  if (fout) { // file opened successfully
    for (int i = 0; i < t_list.size(); i = i + 1) {
      fout << t_list[i] << ' ' << x_list[i] << ' ' << v_list[i] << endl;
    }
  } else { // file did not open successfully
    cout << "Could not open trajectory file for writing" << endl;
  }

  /* The file can be loaded and visualised in Python as follows:

  import numpy as np
  import matplotlib.pyplot as plt
  results = np.loadtxt('trajectories.txt')
  plt.figure(1)
  plt.clf()
  plt.xlabel('time (s)')
  plt.grid()
  plt.plot(results[:, 0], results[:, 1], label='x (m)')
  plt.plot(results[:, 0], results[:, 2], label='v (m/s)')
  plt.legend()
  plt.show()

  */
}
