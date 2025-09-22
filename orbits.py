# uncomment the next line if running in a notebook
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# mass, spring constant, initial position and velocity
M_PLANET = 6.42E23
M_SATELLITE = 1
G = 6.67E-11
#using arrays for cartesian vector coordinates x,y,z
INITIAL_POSITION = np.array([3426000, 250, 250])
INITIAL_VELOCITY = np.array([-3426,0,0])

# simulation time, timestep and time
T_MAX = 400
DT = 0.5
T_ARRAY = np.arange(0, T_MAX, DT)

#euler method
def euler(position=INITIAL_POSITION, velocity=INITIAL_VELOCITY) -> None:
    # initialise empty lists to record trajectories
    position_list = []
    velocity_list = []

    # Euler integration
    for t in T_ARRAY:
        # append current state to trajectories
        position_list.append(position)
        velocity_list.append(velocity)

        # calculate new position and velocity based on gravitational force formula
        abs_position = np.linalg.vector_norm(position)
        abs_acc = - (G * M_PLANET) / (abs_position**3) #cubed because we will multiply with full position vector
        acceleration = position * abs_acc

        position = position + DT * velocity # a vector operation
        velocity = velocity + DT * acceleration #update velocity similarly

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    position_array = np.array(position_list)
    velocity_array = np.array(velocity_list)

    #for graphing, magnitudes are needed
    abs_position_list = [np.linalg.vector_norm(pos) for pos in position_array]
    abs_velocity_list = [np.linalg.vector_norm(vel) for vel in velocity_array] 

    # plot the position-time graph
    plt.figure(1)
    plt.clf()
    plt.xlabel('time (s)')
    plt.grid()
    plt.plot(T_ARRAY, abs_position_list, label='x (m)')
    plt.plot(T_ARRAY, abs_velocity_list, label='v (m/s)')
    plt.legend()
    plt.show()

#verlet method
def verlet(position=INITIAL_POSITION, velocity=INITIAL_VELOCITY) -> None:
    
    #initialize lists
    position_list = []
    velocity_list = []

    #initial values
    position_list.append(position)
    velocity_list.append(velocity)
    
    #calculate first step based on Euler rule
    abs_position = np.linalg.vector_norm(position)
    abs_acc = - (G * M_PLANET) / (abs_position**3) #cubed because we will multiply with full position vector
    acceleration = position * abs_acc
    position = position + DT * velocity # a vector operation
    velocity = velocity + DT * acceleration #update velocity similarly
    position_list.append(position)
    velocity_list.append(velocity)

    #verlet integration loop
    for i in range(len(T_ARRAY)-2): #use index for calling previous item later
        #calculate a
        abs_position = np.linalg.vector_norm(position)
        abs_acc = - (G * M_PLANET) / (abs_position**3) #cubed because we will multiply with full position vector
        acceleration = position * abs_acc

        #calculate x and v based on verlet rule
        position_2 = position_list[i] #2 x's ago
        position_last = position_list[i+1] #last x
        position = position_last*2 - position_2 + (DT**2) * acceleration
        position_list.append(position)

        velocity = 1/DT * (position - position_last)
        velocity_list.append(velocity)
    
    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    position_array = np.array(position_list)
    velocity_array = np.array(velocity_list)

    #create magnitudes for graphing
    position_mags = [np.linalg.vector_norm(pos) for pos in position_array]
    velocity_mags = [np.linalg.vector_norm(pos) for pos in velocity_array]

    # plot the position-time graph
    plt.figure(1)
    plt.clf()
    plt.xlabel('time (s)')
    plt.grid()
    plt.plot(T_ARRAY, position_mags, label='x (m)')
    plt.plot(T_ARRAY, velocity_mags, label='v (m/s)')
    plt.legend()
    plt.show()

def main():
    verlet() #change depending on which function to test

if __name__ == '__main__':
    main()