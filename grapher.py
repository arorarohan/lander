import numpy as np
import matplotlib.pyplot as plt
results = np.loadtxt('analysis.txt')
plt.figure(1)
plt.clf()
plt.xlabel('altitude')
plt.grid()
plt.plot(results[:, 0], results[:, 1], label='error')
plt.plot(results[:, 0], results[:, 2], label='actual descent rate')
plt.legend()
plt.show()