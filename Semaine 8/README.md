# Jouons avec les animations
## Créer une application qui animera un widget de votre choix
### Pour chaque animation, expérimenter avec les QEasingCurve
1) Ajouter un QWidget qui contiendra votre QWidget enfant que vous allez animer
2) Ajouter un bouton qui doublera la taille du widget
   1) Petit rappel: le startValue est optionnel
3) Ajouter un bouton pour réduire la taille du widget de moitié
4) Ajouter un bouton qui va exécuter les animations en 2 et 3 en séquence
5) Ajouter un bouton pour bouger le widget vers le coin bas-droit
6) Ajouter un bouton pour bouger le widget vers le coin haut-gauche
7) Ajouter un bouton pour exécuter les animations en 2 et 5 en parallèle

## Créer une application qui animera l'image de chat
1) Utiliser le QPainter pour dessiner le chat dans le répertoire image
2) Pour animer le chat, utiliser un QTimer. Le QTimer permet d'appeler une méthode à chaque X millisecondes
>timer = QTimer()  
>timer.timeout.connect(la_methode_a_appele)  
>timer.start() 
3) Ajouter un mouvement de gauche vers la droite au chat en plus de l'animation des images

## Créer une application pour couper l'image originale en images de chaque "frame"
1) Utiliser un QFileDialog pour sélectionner le fichier
2) Ajouter des widgets permettant de sélectionner la hauteur et largeur de coupe
3) Sauvegarder les nouveaux fichiers avec la nomenclature nom_index.png  
4) L'image chat.png est un exemple de fichier à couper


# Autres exercices à venir