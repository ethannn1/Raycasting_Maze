import pygame
import math
from genere_map import genere_labyrinthe
from time import monotonic
import json

def check_val(val:int,min:int,max:int)->int:
    """ Vérifie que min<val<max"""
    if val<min:
        val=min
    elif val>max:
        val=max
    return val

#Importation des constantes
with open("reglages.json") as const_fichier:
    reglages = json.load(const_fichier)
    const_fichier.close()

#Constantes
COTE = reglages["COTE"]
TAILLE_MAP = reglages["TAILLE_MAP"]
DEGRADATION = reglages["DEGRADATION"]
TAILLE_PARCELLE = 48
RENDER_DIST = reglages["RENDER_DIST"]
OMBRES = reglages["OMBRES"]
DIFF_MOITIE = reglages["DIFF_MOITIE"]
FOV = math.pi /3
RAYONS_DIFF = COTE // 4
SCALE = COTE // RAYONS_DIFF


#On vérifie que les constantes appartiennent à certains intervalles pour éviter certains bugs
if TAILLE_MAP%2==0:
    TAILLE_MAP-=1
TAILLE_MAP = check_val(TAILLE_MAP,5,99)
COTE = check_val(COTE, 360, 1080)
DEGRADATION = check_val(DEGRADATION, 0, 100)
RENDER_DIST = check_val(RENDER_DIST,100,COTE**2)

MAP = genere_labyrinthe(TAILLE_MAP, DEGRADATION)

player_x = 50
player_y = 50
player_angle = math.pi

#Initialisation de la fenêtre
pygame.init()
screen = pygame.display.set_mode((COTE, COTE))
pygame.display.set_caption("Raycasting")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial Rounded MT",int(COTE/14.4))
font2 = pygame.font.SysFont("Arial Rounded MT",int(COTE/10))

def affiche_map() -> None:
    """Affiche la map en 2D en haut à gauche de l'écran"""
    taille_map_2D = (round(math.sqrt(TAILLE_MAP)) + 2*(720/COTE))

    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, TAILLE_PARCELLE * TAILLE_MAP / taille_map_2D, TAILLE_PARCELLE * TAILLE_MAP / taille_map_2D))
    for i in range(TAILLE_MAP):
        for j in range(TAILLE_MAP):
            if MAP[i][j]==0:
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(j * TAILLE_PARCELLE / taille_map_2D, i * TAILLE_PARCELLE / taille_map_2D, TAILLE_PARCELLE / taille_map_2D, TAILLE_PARCELLE / taille_map_2D))
            elif MAP[i][j]==1:
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(j * TAILLE_PARCELLE / taille_map_2D, i * TAILLE_PARCELLE / taille_map_2D, TAILLE_PARCELLE / taille_map_2D, TAILLE_PARCELLE / taille_map_2D))
            else:
                pygame.draw.rect(screen, (0,0,255), pygame.Rect(j * TAILLE_PARCELLE / taille_map_2D, i * TAILLE_PARCELLE / taille_map_2D, TAILLE_PARCELLE / taille_map_2D, TAILLE_PARCELLE / taille_map_2D))
    pygame.draw.circle(screen,(255,0,0),(player_y/taille_map_2D,player_x/taille_map_2D),2)

def affiche_murs() -> None:

    angle_dep = player_angle - FOV/2
    for i in range(RAYONS_DIFF): #Pour chaque colonne de pixel de l'écran
         for profondeur in range(0,RENDER_DIST,int(DIFF_MOITIE)+1):#Pour chaque pixel de cette colonne
             target_x = player_x - math.sin(angle_dep) * profondeur #On calcule les coordonnées du pixel visé
             target_y = player_y + math.cos(angle_dep) * profondeur
             col = int(target_x // TAILLE_PARCELLE) #On calcule la position sur la map en 2D
             row = int(target_y // TAILLE_PARCELLE)
             if MAP[col][row] != 0: # Si on atteint un mur
                 profondeur *= math.cos(player_angle-angle_dep) # Corrige l'effet fish eye
                 wall_height = COTE*27 / (profondeur+0.0001) # Calcule la hauteur du mur

                 # Génère la couleur des murs
                 if OMBRES:
                    c = 200/(1+profondeur**2*0.0005)
                 else:
                     c = 0

                 if MAP[col][row]==1:
                     color = 3*[c]
                 else:
                     color = [0,255,255]

                 pygame.draw.rect(screen, color, (0 + i * SCALE, (COTE / 2) - (wall_height / 2), SCALE, wall_height)) # On affiche la projection
                 break

         angle_dep += FOV / RAYONS_DIFF #On change l'angle

temps_debut = monotonic()
forward = True
Jeu = True
while Jeu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            Jeu = False

    #On vérifie les collisions
    col = int(player_x // TAILLE_PARCELLE)
    row = int(player_y // TAILLE_PARCELLE)
    if MAP[col][row] == 1:
        if forward:
            player_x -= -math.sin(player_angle)
            player_y -= math.cos(player_angle)
        else:
            player_x += -math.sin(player_angle)
            player_y += math.cos(player_angle)

    if MAP[col][row] == 2: #Le jeu se termine quand on atteint la porte
        Jeu=False

    pygame.draw.rect(screen, (200, 200, 200), (0, 0, COTE,  COTE))
    pygame.draw.rect(screen, (100, 100, 100), (0, COTE / 2, COTE, COTE))

    affiche_murs()

    #Entrée des touches
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player_angle -= 0.05
    if keys[pygame.K_d]:
        player_angle += 0.05
    if keys[pygame.K_z]:
        forward = True
        player_x += -math.sin(player_angle)
        player_y += math.cos(player_angle)
    if keys[pygame.K_s]:
        forward = False
        player_x -= -math.sin(player_angle)
        player_y -= math.cos(player_angle)
    if keys[pygame.K_m]:
        affiche_map()

    #Affichage du chrono
    temps = monotonic()-temps_debut
    nb_minutes = str(round(temps//59))
    nb_secondes = str(round(temps%59))
    if nb_minutes==0:
        texte = font.render(nb_secondes, True, (255, 255, 255))
    else:
        texte = font.render(nb_minutes+":"+nb_secondes,True,(255,255,255))
    screen.blit(texte,(COTE-COTE/7,0))

    #Actualisation de la fenêtre
    pygame.display.flip()
    clock.tick(60)

temps_final = monotonic()-temps_debut
minutes_f = str(round(temps_final//60))
secondes_f = str(round(temps_final%60))

#Écran de fin
Fin = False
while not Fin:

    texte2 = font2.render("Labyrinthe terminé !",True,(255,255,255))
    screen.blit(texte2,(COTE//7,COTE//7))

    texte3 = font.render("Vous l'avez fini en "+minutes_f+" minutes et "+secondes_f+" secondes.",True,(255,255,255))
    screen.blit(texte3,(0,int(COTE//3.5)))

    pygame.display.flip()
    screen.fill((0,0,0))
    clock.tick(60)