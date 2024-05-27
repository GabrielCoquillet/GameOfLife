import pyxel as pyx


size = 128
alive_cells = [[15,15],[16,16],[16,17],[15,17],[14,17]]
dead_cells = [[i,j] for i in range(128) for j in range(128)]
print(dead_cells[:10])
for cell in alive_cells:
    dead_cells.remove(cell)
color = 7
cpt_t = 0
cam_x , cam_y = 0, 0
jeu_lancé = False


pyx.init(height=size,width=size,title="Game Of Life", fps=5)

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

def menu():
    pass

def selectionner() :
    if pyx.btnr(pyx.MOUSE_BUTTON_LEFT) :
        if not [(cam_x+pyx.mouse_x)//2,(cam_y+pyx.mouse_y)//2] in alive_cells :
            alive_cells.append([(cam_x+pyx.mouse_x)//2,(cam_y+pyx.mouse_y)//2])
            dead_cells.remove([(cam_x+pyx.mouse_x)//2,(cam_y+pyx.mouse_y)//2])
        else :
            dead_cells.append([(cam_x+pyx.mouse_x)//2,(cam_y+pyx.mouse_y)//2])
            alive_cells.remove([(cam_x+pyx.mouse_x)//2,(cam_y+pyx.mouse_y)//2])


def editor(alive, dead):
    pass

def cam_change(x, y):
    if pyx.btnr(pyx.KEY_UP):
        y-=10
    elif pyx.btnr(pyx.KEY_DOWN):
        y+=10
    elif pyx.btnr(pyx.KEY_LEFT):
        x-=10
    elif pyx.btnr(pyx.KEY_RIGHT):
        x+=10
    pyx.camera(x, y)
    return x, y

def dead_to_alive() :
    pass

def update():

    global cam_x, cam_y, jeu_lancé, alive_cells, dead_cells

    if jeu_lancé == True :
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
        if menu == True:
            menu()
        if editor == True:
            editor(alive_cells, dead_cells)
        cam_x, cam_y = cam_change(cam_x, cam_y)

        if pyx.btnr(pyx.KEY_RETURN) :
            dead_cells=[[i,j] for i in range(128) for j in range(128)]
            alive_cells=[]
            jeu_lancé=False

    elif jeu_lancé==False :
        pyx.mouse(True)
        selectionner()
        if pyx.btnr(pyx.KEY_SPACE) :
            jeu_lancé=True

def draw():
    pyx.cls(0)
    #borders
    pyx.rect(-2,-2,260,260,13)
    pyx.rect(0,0,256,256,0)


    for cell in alive_cells:
        pyx.rect(cell[0]*2, cell[1]*2, 2,2, color)

pyx.run(update, draw)
