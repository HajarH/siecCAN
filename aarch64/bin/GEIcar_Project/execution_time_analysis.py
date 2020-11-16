import matplotlib.pyplot as plt
import numpy as np

nbr_of_figs = 0

def execution_time_analysis(times, name):
    #We compute means execution time
    mean_exec_time = np.mean(times)
    print("\n MEAN EXECUTION TIME IS: ", mean_exec_time, "s\n")

    #Data
    x = range(1,len(times)+1)
    X= [ 1, 2, 3, 4]
    
    #plot execution time variation
    plt.figure()

    #plot all the execution times
    plt.plot(x, times, 'ro')

    plt.title('Execution time analysis: ' + name)
    plt.xlabel('Measures Index')
    plt.ylabel('Execution Time (s)')
    plt.text(1.5, 1.5, "Means execution time is {}".format(mean_exec_time))

    plt.show()

    return mean_exec_time

if __name__ == "__main__":
     execution_time_analysis([1, 2, 3, 4], 'zeubi')
    
    
    

    
