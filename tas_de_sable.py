import tkinter as tk

N = 3
HAUTEUR = 500
LARGEUR = 500

COUL_MUR = "black"
COUL_VIDE = "white"

racine = tk.Tk()
canvas = tk.Canvas(racine,)
canvas.grid()



P = 0.5


terrain = []
grille = []


def init_terrain():
    global grille, terrain
    grille = []
    terrain = []
    for i in range(N):
        grille.append([0]*N)
        terrain.append([0]*N)
    
    for i in range(N):
        for j in range(N):
            if rd.uniform(0, 1) < P:
                terrain[i][j] = 1
                coul = COUL_MUR
            else:
                terrain[i][j] = 0
                coul = COUL_VIDE
            largeur = LARGEUR // N 
            hauteur = HAUTEUR // N 
            x1 = largeur * i
            y1 = hauteur * j
            x2 = largeur * (i+1)
            y2 = hauteur * (j+1)
            carre = canvas.create_rectangle((x1, y1),(x2, y2),fill=coul)
            grille[i][j] = carre
    




############################################################

def init_terrain():
    grille = [1, 2, 3]
    for i in range(N):
    for j in range(N):
        if rd.uniform(0,1) < P:
            terrain[i] [j] = 1 
            couleur = COUL_MUR
        else :
            couleur = COUL_VIDE



hauteur = HAUTEUR // N 
x0, y0 = i * largeur, j * hauteur
canvas.create_rectangle((x0, y0), (x1, y1), fill=couleur)





