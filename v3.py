import pyxel

class App():
    def __init__(self):
        pyxel.init(128,128,title="Game Of Life", fps=10)
        self.alive_cells = []
        self.dead_cells = [[i,j] for i in range(0,128) for j in range(0,128) if [i,j] not in self.alive_cells]
        self.cam_x = 0
        self.cam_y = 0
        self.to_dead = []
        self.to_alive = []
        self.jeu_lance = False
        self.menu_stat = True
        pyxel.run(self.update, self.draw)

    def prox(self,x_cell, y_cell):
        '''

        @x_cell : int
        @y_cell : int
        @cpt : int

        agrémente de 1 @cpt pour chaque cellule vivante autours de @x_cell, @y_cell

        '''
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

    def change_stat(self):
        self.to_dead = []
        self.to_alive = []
        for cell in self.alive_cells:
            if self.prox(cell[0], cell[1])!=2 and self.prox(cell[0], cell[1])!=3:
                self.to_dead.append(cell)
        for cell in self.dead_cells:
            if self.prox(cell[0], cell[1])==3:
                self.to_alive.append(cell)
        for cell in self.to_alive:
            self.dead_cells.remove(cell)
            self.alive_cells.append(cell)
        for cell in self.to_dead:
            self.alive_cells.remove(cell)
            self.dead_cells.append(cell)

    def selectionner(self) :
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            if not [(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2] in self.alive_cells :
                self.alive_cells.append([(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2])
                self.dead_cells.remove([(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2])
            else :
                self.dead_cells.append([(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2])
                self.alive_cells.remove([(self.cam_x+pyxel.mouse_x)//2,(self.cam_y+pyxel.mouse_y)//2])

    def cam_change(self):
        '''
        @self.cam_x : int
        @self.cam_y : int
        change les coordonnées du coin supérieur gauche en fonction des flèches pressées
        '''
        if pyxel.btnr(pyxel.KEY_UP):
            self.cam_y-=5
        elif pyxel.btnr(pyxel.KEY_DOWN):
            self.cam_yy+=5
        elif pyxel.btnr(pyxel.KEY_LEFT):
            self.cam_yx-=5
        elif pyxel.btnr(pyxel.KEY_RIGHT):
            self.cam_yx+=5
        pyxel.camera(self.cam_x, self.cam_y)

    def menu(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.menu = False


    def update(self):
        if self.menu_stat == False:
            if self.jeu_lance == True :
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.jeu_lance = False
                self.change_stat()
                self.cam_change()

                if pyxel.btnr(pyxel.KEY_RETURN) :
                    self.dead_cells=[[i,j] for i in range(0,128) for j in range(0,128) if [i,j] not in self.alive_cells]
                    self.alive_cells=[]
                    self.jeu_lance=False

            elif self.jeu_lance==False :
                self.selectionner()
                if pyxel.btnr(pyxel.KEY_SPACE) :
                    self.jeu_lance=True
        elif self.menu_stat == True:
            self.menu()

    def draw(self):
        pyxel.cls(0)
        if self.menu_stat == True:
            pyxel.text(5,5, 'Game Of Life', 7)
            pyxel.text(5,20, 'Choose your version', 7)

        else:
            pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 2,2,7)
            for cell in self.alive_cells:
                pyxel.rect(cell[0]*2, cell[1]*2, 2,2, 7)

App()
