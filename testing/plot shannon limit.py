import cascade #import the code into the testing environment
import matplotlib.pyplot as plt #import matplotlib to plot the output graphically
Shannon_plot, p_plot = [], []
for i in range (1,99,1):
    p = i/100
    p_plot.append(p)
    Shannon_plot.append(cascade.h_func(p))
plt.plot(p_plot,Shannon_plot) # plot the error rate against h_func output
plt.title("h_func function output against error rate") #add a title to the graph
plt.grid() #add gridlines to graph
plt.show() #show graph