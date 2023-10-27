from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QPainter, QColor,QPen, QColorConstants, QKeyEvent
from PySide6.QtCore import QPoint, QTimer, Qt
import random
from enum import Enum
from collections import deque


class FenetrePrincipale(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super Serpents")
        self.creerMenuJeu()

    # Gérer les événements du clavier
    def keyPressEvent(self, event: QKeyEvent) -> None:

        if event.key() == Qt.Key.Key_W:
            self.jeu.joueurs[0].direction = Serpent.Direction.HAUT
        elif event.key() == Qt.Key.Key_S:
            self.jeu.joueurs[0].direction = Serpent.Direction.BAS
        elif event.key() == Qt.Key.Key_A:
            self.jeu.joueurs[0].direction = Serpent.Direction.GAUCHE
        elif event.key() == Qt.Key.Key_D:
            self.jeu.joueurs[0].direction = Serpent.Direction.DROITE
        elif self.jeu.nb_joueurs == 2:
            if event.key() == Qt.Key.Key_I:
                self.jeu.joueurs[1].direction = Serpent.Direction.HAUT
            elif event.key() == Qt.Key.Key_K:
                self.jeu.joueurs[1].direction = Serpent.Direction.BAS
            elif event.key() == Qt.Key.Key_J:
                self.jeu.joueurs[1].direction = Serpent.Direction.GAUCHE
            elif event.key() == Qt.Key.Key_L:
                self.jeu.joueurs[1].direction = Serpent.Direction.DROITE
        else:
            # On ignore les autres touches, si on veut les utiliser, on peut appeler super().keyPressEvent(event)
            return


    # Créer le menu de sélection 1 ou 2 joueur
    def creerMenuJeu(self):
        widget_central = QWidget()
        disposition = QVBoxLayout()
        widget_central.setLayout(disposition)
        self.bouton_un_joueur = QPushButton("Un joueur")
        self.bouton_un_joueur.clicked.connect(self.un_joueur_clicked)
        self.bouton_deux_joueurs = QPushButton("Deux joueurs")
        self.bouton_deux_joueurs.clicked.connect(self.deux_joueurs_clicked)

        disposition.addWidget(self.bouton_un_joueur)
        disposition.addWidget(self.bouton_deux_joueurs)

        self.setCentralWidget(widget_central)

        self.label_jeu = QLabel()

    def un_joueur_clicked(self):
        self.jeu = JeuSerpent(self, 1)
        self.label_jeu.setPixmap(self.jeu.canevas)
        self.setCentralWidget(self.label_jeu)
        self.jeu.demarrer_jeu()

    def deux_joueurs_clicked(self):
        self.jeu = JeuSerpent(self,2)
        self.label_jeu.setPixmap(self.jeu.canevas)
        self.setCentralWidget(self.label_jeu)
        self.jeu.demarrer_jeu()


class JeuSerpent():
    # Grandeur d'un QPoint de serpent
    GRANDEUR_SERPENT = 10

    def __init__(self, vue: FenetrePrincipale, nb_joueurs: int = 1, largeur: int = 500, hauteur: int = 500):
        self.vue = vue
        self.nb_joueurs = nb_joueurs
        self.largeur = largeur
        self.hauteur = hauteur
        self.label_jeu = self.vue.label_jeu
        self.canevas = QPixmap(largeur, hauteur)
        self.canevas.fill(QColor("white"))
        self.joueurs = []
        self.nourriture = []
        self.compteur_nourriture = 0

        self.game_over = True
        self.is_paused = False

        self.joueurs.append(Serpent(QColorConstants.Red, QColorConstants.Green, self.generer_random_qpoint(self.largeur, self.hauteur)))

        if self.nb_joueurs == 2:
            self.joueurs.append(Serpent(QColorConstants.Yellow, QColorConstants.Blue, self.generer_random_qpoint(self.largeur, self.hauteur)))

    def generer_random_qpoint(self, largeur, hauteur):
        x = random.randrange(JeuSerpent.GRANDEUR_SERPENT, largeur - JeuSerpent.GRANDEUR_SERPENT, JeuSerpent.GRANDEUR_SERPENT)
        y = random.randrange(JeuSerpent.GRANDEUR_SERPENT, hauteur - JeuSerpent.GRANDEUR_SERPENT, JeuSerpent.GRANDEUR_SERPENT)
        return QPoint(x, y)

    def demarrer_jeu(self):
        self.game_over = False
        self.is_paused = False
        self.timer = QTimer(self.vue)
        self.timer.timeout.connect(self.boucle_jeu)
        self.timer.start(250)

    def dessiner_jeu(self):
        canevas = self.vue.label_jeu.pixmap()
        painter = QPainter(canevas)
        painter.fillRect(0, 0, self.largeur, self.hauteur, QColorConstants.Gray)
        painter.end()
        self.vue.label_jeu.setPixmap(canevas)
        self.vue.update()
        for serpent in self.joueurs:
            serpent.dessiner(self.vue)
        for nourriture in self.nourriture:
            nourriture.dessiner(self.vue)

    def boucle_jeu(self):

        if not self.game_over:
            if self.is_paused:
                return
            if self.compteur_nourriture % 20 == 0:
                nourriture = Nourriture(self.generer_random_qpoint(self.largeur, self.hauteur))
                self.nourriture.append(nourriture)
            if len(self.nourriture) == 0:
                nourriture = Nourriture(self.generer_random_qpoint(self.largeur, self.hauteur))
                self.nourriture.append(nourriture)
            self.compteur_nourriture += 1
            self.dessiner_jeu()
            for serpent in self.joueurs:
                ancienne_position = serpent.position.__copy__()
                serpent.avancer()
                # Collision de base, ne pas utiliser pour le TP
                for bouffe in self.nourriture:
                    # print("Bouffe: " + str(bouffe.position) + " Serpent: " + str(self.position))
                    if bouffe.position.x() == serpent.position.x() and bouffe.position.y() == serpent.position.y():
                        serpent.corps_serpent.appendleft(ancienne_position)
                        self.nourriture.remove(bouffe)

                if serpent.position.x() >= self.largeur or serpent.position.x() <= 0:
                    self.game_over = True

                if serpent.position.y() >= self.hauteur or serpent.position.y() <= 0:
                    self.game_over = True

        return


class Serpent():

    class Direction(Enum):
        HAUT = 1
        BAS = 2
        GAUCHE = 3
        DROITE = 4

    def __init__(self, couleur_tete: QColor, couleur_corps: QColor, position: QPoint):
        self.couleur_tete = couleur_tete
        self.couleur_corps = couleur_corps
        self.position = position
        self.corps_serpent = deque([])
        self.direction = Serpent.Direction.HAUT

    def dessiner(self, vue: FenetrePrincipale):
        canevas = vue.label_jeu.pixmap()
        painter = QPainter(canevas)
        pen = QPen()
        # tete rouge
        pen.setColor(self.couleur_tete)
        pen.setWidth(JeuSerpent.GRANDEUR_SERPENT)
        painter.setPen(pen)
        painter.drawPoint(self.position)

        pen = QPen()
        pen.setWidth(JeuSerpent.GRANDEUR_SERPENT)
        pen.setColor(self.couleur_corps)
        painter.setPen(pen)

        for point in self.corps_serpent:
            painter.drawPoint(point)

        painter.end()
        vue.label_jeu.setPixmap(canevas)
        vue.update()

    def avancer(self):

        if self.direction == Serpent.Direction.HAUT:
            previous_position = self.position.__copy__()
            self.position.setY(self.position.y() - 10)
            self.corps_serpent.appendleft(previous_position)
            self.corps_serpent.pop()
        elif self.direction == Serpent.Direction.BAS:
            previous_position = self.position.__copy__()
            self.position.setY(self.position.y() + 10)
            self.corps_serpent.appendleft(previous_position)
            self.corps_serpent.pop()
        elif self.direction == Serpent.Direction.GAUCHE:
            previous_position = self.position.__copy__()
            self.position.setX(self.position.x() - 10)
            self.corps_serpent.appendleft(previous_position)
            self.corps_serpent.pop()
        elif self.direction == Serpent.Direction.DROITE:
            previous_position = self.position.__copy__()
            self.position.setX(self.position.x() + 10)
            self.corps_serpent.appendleft(previous_position)
            self.corps_serpent.pop()
        else:
            return

    def collision(self, liste_points: []):
        for point in liste_points:
            if self.position.x() == point.x() and self.position.y() == point.y():
                return True
        return False


class Nourriture:

    def __init__(self, position: QPoint):
        self.position = position

    def dessiner(self, vue: FenetrePrincipale):
        canevas = vue.label_jeu.pixmap()
        painter = QPainter(canevas)
        pen = QPen()
        pen.setWidth(JeuSerpent.GRANDEUR_SERPENT)
        pen.setColor(QColorConstants.Magenta)
        painter.setPen(pen)
        painter.drawPoint(self.position)
        painter.end()
        vue.label_jeu.setPixmap(canevas)
        vue.update()


app = QApplication()
fp = FenetrePrincipale()
fp.show()
app.exec()

