import pyxel

alive_cells = []
dead_cells = [[i,j] for i in range(0,128) for j in range(0,128) if [i,j] not in alive_cells]
cam_x , cam_y = 0, 0
jeu_lancé = False

pyxel.init(height=128,width=128,title="Game Of Life", fps=10)

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

def change_stat(alive_cells, dead_cells):
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
    return alive_cells, dead_cells

def selectionner() :
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
        if not [(cam_x+pyxel.mouse_x)//2,(cam_y+pyxel.mouse_y)//2] in alive_cells :
            alive_cells.append([(cam_x+pyxel.mouse_x)//2,(cam_y+pyxel.mouse_y)//2])
            dead_cells.remove([(cam_x+pyxel.mouse_x)//2,(cam_y+pyxel.mouse_y)//2])
        else :
            dead_cells.append([(cam_x+pyxel.mouse_x)//2,(cam_y+pyxel.mouse_y)//2])
            alive_cells.remove([(cam_x+pyxel.mouse_x)//2,(cam_y+pyxel.mouse_y)//2])

def cam_change(x, y):
    if pyxel.btnr(pyxel.KEY_UP):
        y-=5
    elif pyxel.btnr(pyxel.KEY_DOWN):
        y+=5
    elif pyxel.btnr(pyxel.KEY_LEFT):
        x-=5
    elif pyxel.btnr(pyxel.KEY_RIGHT):
        x+=5
    pyxel.camera(x, y)
    return x, y

def update():

    global cam_x, cam_y, jeu_lancé, alive_cells, dead_cells

    if jeu_lancé == True :
        if pyxel.btnp(pyxel.KEY_SPACE):
            jeu_lancé = False
        alive_cells, dead_cells = change_stat(alive_cells, dead_cells)
        cam_x, cam_y = cam_change(cam_x, cam_y)

        if pyxel.btnr(pyxel.KEY_RETURN) :
            dead_cells=[[i,j] for i in range(128) for j in range(128)]
            alive_cells=[]
            jeu_lancé=False

    elif jeu_lancé==False :
        selectionner()
        if pyxel.btnr(pyxel.KEY_SPACE) :
            jeu_lancé=True

def draw():
    pyxel.cls(0)
    pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 2,2,7)
    for cell in alive_cells:
        pyxel.rect(cell[0]*2, cell[1]*2, 2,2, 7)

pyxel.run(update, draw)
