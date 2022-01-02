from random import randint

def fin(ecran:list)->bool:
    """Vérifie que toutes les cases sont reliées entre-elles"""
    for i in range(1,len(ecran)-1,2):
        for j in range(1,len(ecran[0])-1,2):
            if ecran[i][j]!=ecran[1][1]:
                return True

def genere_labyrinthe(nb_carres:int, prc_degradation:int=0) -> list:
    """Génère le labyrinthe"""

    #On fait un tableau rempli de cases contenant des couleurs aléatoires
    ecran = []
    ligne = []
    numeros = []
    for i in range(nb_carres):
        for j in range(nb_carres):
            col = [randint(0, 255), randint(0, 255), randint(0, 255)]
            while col in numeros:
                col = [randint(0, 255), randint(0, 255), randint(0, 255)]
            ligne.append(col)
            numeros.append(col)
        ecran.append(ligne)
        ligne = []

    #On une grille qui sert de murs
    for i in range(len(ecran)):
        for j in range(len(ecran[0])):
            if not(i%2==1 and j%2==1):
                ecran[i][j]=1

    #Tant que les cases du labyrinthes ne sont pas toutes connectées entre elles
    while fin(ecran):

        #On prend deux cases séparées par mur
        x = randint(0,100000)%(len(ecran)-2)+1
        if x%2==0:
            y = ((randint(0,100000)%((len(ecran)-1)//2))) *2+1
        else:
            y = ((randint(0, 100000) % ((len(ecran) - 2) // 2))) * 2 + 2

        if ecran[x-1][y]==1:
            cell_1 = ecran[x][y-1]
            cell_2 = ecran[x][y+1]
        else:
            cell_1 = ecran[x-1][y]
            cell_2 = ecran[x+1][y]

        #Si ces deux cellules sont différentes on casse le mur
        if cell_1 != cell_2:
            ecran[x][y] = cell_2

            #On met toutes les cases qui sont reliées de la même couleur
            for i in range(1,len(ecran)-1,2):
                for j in range(1,len(ecran)-1,2):
                    if ecran[i][j]==cell_1:
                        ecran[i][j]=cell_2


    #On met toutes les cases qui ne sont pas des murs en blanc
    for i in range(len(ecran)):
        for j in range(len(ecran)):
            if ecran[i][j]!=1:
                ecran[i][j]=0

    if prc_degradation>0:
        murs_cassables = []
        for i in range(1,len(ecran)-1):
            for j in range(1,len(ecran)-1):
                if ((i%2==0 and j%2==1) or (i%2==1 and j%2==0)) and ecran[i][j]==1:
                    murs_cassables.append((i,j))
        if prc_degradation>100:
            prc_degradation = 100
        nb_murs_a_casser = round(prc_degradation/100 * len(murs_cassables))

        for i in range(nb_murs_a_casser):
            d = randint(0,len(murs_cassables)-1)
            y,x = murs_cassables[d][0],murs_cassables[d][1]
            ecran[y][x] = 0
            murs_cassables.pop(d)

    ecran[-1][-2]=2
    return ecran
