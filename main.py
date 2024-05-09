import pyxel as pyx


height = 500
width = 500
cells = [[15,15],[30,30],[45,45]]
color = 7

pyx.init(height=height,width=width,title="Game Of Life")

def prox(x_cell, y_cell):
    if pyx.pget(x_cell-2, y_cell+2) == color:
        return True
    elif pyx.pget(x_cell+2, y_cell-2) == color:
        return True    
    elif pyx.pget(x_cell+6, y_cell+2) == color:
        return True
    elif pyx.pget(x_cell+6, y_cell+6) == color:
        return True

def update():
    for cell in cells:
        if prox(cell[0], cell[1]) == False:
            cells.remove(cell)

def draw():
    for cell in cells:
        pyx.rect(cell[0], cell[1], 4,4, color)

pyx.run(update, draw)