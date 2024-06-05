import pyxel

class App():
    def __init__(self):
        pyxel.init(128,128,title="Game Of Life", fps=10)
        pyxel.load("game.pyxres")
        self.alive_cells = []
        self.dead_cells = [[i,j] for i in range(0,128) for j in range(0,128) if [i,j] not in self.alive_cells]
        self.cam_x = 0
        self.cam_y = 0
        self.to_dead = []
        self.to_alive = []
        self.mode = 0
        self.rules = [ [[3],[2,3]] , [[1],[0,1,4,5,6,7]] , [[1],[1]] , [[0,1,2,3,4,7,8],[3,4,6,7,8]] ]
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
        '''
        @to_dead : list
        @to_alive : list
        @alive_cells : list
        @dead_cells : list

        change l'état d'une cellule
        '''
        self.to_dead = []
        self.to_alive = []
        for cell in self.alive_cells:
            if self.mode == 1:
                if self.prox(cell[0], cell[1])!=2 and self.prox(cell[0], cell[1])!=3:
                    self.to_dead.append(cell)
            elif self.mode == 2:
                if self.prox(cell[0], cell[1])!=0 and self.prox(cell[0], cell[1])!=1 and self.prox(cell[0], cell[1])!=4 and self.prox(cell[0], cell[1])!=5 and self.prox(cell[0], cell[1])!=6 and self.prox(cell[0], cell[1])!=7:
                    self.to_dead.append(cell)
            elif self.mode == 3:
                if self.prox(cell[0], cell[1])!=1:
                    self.to_dead.append(cell)
            elif self.mode == 4:
                if self.prox(cell[0], cell[1])!=3 and self.prox(cell[0], cell[1])!=4 and self.prox(cell[0], cell[1])!=6 and self.prox(cell[0], cell[1])!=7 and self.prox(cell[0], cell[1])!=8:
                    self.to_dead.append(cell)
                    
        for cell in self.dead_cells:
            if self.mode ==1:
                if self.prox(cell[0], cell[1])==3:
                    self.to_alive.append(cell)
            elif self.mode == 2:
                if self.prox(cell[0], cell[1])==1:
                    self.to_alive.append(cell)
            elif self.mode == 3:
                if self.prox(cell[0], cell[1])==1:
                    self.to_alive.append(cell)
            elif self.mode == 4: #0123478
                if self.prox(cell[0], cell[1])==0 or self.prox(cell[0], cell[1])==1 or self.prox(cell[0], cell[1])==2 or self.prox(cell[0], cell[1])==3 or self.prox(cell[0], cell[1])==4 or self.prox(cell[0], cell[1])==7 or self.prox(cell[0], cell[1])==8:
                    self.to_alive.append(cell)

        for cell in self.to_alive:
            self.dead_cells.remove(cell)
            self.alive_cells.append(cell)
        for cell in self.to_dead:
            self.alive_cells.remove(cell)
            self.dead_cells.append(cell)

    def selectionner(self) :
        '''
        @alive_cell : list
        @dead_cells : list
        change le statut de la cellule cliquée quand la simulation est en pause
        '''
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
            self.cam_y+=5
        elif pyxel.btnr(pyxel.KEY_LEFT):
            self.cam_x-=5
        elif pyxel.btnr(pyxel.KEY_RIGHT):
            self.cam_x+=5
        pyxel.camera(self.cam_x, self.cam_y)

    def menu(self):
        '''
        @menu_stat : bool
        @mode : int
        permet la selection de la règle du jeu de la vie en changeant @mode puis met @menu_stat à True pour lancer la simulation
        '''
        if pyxel.btn(pyxel.KEY_RETURN):
            self.menu_stat = False
        if pyxel.mouse_x>5 and pyxel.mouse_x<21 and pyxel.mouse_y>65 and pyxel.mouse_y<81 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mode = 1 #B3/S23 -> Conway's Game Of Life
            self.menu_stat = False
        elif pyxel.mouse_x>65 and pyxel.mouse_x<81 and pyxel.mouse_y>65 and pyxel.mouse_y<81 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mode = 2 #B1/S014567 -> Fuzz
            self.menu_stat = False
        elif pyxel.mouse_x>5 and pyxel.mouse_x<21 and pyxel.mouse_y>110 and pyxel.mouse_y<126 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mode = 3 #B1/S1 -> Gnari
            self.menu_stat = False
        elif pyxel.mouse_x>65 and pyxel.mouse_x<81 and pyxel.mouse_y>110 and pyxel.mouse_y<126 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mode = 4 #B0123478/S34678 -> InverseLife
            self.menu_stat = False

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
            pyxel.blt(5,65,0,0,0,16,16)
            pyxel.blt(65,65,0,16,0,16,16)
            pyxel.blt(5,110,0,0,16,16,16)
            pyxel.blt(65,110,0,16,16,16,16)

        else:
            pyxel.text(5,5,'mode:'+str(self.mode),7)
            for cell in self.alive_cells:
                pyxel.rect(cell[0]*2, cell[1]*2, 2,2, 7)
            pyxel.rect(-5,-5,266,5,5)
            pyxel.rect(-5,-5,5,266,5)
            pyxel.rect(261,-5,5,266,5)
            pyxel.rect(-5,256,266,5,5)
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 2,2,5)

App()
