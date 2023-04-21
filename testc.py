from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
from random import randint


# new forward button callback => gets triggered, when forward button gets pushed
def customForward(*args):
    ax = plt.gca()
    fig = plt.gcf()

    # get line object...
    line = ax.get_lines()[0]

    # ...create some new random data...
    newData = [randint(1, 10), randint(1, 10), randint(1, 10)]

    # ...and update displayed data
    line.set_ydata(newData)
    ax.set_ylim(min(newData), max(newData))
    # redraw canvas or new data won't be displayed
    fig.canvas.draw()


# monkey patch forward button callback
NavigationToolbar2Tk.forward = customForward

# plot first data
plt.plot([1, 2, 3], [1, 2, 3])
plt.show()