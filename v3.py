import pyxel

class App():

    def __init__(self):
        pyxel.init(128,128, title='Game Of Life')
        self.alive_cells = []
        self.dead_cells = [[i,j] for i in range(128) for j in range(128)]
        for cell in self.alive_cells:
            self.dead_cells.remove(cell)
        self.cam_x = 0
        self.cam_y = 0
        self.jeu_lancé = False
        pyxel.run(self.update, self.draw)
    
    def cam_change(self):
        if pyxel.btnr(pyxel.KEY_UP):
            self.cam_x-=10
        elif pyxel.btnr(pyxel.KEY_DOWN):
            self.cam_y+=10
        elif pyxel.btnr(pyxel.KEY_LEFT):
            self.cam_x-=10
        elif pyxel.btnr(pyxel.KEY_RIGHT):
            self.cam_x+=10
        pyxel.camera(self.cam_x, self.cam_y)
    
    def selectionner(self) :
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            if not [(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2] in self.alive_cells :
                self.alive_cells.append([(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2])
                self.dead_cells.remove([(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2])
            else :
                self.dead_cells.append([(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2])
                self.alive_cells.remove([(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2])
            
    def prox(self,x_cell, y_cell):
        cpt = 0
        if [x_cell+1, y_cell+1] in self.alive_cells:
            cpt+=1
        if [x_cell, y_cell+1] in self.alive_cells:
            cpt+=1
        if [x_cell+1, y_cell] in self.alive_cells:
            cpt+=1
        if [x_cell-1, y_cell+1] in self.alive_cells:
            cpt+=1
        if [x_cell-1, y_cell] in self.alive_cells:
            cpt+=1
        if [x_cell-1, y_cell-1] in self.alive_cells:
            cpt+=1
        if [x_cell, y_cell-1] in self.alive_cells:
            cpt+=1
        if [x_cell+1, y_cell-1] in self.alive_cells:
            cpt+=1
        return cpt

    def alive_to_dead(self):
        to_dead = []
        for cell in self.alive_cells:
            if self.prox(cell[0], cell[1]) != 2 or self.prox(cell[0], cell[1]) != 3:
                to_dead.append(cell)
        return to_dead


    def dead_to_alive(self):
        to_alive = []
        for cell in self.dead_cells:
            if self.prox(cell[0], cell[1]) == 2:
                to_alive.append(cell)
        return to_alive
    
    def change_status(self):
        dead = self.alive_to_dead()
        alive = self.dead_to_alive()

        for cell in dead:
            self.dead_cells.append(cell)

        for cell in alive:
            self.alive_cells.append(cell)


    def update(self):
        self.cam_change()
        self.selectionner()
        self.change_status()

    def draw(self):
        pyxel.cls(1)
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 2,2,7)
        for cell in self.alive_cells:
            pyxel.rect(cell[0]*2, cell[1]*2, 2,2, 7)

App()
