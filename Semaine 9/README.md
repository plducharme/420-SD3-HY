# Gestion des événements

## QMouseEvent
1) Créer une application contenant un canevas
2) Gérer le mouseMoveEvent(self, e: QMouseEvent) pour afficher
   1) globalPos()
   2) localPos()
   3) screenPos()
   4) windowsPos()
   5) Étudier la différence entre chaque position et se ce chaque position représente

## keyPressEvent
1) Créer une application qui permet de contrôler un objet qui se dessinera sur le canevas
2) Utiliser les touches suivantes (voir Exemples/serpents.py)
   1) W = accélérer
   2) S = ralentir
   3) A = rotation vers la gauche
   4) D = rotation vers la droite
3) L'objet devrait être représenté par sa propre classe

## Widget et signal personnalisés
### QBatterie(Qwidget)
1) Créer une application qui va afficher un widget personnalisé sous la forme d'une batterie
2) Le widget aura comme propriétés: minValeur, valeur et maxValeur
   1) Ajouter les getters/setters
3) La méthode paintEvent() peut être redéfinie (override) pour peinturer le widget
	
```
def paintEvent(self, event)
  painter = QPainter(self)
  ...
```
   - Le widget aura un rectangle de couleur pour le fond
   - Basé sur la valeur actuelle (par rapport au min et max), jusqu'à 5 barre de courant seront dessinés
4) La méthode sizeHint() peut être redéfini pour suggérer la grandeur par défaut
5) Ajouter le code suivant au constructeur pour minimizer l'expansion du widget
```
self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
```
6) Ajouter un signal personnalisé valeurChanged qui sera déclenché dans le setValue()
7) Embellissez le tout une fois que cela fonctionne


