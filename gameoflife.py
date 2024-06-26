import pyxel

class App():
    def __init__(self):
        pyxel.init(128,128,title="Game Of Life", fps=20)
        pyxel.load("gameoflife.pyxres")
        self.alive_cells = []
        self.dead_cells = [[i,j] for i in range(0,128) for j in range(0,128) if [i,j] not in self.alive_cells]
        self.cam_x = 0
        self.cam_y = 0
        self.to_dead = []
        self.to_alive = []
        self.mode = 0
        self.rules = ["Conway's Game","Fuzz","Gnari","Inverse Life"]
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
        if [x_cell+1, y_cell+1] in self.alive_cells: #diag bas droit
            cpt+=1
        if [x_cell, y_cell+1] in self.alive_cells: #bas
            cpt+=1
        if [x_cell+1, y_cell] in self.alive_cells: #droite
            cpt+=1
        if [x_cell-1, y_cell+1] in self.alive_cells: #diag inf gauche
            cpt+=1
        if [x_cell-1, y_cell] in self.alive_cells: #gauche
            cpt+=1
        if [x_cell-1, y_cell-1] in self.alive_cells: #diag sup gauche
            cpt+=1
        if [x_cell, y_cell-1] in self.alive_cells: #haut
            cpt+=1
        if [x_cell+1, y_cell-1] in self.alive_cells: #diag sup droit
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

        #vérification de mort de cellule : 

        for cell in self.alive_cells:
            proxi = self.prox(cell[0], cell[1])
            if self.mode == 1: #S23 -> Conway's Game Of Life
                if proxi!=2 and proxi!=3:
                    self.to_dead.append(cell)
            elif self.mode == 2: #S014567 -> Fuzz
                if proxi!=0 and proxi!=1 and proxi!=4 and proxi!=5 and proxi!=6 and proxi!=7:
                    self.to_dead.append(cell)
            elif self.mode == 3: #S1 -> Gnari
                if proxi!=1:
                    self.to_dead.append(cell)
            elif self.mode == 4: #S34678 -> InverseLife
                if proxi!=3 and proxi!=4 and proxi!=6 and proxi!=7 and proxi!=8:
                    self.to_dead.append(cell)
        
        #verification de naissance de cellule :

        for cell in self.dead_cells:
            proxi = self.prox(cell[0], cell[1])
            if self.mode ==1: #B3 -> Conway's Game Of Life
                if proxi==3:
                    self.to_alive.append(cell)
            elif self.mode == 2: #B1 -> Fuzz
                if proxi==1:
                    self.to_alive.append(cell)
            elif self.mode == 3: #B1 -> Gnari
                if proxi==1:
                    self.to_alive.append(cell)
            elif self.mode == 4: #B0123478 -> InverseLife
                if proxi==0 or proxi==1 or proxi==2 or proxi==3 or proxi==4 or proxi==7 or proxi==8:
                    self.to_alive.append(cell)

        #update des listes :

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
        pyxel.camera(self.cam_x, self.cam_y) #change les coordonnées x et y du coin supérieur gauche de la fenetre pyxel.

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
            self.dead_cells = [[i,j] for i in range(0,64) for j in range(0,64) if [i,j] not in self.alive_cells]
        elif pyxel.mouse_x>5 and pyxel.mouse_x<21 and pyxel.mouse_y>110 and pyxel.mouse_y<126 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mode = 3 #B1/S1 -> Gnari
            self.menu_stat = False
            self.dead_cells = [[i,j] for i in range(0,64) for j in range(0,64) if [i,j] not in self.alive_cells]
        elif pyxel.mouse_x>65 and pyxel.mouse_x<81 and pyxel.mouse_y>110 and pyxel.mouse_y<126 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.mode = 4 #B0123478/S34678 -> InverseLife
            self.menu_stat = False
            self.dead_cells = [[i,j] for i in range(0,64) for j in range(0,64) if [i,j] not in self.alive_cells]

    def update(self):
        if self.menu_stat == False:
            if self.jeu_lance == True :
                self.change_stat()
                self.cam_change()

                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.jeu_lance = False

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

            #Conway's Game
            pyxel.blt(5,65,0,0,0,16,16)
            pyxel.text(25,65,"Conway's",7)
            pyxel.text(25,75,"Game",7)

            #Fuzz
            pyxel.blt(65,65,0,16,0,16,16)
            pyxel.text(85,65,"Fuzz",7)

            #Gnari
            pyxel.blt(5,110,0,0,16,16,16)
            pyxel.text(25,110,"Gnari",7)

            #Inverse Life
            pyxel.blt(65,110,0,16,16,16,16)
            pyxel.text(85,110,"Inverse",7)
            pyxel.text(85,120,"Life",7)

        else:
            pyxel.text(5,5,'mode:'+self.rules[self.mode-1],7)
            for cell in self.alive_cells:
                pyxel.rect(cell[0]*2, cell[1]*2, 2,2, 7)
        pyxel.rect(self.cam_x+pyxel.mouse_x, self.cam_y+pyxel.mouse_y, 2,2,5)

App()
