import numpy as np
import matplotlib.pyplot as plt

def main():
    data = np.loadtxt('algorithm_performance_results.csv', delimiter=',')
    y_alpha_beta = data[:, 0]
    y_minimax = data[:, 1]
    x = range(1, len(data) + 1, 1)

    plt.plot(x, y_alpha_beta, color='red', linestyle='dashed', label='alpha beta')
    plt.plot(x, y_minimax, color='blue', linestyle='dotted', label='minimax')
    plt.xticks(x)

    plt.title('Algorithm performance')
    plt.xlabel('depth')
    plt.ylabel('time [s]')
    plt.grid(True)
    plt.legend(loc='best') 
    plt.show()

if __name__=='__main__':
    main()