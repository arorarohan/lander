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
T_MAX = 100
DT = 0.1
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
    pass

def main():
    euler()

if __name__ == '__main__':
    main()