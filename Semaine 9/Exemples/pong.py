import PySide6.QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLCDNumber
from PySide6.QtGui import QPixmap, QColorConstants, QPen, QPainter, Qt
from PySide6.QtCore import QTimer, QRect
from enum import Enum


class Pong(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pong")
        self.label_jeu = QLabel()
        self.canevas = QPixmap(800, 600)
        self.label_jeu.setPixmap(self.canevas)
        widget_central = QWidget()
        disposition_centrale = QVBoxLayout()
        widget_central.setLayout(disposition_centrale)

        widget_score = QWidget()
        disposition_score = QHBoxLayout()
        widget_score.setLayout(disposition_score)
        self.score_j1 = QLCDNumber()
        self.score_j1.display("0")
        self.score_j2 = QLCDNumber()
        self.score_j2.display("0")
        disposition_score.addWidget(self.score_j1)
        disposition_score.addWidget(self.score_j2)

        disposition_centrale.addWidget(widget_score)
        disposition_centrale.addWidget(self.label_jeu)

        self.setCentralWidget(widget_central)
        # On initialise le jeu et on commence la boucle de jeu
        self.jeu = JeuPong(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.jeu.boucle_jeu)
        self.timer.start(200)

    # Surdéfinition (override) de la méthode pour capter les événements clavier
    def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)

        if event.key() == Qt.Key.Key_W:
            self.jeu.joueurs[0].deplacer(Direction.HAUT, self.jeu.hauteur)
        elif event.key() == Qt.Key.Key_S:
            self.jeu.joueurs[0].deplacer(Direction.BAS, self.jeu.hauteur)
        elif event.key() == Qt.Key.Key_I:
            self.jeu.joueurs[1].deplacer(Direction.HAUT, self.jeu.hauteur)
        elif event.key() == Qt.Key.Key_K:
            self.jeu.joueurs[1].deplacer(Direction.BAS, self.jeu.hauteur)


class JeuPong:

    BLOCK_SIZE = 10
    LARGEUR = 800
    HAUTEUR = 600

    def __init__(self, vue: Pong):
        self.vue = vue
        self.max_score = 10
        self.paused = False
        self.game_over = False
        self.joueurs = []
        self.largeur = 800
        self.hauteur = 600
        joueur1 = Joueur(0)
        joueur2 = Joueur(self.largeur - JeuPong.BLOCK_SIZE)
        self.joueurs.append(joueur1)
        self.joueurs.append(joueur2)
        self.balle = Balle(Joueur.LARGEUR_PALETTE)
        self.but_j1 = False
        self.but_j2 = False
        self.nouveau_round = True
        self.delai_nouveau_round = 0

    def dessiner(self):
        canevas = self.vue.canevas
        painter = QPainter(canevas)

        painter.fillRect(0, 0, self.largeur, self.hauteur, QColorConstants.Black)
        painter.end()
        self.vue.label_jeu.setPixmap(canevas)
        self.vue.update()

    def boucle_jeu(self):
        if not self.game_over:
            if self.paused:
                return
            if self.nouveau_round:
                # Le QTimer appelle la méthode chaque 200ms, 10*200 = 2sec entre les rounds
                if self.delai_nouveau_round == 10:
                    self.delai_nouveau_round = 0
                    self.nouveau_round = False
                else:
                    self.delai_nouveau_round += 1
                    return
            if self.but_j1 or self.but_j2:
                if self.but_j1:
                    self.joueurs[0].score += 1
                    self.balle = Balle(self.largeur - Joueur.LARGEUR_PALETTE)
                    self.balle.vitesse_x = self.balle.vitesse_x * -1
                    self.but_j1 = False
                else:
                    self.joueurs[1].score += 1
                    self.balle = Balle(Joueur.LARGEUR_PALETTE)
                    self.but_j2 = False
                self.nouveau_round = True
                self.reset_palette()
                self.update_score()
            self.dessiner()
            for joueur in self.joueurs:
                joueur.dessiner(self.vue)
            self.balle.deplacer(self)
            self.balle.dessiner(self.vue)

    def update_score(self):
        self.vue.score_j1.display(str(self.joueurs[0].score))
        self.vue.score_j2.display(str(self.joueurs[1].score))

    def reset_palette(self):
        for joueur in self.joueurs:
            joueur.y = 300

class Direction(Enum):
    HAUT = 1
    BAS = 2

class Joueur:

    GRANDEUR_PALETTE = 75
    LARGEUR_PALETTE = 10

    def __init__(self, x: int):
        self.score = 0
        self.y = 300
        self.x = x
        self.direction = Direction.HAUT

    def deplacer(self, direction: Direction, hauteur: int):
        if direction == Direction.HAUT:
            if self.y - JeuPong.BLOCK_SIZE > 0:
                self.y -= JeuPong.BLOCK_SIZE
            else:
                self.y = 0
        elif direction == Direction.BAS:
            if self.y + Joueur.GRANDEUR_PALETTE + JeuPong.BLOCK_SIZE < hauteur:
                self.y += JeuPong.BLOCK_SIZE
            else:
                self.y = hauteur - Joueur.GRANDEUR_PALETTE

    def dessiner(self, vue: Pong):
        canevas = vue.canevas
        painter = QPainter(canevas)
        pen = QPen()
        pen.setWidth(JeuPong.BLOCK_SIZE)
        pen.setColor(QColorConstants.White)
        painter.setPen(pen)
        painter.fillRect(QRect(self.x, self.y, Joueur.LARGEUR_PALETTE, Joueur.GRANDEUR_PALETTE), QColorConstants.White)
        #painter.drawRect()
        painter.end()
        vue.label_jeu.setPixmap(canevas)
        vue.update()


class Balle:
    def __init__(self, x: int):
        self.vitesse_x = 2 * JeuPong.BLOCK_SIZE
        self.vitesse_y = 2 * JeuPong.BLOCK_SIZE
        self.x = x
        self.y = 300


    def dessiner(self, vue: Pong):
        canevas = vue.canevas
        painter = QPainter(canevas)
        pen = QPen()
        pen.setWidth(JeuPong.BLOCK_SIZE)
        pen.setColor(QColorConstants.Green)
        painter.setPen(pen)

        painter.drawPoint(self.x, self.y)
        painter.end()
        vue.label_jeu.setPixmap(canevas)

    def deplacer(self, jeu: JeuPong):
        x2 = self.x + self.vitesse_x
        y2 = self.y + self.vitesse_y

        if y2 <= 0:
            self.vitesse_y = self.vitesse_y * -1
        elif y2 >= JeuPong.HAUTEUR:
            self.vitesse_y = self.vitesse_y * -1
        self.y = y2

        for joueur in jeu.joueurs:
            if x2 in range(joueur.x, joueur.x + Joueur.LARGEUR_PALETTE + 1) and y2 in range(joueur.y, joueur.y + joueur.GRANDEUR_PALETTE + 1):
                self.vitesse_x = self.vitesse_x * -1

        if x2 <= 0:
            jeu.but_j2 = True
        elif x2 >= JeuPong.LARGEUR:
            jeu.but_j1 = True
        self.x = x2


app = QApplication()
pong = Pong()
pong.show()
app.exec()