import numpy as np
import grid
from Tkinter import *
from graphics import color_rgb
import defaultagent
import customagent

def left(arr,i,j):
    if(arr[i][j-1] != -1):
        arr[i][j-1] += 1

def right(arr,i,j):
    if(arr[i][j+1] != -1):
        arr[i][j+1] += 1

def up(arr,i,j):
    if(arr[i-1][j] != -1):
        arr[i-1][j] += 1

def down(arr,i,j):
    if(arr[i+1][j] != -1):
        arr[i+1][j] += 1

def bottomleft(arr,i,j):
    if(arr[i+1][j-1] != -1):
        arr[i+1][j-1] += 1

def topleft(arr,i,j):
    if(arr[i-1][j-1] != -1):
        arr[i-1][j-1] += 1

def bottomright(arr,i,j):
    if(arr[i+1][j+1] != -1):
        arr[i+1][j+1] += 1

def topright(arr,i,j):
    if(arr[i-1][j+1] != -1):
        arr[i-1][j+1] += 1


def make2DArray(dimension,number_of_mines):
    total = dimension*dimension
    arr = []
    for i in range(0,number_of_mines):
        arr.append(-1)
    for i in range(number_of_mines,total):
        arr.append(0)
    np.random.shuffle(arr)
    arr = np.array(arr).reshape(dimension,dimension)
    return arr


def setup(dimension,number_of_mines):
    grid = make2DArray(dimension,number_of_mines)
    for i in range(0,dimension):
        for j in range(0,dimension):
            if(i == 0 and j == 0 and grid[i][j] == -1):
                down(grid,i,j)
                right(grid,i,j)
                bottomright(grid,i,j)

            if(i == dimension-1 and j == dimension-1 and grid[i][j] == -1):
                up(grid,i,j)
                left(grid,i,j)
                topleft(grid,i,j)

            if(i == 0 and j == dimension-1 and grid[i][j] == -1):
                down(grid,i,j)
                left(grid,i,j)
                bottomleft(grid,i,j)

            if(i == dimension-1 and j == 0 and grid[i][j] == -1):
                up(grid,i,j)
                right(grid,i,j)
                topright(grid,i,j)

            if(i == 0 and j > 0 and j < dimension-1 and grid[i][j] == -1):
                down(grid,i,j)
                bottomleft(grid,i,j)
                bottomright(grid,i,j)
                left(grid, i,j)
                right(grid ,i, j)

            if(i == dimension-1 and j > 0 and j < dimension-1 and grid[i][j] == -1):
                up(grid,i,j)
                right(grid,i,j)
                left(grid,i,j)
                topleft(grid,i,j)
                topright(grid,i,j)

            if(j == 0 and i > 0 and i < dimension-1 and grid[i][j] == -1):
                up(grid,i,j)
                right(grid,i,j)
                down(grid,i,j)
                topright(grid,i,j)
                bottomright(grid,i,j)

            if(j == dimension-1 and i > 0 and i < dimension-1 and grid[i][j] == -1 ):
                up(grid,i,j)
                down(grid,i,j)
                left(grid,i,j)
                topleft(grid,i,j)
                bottomleft(grid,i,j)

            if (i > 0 and i < dimension-1 and j > 0 and j < dimension-1 and grid[i][j] == -1):
                left(grid,i,j)
                right(grid,i,j)
                up(grid,i,j)
                down(grid,i,j)
                bottomleft(grid,i,j)
                bottomright(grid,i,j)
                topleft(grid,i,j)
                topright(grid,i,j)
    #print(grid)
    return grid
