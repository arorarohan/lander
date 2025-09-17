# uncomment the next line if running in a notebook
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# mass, spring constant, initial position and velocity
M = 1
K = 1
X = 0
V = 1

# simulation time, timestep and time
T_MAX = 400
DT = 1.9
T_ARRAY = np.arange(0, T_MAX, DT)

#euler method
def euler(dt=DT, t_array=T_ARRAY, k=K, m=M, x=X, v=V) -> None:
    # initialise empty lists to record trajectories
    x_list = []
    v_list = []

    # Euler integration
    for t in t_array:

        # append current state to trajectories
        x_list.append(x)
        v_list.append(v)

        # calculate new position and velocity
        a = -k * x / m
        x = x + dt * v
        v = v + dt * a

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

#verlet method
def verlet(dt=DT, t_array=T_ARRAY, k=K, m=M, x=X, v=V) -> None:
    
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

def main():
    verlet() #change depending on which function to test

if __name__ == '__main__':
    main()