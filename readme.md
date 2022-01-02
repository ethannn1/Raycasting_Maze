# RAYCASTING_MAZE

## Description :
C'est un jeu où le but est simple : sortir du labyrinthe.  
On ne peut que se déplacer et tourner la tête pour trouver la sortie  
(ou afficher la carte du labyrinthe si on aime tricher).  
La génération du labyrinthe est personnalisable et complètement aléatoire.


## Commandes :
- Z : Avancer
- Q : Pivoter à gauche
- S : Reculer
- D : Pivoter à droite
- M : Afficher la map

## Réglages :
- Aller dans le fichier "reglages.json"
- "COTE" Permet de régler la taille du côté de la fenêtre. 
- "TAILLE_MAP" Permet de régler la taille de la carte.
- "DEGRADATION" Permet de déterminer le pourcentage de dégradation du labyrinthe.
- "RENDER_DIST" La distance d'affichage, baisser si le jeu n'est pas fluide
- "OMBRES" Permet de choisir si on veut des ombres sur les murs.
- "DIFF_MOITIE" Permet de diffuser que la moitié des rayons. (Utile en cas de lag)

## Idées d'amélioration :
- Rajouter des textures sur les murs
- Mettre un sol et un ciel
- Mettre un menu pour les réglages

## Prototypage des fonctions :
### genere_map :
- fin(list) -> bool : sert pour la génération du labyrinthe, renvoie True quand il est parfait
- genere_labyrinthe(int,int) -> list : renvoie un labyrinthe complexe généré aléatoirement sous forme de liste de liste de la taille qu'on veut avec le pourcentage de dégradation qu'on veut. 

### main :
- check_val(int,int,int) -> int : Vérifie qu'une valeur soit dans une intervalle donnée
- affiche_map() -> None : Affiche dans le coin supérieur gauche de l'écran la map en 2D du jeu, fonctionne que dans main.py car elle ne prend aucune valeur en paramètre et utilise les variables du programme.
- affiche_murs() -> None : Utilise le raycasting pour afficher les murs du labyrinthe en 3D, fonctionne aussi que dans main.py
