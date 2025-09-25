// Mars lander simulator
// Version 1.11
// Mechanical simulation functions
// Gabor Csanyi and Andrew Gee, August 2019

// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation, to make use of it
// for non-commercial purposes, provided that (a) its original authorship
// is acknowledged and (b) no modified versions of the source code are
// published. Restriction (b) is designed to protect the integrity of the
// exercise for future generations of students. The authors would be happy
// to receive any suggested modifications by private correspondence to
// ahg@eng.cam.ac.uk and gc121@eng.cam.ac.uk.

#include "lander.h"
#include <vector>
#include <cmath>

void autopilot (void)
  // Autopilot to adjust the engine throttle, parachute and attitude control
{
  // INSERT YOUR CODE HERE
}

vector3d calculate_drag(void)
// Drag calculation helper function
{
  double lander_area, parachute_area;
  lander_area = M_PI * pow(LANDER_SIZE, 2); // circle
  parachute_area = 0; // for now

  // if parachute is deployed, update parachute area
  if (parachute_status == DEPLOYED) {
    parachute_area = pow(2*LANDER_SIZE, 2) * 5;
  }

  // now get drags (check for zero vel)
  vector3d lander_drag, parachute_drag, total_drag;
  if (velocity.abs() > 0
){
    lander_drag = -0.5 * atmospheric_density(position) * DRAG_COEF_LANDER * lander_area * pow(velocity.abs(), 2) * velocity.norm();
    parachute_drag = -0.5 * atmospheric_density(position) * DRAG_COEF_CHUTE * parachute_area * pow(velocity.abs(), 2) * velocity.norm();
    total_drag = lander_drag + parachute_drag;
  }
  else {
    total_drag.x, total_drag.y, total_drag.z = 0;
  }

    return total_drag;
}

void numerical_dynamics (void)
  // This is the function that performs the numerical integration to update the
  // lander's pose. The time step is delta_t (global variable).
{
  // create static lists for the position, velocity tracking across calls
  static vector<vector3d> position_list, velocity_list;

  // reset them if we are running a new scenario.
  if (new_scenario) {
    position_list.clear();
    velocity_list.clear();
    new_scenario = false;
  }

  // Calculate net acceleration on lander by vector sum of 3 forces
  vector3d grav_acc, thrust_acc, drag_acc, thr, total_acc, position_2;
  double total_mass;

  // Start with gravity as we don't need mass
  grav_acc = -(GRAVITY * MARS_MASS) / (pow(position.abs(), 2)) * position.norm();

  // find total mass
  total_mass = UNLOADED_LANDER_MASS + fuel * FUEL_DENSITY;

  // Now thrust
  thr = thrust_wrt_world();
  thrust_acc = thr / total_mass;

  // Now drag
  drag_acc = calculate_drag() / total_mass;
  
  // sum them up to get the total acceleration
  total_acc = grav_acc + thrust_acc + drag_acc;

  // Initial setup: initial conditions then Euler.
  if (position_list.size() == 0) {
    position_list.push_back(position);
    velocity_list.push_back(velocity);

    position = position + delta_t * velocity;
    velocity = velocity + delta_t * total_acc;
    position_list.push_back(position);
    velocity_list.push_back(velocity);
  }
  // Subsequent runs where we have 2 prev steps: Verlet
  else {
    // update position and velocity
    position_2 = position_list[position_list.size() - 2]; // gets second last position
    position = 2*position - position_2 + pow(delta_t, 2) * total_acc;
    velocity = 1/delta_t * (position - position_list.back());

    // now append to lists
    position_list.push_back(position);
    velocity_list.push_back(velocity);
  }
  

  // Here we can apply an autopilot to adjust the thrust, parachute and attitude
  if (autopilot_enabled) autopilot();

  // Here we can apply 3-axis stabilization to ensure the base is always pointing downwards
  if (stabilized_attitude) attitude_stabilization();
}

void initialize_simulation (void)
  // Lander pose initialization - selects one of 10 possible scenarios
{
  // The parameters to set are:
  // position - in Cartesian planetary coordinate system (m)
  // velocity - in Cartesian planetary coordinate system (m/s)
  // orientation - in lander coordinate system (xyz Euler angles, degrees)
  // delta_t - the simulation time step
  // boolean state variables - parachute_status, stabilized_attitude, autopilot_enabled
  // scenario_description - a descriptive string for the help screen

  scenario_description[0] = "circular orbit";
  scenario_description[1] = "descent from 10km";
  scenario_description[2] = "elliptical orbit, thrust changes orbital plane";
  scenario_description[3] = "polar launch at escape velocity (but drag prevents escape)";
  scenario_description[4] = "elliptical orbit that clips the atmosphere and decays";
  scenario_description[5] = "descent from 200km";
  scenario_description[6] = "";
  scenario_description[7] = "";
  scenario_description[8] = "";
  scenario_description[9] = "";

  switch (scenario) {

  case 0:
    // a circular equatorial orbit
    position = vector3d(1.2*MARS_RADIUS, 0.0, 0.0);
    velocity = vector3d(0.0, -3247.087385863725, 0.0);
    orientation = vector3d(0.0, 90.0, 0.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = false;
    autopilot_enabled = false;
    new_scenario = true;
    break;

  case 1:
    // a descent from rest at 10km altitude
    position = vector3d(0.0, -(MARS_RADIUS + 10000.0), 0.0);
    velocity = vector3d(0.0, 0.0, 0.0);
    orientation = vector3d(0.0, 0.0, 90.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = true;
    autopilot_enabled = false;
    new_scenario = true;
    break;

  case 2:
    // an elliptical polar orbit
    position = vector3d(0.0, 0.0, 1.2*MARS_RADIUS);
    velocity = vector3d(3500.0, 0.0, 0.0);
    orientation = vector3d(0.0, 0.0, 90.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = false;
    autopilot_enabled = false;
    new_scenario = true;
    break;

  case 3:
    // polar surface launch at escape velocity (but drag prevents escape)
    position = vector3d(0.0, 0.0, MARS_RADIUS + LANDER_SIZE/2.0);
    velocity = vector3d(0.0, 0.0, 5027.0);
    orientation = vector3d(0.0, 0.0, 0.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = false;
    autopilot_enabled = false;
    new_scenario = true;
    break;

  case 4:
    // an elliptical orbit that clips the atmosphere each time round, losing energy
    position = vector3d(0.0, 0.0, MARS_RADIUS + 100000.0);
    velocity = vector3d(4000.0, 0.0, 0.0);
    orientation = vector3d(0.0, 90.0, 0.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = false;
    autopilot_enabled = false;
    new_scenario = true;
    break;

  case 5:
    // a descent from rest at the edge of the exosphere
    position = vector3d(0.0, -(MARS_RADIUS + EXOSPHERE), 0.0);
    velocity = vector3d(0.0, 0.0, 0.0);
    orientation = vector3d(0.0, 0.0, 90.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = true;
    autopilot_enabled = false;
    new_scenario = true;
    break;

  case 6:
    new_scenario = true;
    break;

  case 7:
    new_scenario = true;
    break;

  case 8:
    new_scenario = true;
    break;

  case 9:
    new_scenario = true;
    break;

  }
}
