###########################
# Auteur: Pierre Coucheney


###########################
# import des modules
import tkinter as tk
import copy
import random as rd


############################
# constantes

# taille de la grille carrée
N = 100
# dimensions du canvas et de la grille
LARGEUR = 450
HAUTEUR = 450
LARGEUR_CASE = LARGEUR // N
HAUTEUR_CASE = HAUTEUR // N


#########################################
# variables globales en plus des widgets

# objets graphiques représentant la grille dans un tableau 2D
grille = None
# configuration courante dans un tableau 2D de dimension N+2
# pour tenir compte des bords
config_cur = None
# deux variables booléeennes por savoir si il faut
# ajouter ou soustraire la config
# créée quand on clique dessus
add_active = False
sous_active = False
# variable booléenne pour savoir si le mode cinéma est actif ou pas
arret = True
# identifiant de la méthode after qui sert à pouvoir
# arrêter le compte à rebours
id_after = 0


############################
# fonctions

def choix_couleur(n):
    """Retourne une couleur à partir de l'entier n"""
    liste_col = ["black", "yellow", "green", "blue"]
    if n < 4:
        return liste_col[n]
    else:
        return "grey" + str(min(n + 20, 100))


def init_grille():
    """Retourne une grille carrée vide
       dimension N+2, les éléments de la configuration vont de 1 à N
       les indices 0 et N+1 sont les bords et permettent de ne pas gérer
       de cas particuliers
    """
    global grille, config_cur
    grille = [[0 for i in range(N+2)] for j in range(N+2)]
    config_cur = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N+1):
        x = (i - 1) * LARGEUR_CASE
        for j in range(1, N+1):
            y = (j - 1) * HAUTEUR_CASE
            col = "black"
            carre = canvas.create_rectangle(x, y, x+LARGEUR_CASE,
                                            y+HAUTEUR_CASE, fill=col,
                                            outline="grey50")
            grille[i][j] = carre


def affiche_grille(config):
    """Affiche la configuration donnée"""
    for i in range(1, N+1):
        for j in range(1, N+1):
            col = choix_couleur(config[i][j])
            canvas.itemconfigure(grille[i][j], fill=col)


def avalanche(config, i, j):
    """Fait l'avalanche de la case (i, j)
        pour la config donnée, modifie directement la config
    """
    n = config[i][j]
    if n >= 4:
        config[i-1][j] += 1
        config[i+1][j] += 1
        config[i][j-1] += 1
        config[i][j+1] += 1
        config[i][j] -= 4


def avalanche_efficace(config, i, j):
    """Fait toutes les avalanches de la case (i, j)
        pour la config donnée, modifie directement la config
    """
    n = config[i][j]
    q, r = n // 4, n % 4
    if n >= 4:
        config[i-1][j] += q
        config[i+1][j] += q
        config[i][j-1] += q
        config[i][j+1] += q
        config[i][j] = r


def etape_efficace(config):
    """Fait une étape de l'automate;
        retourne True si modif, False sinon
        utilise la propriété de commutativité pour accélérer la stabilization
    """
    modif = False
    for i in range(1, N+1):
        for j in range(1, N+1):
            if config[i][j] >= 4:
                avalanche_efficace(config, i, j)
                modif = True
    return modif


def etape(config):
    """Fait une étape de l'automate;
        retourne True si modif, False sinon
    """
    config_copy = copy.deepcopy(config)
    modif = False
    for i in range(1, N+1):
        for j in range(1, N+1):
            if config_copy[i][j] >= 4:
                avalanche(config, i, j)
                modif = True
    return modif


def stabilize():
    """Stabilize la configuration config en affichant
        les modifs à chaque étape
    """
    global arret, id_after
    # si la config est stable, on arrête le compte à rebours
    # et on remet le bouton à start
    if not etape(config_cur):
        arret = True
        bouton_start.configure(text="Start")
        return
    affiche_grille(config_cur)
    id_after = canvas.after(100, stabilize)


def stabilize_efficace(config):
    """Stabilize la configuration config"""
    while etape_efficace(config):
        pass


def stabilize_bouton():
    """Stabilization à partit du bouton"""
    stabilize_efficace(config_cur)
    affiche_grille(config_cur)


def addition(c1, c2):
    """Retourne l'addition des deux configs c1 et c2"""
    c_res = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N+1):
        for j in range(1, N+1):
            c_res[i][j] = c1[i][j] + c2[i][j]
    return c_res


def addition_bouton():
    """Addition depuis le bouton"""
    global add_active
    add_active = True


def soustraction(c1, c2):
    """Retourne le résultat de la soustraction de c1 par c2"""
    cres = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N+1):
        for j in range(1, N+1):
            cres[i][j] = max(c1[i][j] - c2[i][j], 0)
    return cres


def soustraction_bouton():
    """Soustraction depuis le bouton"""
    global sous_active
    sous_active = True


def identity():
    """Retourne la configuration identité"""
    config = max_stable()
    config = addition(config, config)
    config2 = copy.deepcopy(config)
    stabilize_efficace(config)
    config = soustraction(config2, config)
    stabilize_efficace(config)
    return config


def identity_bouton():
    """Depuis le bouton identity, modifie la config courante,
       ou fait une opération"""
    global config_cur, add_active, sous_active
    if add_active:
        config_cur = addition(config_cur, identity())
        add_active = False
    elif sous_active:
        config_cur = soustraction(config_cur, identity())
        sous_active = False
    else:
        config_cur = identity()
    affiche_grille(config_cur)


def max_stable():
    """Retourne config Max stable"""
    config = [[3 for i in range(N+2)] for j in range(N+2)]
    return config


def max_stable_bouton():
    """Max stable depuis bouton"""
    global config_cur, add_active, sous_active
    if add_active:
        config_cur = addition(config_cur, max_stable())
        add_active = False
    elif sous_active:
        config_cur = soustraction(config_cur, max_stable())
        sous_active = False
    else:
        config_cur = max_stable()
    affiche_grille(config_cur)


def config_rand():
    """Retourne config random"""
    config = [[rd.randint(0, 3) for i in range(N+2)] for j in range(N+2)]
    return config


def config_rand_bouton():
    """Max stable depuis bouton"""
    global config_cur, add_active, sous_active
    if add_active:
        config_cur = addition(config_cur, config_rand())
        add_active = False
    elif sous_active:
        config_cur = soustraction(config_cur, config_rand())
        sous_active = False
    else:
        config_cur = config_rand()
    affiche_grille(config_cur)


def pile():
    """Retourne config Max stable"""
    config = [[0 for i in range(N+2)] for j in range(N+2)]
    n = input("Entrez le nombre de grains de sable à mettre au milieu\n")
    config[N // 2][N // 2] = int(n)
    return config


def pile_bouton():
    """Max stable depuis bouton"""
    global config_cur, add_active, sous_active
    if add_active:
        config_cur = addition(config_cur, pile())
        add_active = False
    elif sous_active:
        config_cur = soustraction(config_cur, pile())
        sous_active = False
    else:
        config_cur = pile()
    affiche_grille(config_cur)


def start():
    """Démarre ou arrête le mode cinéma lors de la stabilization"""
    global arret
    if arret:
        arret = False
        bouton_start.configure(text="Stop")
        stabilize()
    else:
        arret = True
        bouton_start.configure(text="Start")
        canvas.after_cancel(id_after)


def add_souris(event):
    """Ajoute un grain de sable sur la config couante là où se trouve la souris
    et modifie l'afichage"""
    x, y = event.x, event.y
    i, j = x // LARGEUR_CASE + 1, y // HAUTEUR_CASE + 1
    config_cur[i][j] += 1
    affiche_grille(config_cur)


def sauvegarde():
    """Sauvegarde la config courante dans le fichier sauvegarde"""
    fic = open("sauvegarde", "w")
    fic.write(str(N)+"\n")
    for i in range(1, N+1):
        for j in range(1, N+1):
            fic.write(str(config_cur[i][j]))
            fic.write("\n")
    fic.close()


def load():
    """Charge la configuration sauvegardée et la retourne si
    elle a même valeur N que la config courante, sinon retourne config vide
    """
    fic = open("sauvegarde", "r")
    config = [[0 for i in range(N+2)] for j in range(N+2)]
    ligne = fic.readline()
    n = int(ligne)
    if n != N:
        fic.close()
        return config
    i = j = 1
    for ligne in fic:
        config[i][j] = int(ligne)
        j += 1
        if j == N + 1:
            j = 1
            i += 1
    fic.close()
    return config


def load_bouton():
    """Modifie la config courante à partir de la config sauvegardée,
        ou fait une opération avec cette config
    """
    global config_cur, add_active, sous_active
    if add_active:
        config_cur = addition(config_cur, load())
        add_active = False
    elif sous_active:
        config_cur = soustraction(config_cur, load())
        sous_active = False
    else:
        config_cur = load()
    affiche_grille(config_cur)


############################
# programme principal

racine = tk.Tk()
racine.title("Tas de sable")

# définition des widgets
canvas = tk.Canvas(racine, width=LARGEUR, height=HAUTEUR)
init_grille()
bouton_start = tk.Button(racine, text="Start", command=lambda: start())
bouton_id = tk.Button(racine, text="Identity", command=identity_bouton)
bouton_max = tk.Button(racine, text="Max stable", command=max_stable_bouton)
bouton_stabilize = tk.Button(racine, text="Stabilize",
                             command=stabilize_bouton
                             )
bouton_addition = tk.Button(racine, text="Addition", command=addition_bouton)
bouton_soustraction = tk.Button(racine, text="Soustraction",
                                command=soustraction_bouton
                                )
bouton_sauv = tk.Button(racine, text="Sauvegarde", command=sauvegarde)
bouton_config_sauv = tk.Button(racine, text="Config sauvegardée",
                               command=load_bouton
                               )
label_operation = tk.Label(racine, text="Opérations", bg="blue")
label_config = tk.Label(racine, text="Configurations", bg="blue")
bouton_rand = tk.Button(racine, text="random", command=config_rand_bouton)
bouton_pile = tk.Button(racine, text="Pile centrée", command=pile_bouton)

# placement des widgets
bouton_start.grid(row=6, column=1)
label_config.grid(row=0, column=2)
bouton_id.grid(row=1, column=2)
bouton_max.grid(row=2, column=2)
bouton_rand.grid(row=3, column=2)
bouton_pile.grid(row=4, column=2)
bouton_config_sauv.grid(row=5, column=2)
label_operation.grid(row=0, column=0)
bouton_stabilize.grid(row=1, column=0)
bouton_addition.grid(row=2, column=0)
bouton_soustraction.grid(row=3, column=0)
bouton_sauv.grid(row=4, column=0)
canvas.grid(row=0, column=1, rowspan=6)

# liaison d'événements
canvas.bind("<Button-1>", add_souris)
canvas.bind("<B1-Motion>", add_souris)

# boucle prinicipale
racine.mainloop()
