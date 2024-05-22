import pyxel as pyx


height = 128
width = 128
alive_cells = [[15,15],[15,16],[15,17]]
dead_cells = [[i,j] for i in range(128) for j in range(128)]
print(dead_cells[:10])
for cell in alive_cells:
    dead_cells.remove(cell)
color = 7
cpt_t = 0


pyx.init(height=height,width=width,title="Game Of Life", fps=1)

def prox(x_cell, y_cell):
    cpt = 0
    if [x_cell+1, y_cell+1] in alive_cells:
        cpt+=1
    if [x_cell, y_cell+1] in alive_cells:
        cpt+=1
    if [x_cell+1, y_cell] in alive_cells:
        cpt+=1
    if [x_cell-1, y_cell+1] in alive_cells:
        cpt+=1
    if [x_cell-1, y_cell] in alive_cells:
        cpt+=1
    if [x_cell-1, y_cell-1] in alive_cells:
        cpt+=1
    if [x_cell, y_cell-1] in alive_cells:
        cpt+=1
    if [x_cell+1, y_cell-1] in alive_cells:
        cpt+=1
    return cpt      

def update():
    print(prox(15,16))
    global cpt_t
    if cpt_t%2 == 0:
        to_dead = []
        to_alive = []
        for cell in alive_cells:
            if prox(cell[0], cell[1])!=2 and prox(cell[0], cell[1])!=3:
                to_dead.append(cell)
        for cell in dead_cells:
            if prox(cell[0], cell[1])==3:
                to_alive.append(cell)
        for cell in to_alive:
            dead_cells.remove(cell)
            alive_cells.append(cell)
        for cell in to_dead:
            alive_cells.remove(cell)
            dead_cells.append(cell)
    cpt_t+=1

def draw():
    pyx.cls(0)
    for cell in alive_cells:
        pyx.rect(cell[0], cell[1], 1,1, color)

pyx.run(update, draw)