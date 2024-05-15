import pyxel as pyx


height = 128
width = 128
alive_cells = [[15,15],[15,16],[15,14]]
dead_cells = [[i,j] for i in range(128) for j in range(128)]
for cell in alive_cells:
    dead_cells.remove(cell)
color = 7



pyx.init(height=height,width=width,title="Game Of Life", fps=1)

def prox(x_cell, y_cell):
    cpt = 0
    if [x_cell+1, y_cell+1] in alive_cells:
        cpt+=1
    elif [x_cell, y_cell+1] in alive_cells:
        cpt+=1
    elif [x_cell+1, y_cell] in alive_cells:
        cpt+=1
    elif [x_cell-1, y_cell+1] in alive_cells:
        cpt+=1
    elif [x_cell-1, y_cell] in alive_cells:
        cpt+=1
    elif [x_cell-1, y_cell-1] in alive_cells:
        cpt+=1
    elif [x_cell, y_cell-1] in alive_cells:
        cpt+=1
    elif [x_cell+1, y_cell-1] in alive_cells:
        cpt+=1
    if cpt != 0:
        return cpt
    else:
        return False

def update():
    for cell in alive_cells:
        if prox(cell[0], cell[1]) == False or prox(cell[0], cell[1])>3 or prox(cell[0], cell[1])<2:
            alive_cells.remove(cell)
    print(alive_cells)

def draw():
    pyx.cls(0)
    for cell in alive_cells:
        pyx.rect(cell[0], cell[1], 1,1, color)

pyx.run(update, draw)