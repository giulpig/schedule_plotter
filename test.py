import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Button handler object
class Index(object):
    ind = 0

    # This function is called when bswitch is clicked
    def switch(self, event):
        self.ind = (self.ind+1) % len(functions)
        ydata = 1 + functions[self.ind](2 * np.pi * t)
        l.set_ydata(ydata)
        ax.set(title='Graph '+str(self.ind + 1))
        
        plt.draw()

    # This function is called when bquit is clicked
    def quit(self, event):
        plt.close()

# Store the functions you want to use to plot the two different graphs in a list
functions = [np.sin, np.cos]

# Adjust bottom to make room for Buttons
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# Get t and s values for Graph 1
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

# Plot Graph 1 and set axes and title
l, = plt.plot(t, s, lw=2)
ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='Graph 1')

# Initialize Button handler object
callback = Index()

# Connect to a "switch" Button, setting its left, top, width, and height
axswitch = plt.axes([0.40, 0.07, 0.2, 0.05])
bswitch = Button(axswitch, 'Switch graph')
bswitch.on_clicked(callback.switch)

# Connect to a "quit" Button, setting its left, top, width, and height
axquit = plt.axes([0.40, 0.01, 0.2, 0.05])
bquit = Button(axquit, 'Quit')
bquit.on_clicked(callback.quit)

# Show
plt.show()