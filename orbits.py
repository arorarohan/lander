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
    #debug prints
    print(f"positions: {position_array}")
    print(f"velocities: {velocity_array}")

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

'''
#verlet method
def verlet(position=INITIAL_POSITION, velocity=INITIAL_VELOCITY) -> None:
    
    #initialize lists
    x_list = []
    v_list = []

    #initial values
    x_list.append(x)
    v_list.append(v)
    
    #calculate first step based on Euler rule
    a = -k * x / m
    x = x + dt * v
    v = v + dt * a
    x_list.append(x)
    v_list.append(v)

    #verlet integration loop
    for i in range(len(t_array)-2): #use index for calling previous item later
        #calculate a
        a = -k * x / m
        #calculate x and v based on verlet rule
        x_2 = x_list[i] #2 x's ago
        x_last = x_list[i+1] #last x
        x = x_last*2 - x_2 + (dt**2) * a
        x_list.append(x)

        v = 1/dt * (x - x_last)
        v_list.append(v)
    
    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    x_array = np.array(x_list)
    v_array = np.array(v_list)

    # plot the position-time graph
    plt.figure(1)
    plt.clf()
    plt.xlabel('time (s)')
    plt.grid()
    plt.plot(t_array, x_array, label='x (m)')
    plt.plot(t_array, v_array, label='v (m/s)')
    plt.legend()
    plt.show()
'''
def main():
    euler() #change depending on which function to test

if __name__ == '__main__':
    main()