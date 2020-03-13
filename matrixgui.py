import numpy as np
import grid
from Tkinter import *
from graphics import color_rgb
import setup

colors = { -1:[0,0,0], 0:[215,255,215] , 1:[135, 206, 235], 2:[0, 128, 0] , 3:[255, 0, 0], 4:[128, 0, 128],
           5:[128, 0, 0], 6 :[64, 224, 208], 7:[255, 192, 203] , 8:[128, 128, 128], 9:[255,255,255]}

'''
n =10
dimension = n
number_of_mines = 20
'''
def matrix_gui(n,val):
    w, gui = grid.buildmaze(n) #now that we have the base w and gui which is each boxes we can start coloring them
    gui = np.array(gui)
    gui = gui.reshape((n,n))
    w.setBackground('white')
    val = np.array(val)


    print(val)
    print(val[0][0])
    for i in range(0,n):
        for j in range( 0 , n):
            #print(arr[i][j])
            #if(val[i][j] == -1):
            #    gui[i][j].setFill(color_rgb(0,0,0))
            #    continue
            c = colors[val[i][j]]
            gridnum = val[i][j]
            #print("this is the value of n: " + str(gridnum))
            #print(val[i][j])
            #print(c[0])
            #print(type(gui[i][j]))
            gui[i][j].setFill(color_rgb(c[0],c[1],c[2]))

            gui[i][j].draw(w)
    w.getMouse()
    w.close()


#matrix_gui(10,setup.setup(10,15))
