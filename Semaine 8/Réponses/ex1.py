from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout
from PySide6.QtCore import (QSize, QPoint, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup,
                            QParallelAnimationGroup, QRect)



class Ex1(QMainWindow):

    def __init__(self):
        super().__init__()

        # Le widget contenant le layout
        widget_central = QWidget()
        disposition = QVBoxLayout()
        widget_central.setLayout(disposition)
        self.setCentralWidget(widget_central)

        # Le widget dans lequel on va ajouter le widget à animer
        widget_surface = QWidget()
        widget_surface.setFixedSize(QSize(800, 600))
        disposition.addWidget(widget_surface)

        # Le widget qui sera animé
        self.widget_enfant = QWidget(widget_surface)
        self.widget_enfant.resize(QSize(15, 15))
        self.widget_enfant.setStyleSheet("background-color:green")
        rect = QRect(QPoint(150, 150), self.widget_enfant.size())
        self.widget_enfant.setGeometry(rect)

        # Ajout des boutons
        bouton_doubler = QPushButton("Doubler grandeur")
        bouton_doubler.clicked.connect(self.bouton_doubler_clicked)
        disposition.addWidget(bouton_doubler)

        bouton_moitie = QPushButton("Moitié grandeur")
        bouton_moitie.clicked.connect(self.bouton_moitie_clicked)
        disposition.addWidget(bouton_moitie)

        bouton_doubler_moitie_seq = QPushButton("Doubler -> Réduire")
        bouton_doubler_moitie_seq.clicked.connect(self.bouton_doubler_moitie_seq_clicked)
        disposition.addWidget(bouton_doubler_moitie_seq)

        bouton_translation_bas_droite = QPushButton("Déplacement Bas-Droite")
        bouton_translation_bas_droite.clicked.connect(self.bouton_translation_bas_droite_clicked)
        disposition.addWidget(bouton_translation_bas_droite)

        bouton_translation_haut_gauche = QPushButton("Déplacement Haut-Gauche")
        bouton_translation_haut_gauche.clicked.connect(self.bouton_translation_haut_gauche_clicked)
        disposition.addWidget(bouton_translation_haut_gauche)



    def bouton_doubler_clicked(self):
        animation = self.doubler(self.widget_enfant.size())
        animation.start()

    def bouton_moitie_clicked(self):
        animation = self.moitie(self.widget_enfant.size())
        animation.start()

    def bouton_doubler_moitie_seq_clicked(self):
        animation_doubler = self.doubler(self.widget_enfant.size())
        # On débute au double de la grandeur
        animation_moitie = self.moitie(self.widget_enfant.size()*2)
        groupe_animation_seq = QSequentialAnimationGroup(self)
        groupe_animation_seq.addAnimation(animation_doubler)
        groupe_animation_seq.addAnimation(animation_moitie)
        groupe_animation_seq.start()

    def bouton_translation_bas_droite_clicked(self):
        animation = self.translation_bas_droite()
        animation.start()

    def bouton_translation_haut_gauche_clicked(self):
        animation = self.translation_haut_gauche()
        animation.start()



    # Méthodes retournant des animations pour réutilisation
    def doubler(self, grandeur_initiale: QSize) -> QPropertyAnimation:
        animation_doubler = QPropertyAnimation(self.widget_enfant, b"size", self)
        animation_doubler.setStartValue(grandeur_initiale)
        animation_doubler.setEndValue(grandeur_initiale*2)
        animation_doubler.setDuration(500)
        animation_doubler.setEasingCurve(QEasingCurve.Type.OutCurve)
        return animation_doubler

    def moitie(self, grandeur_initiale: QSize) -> QPropertyAnimation:
        animation_moitie = QPropertyAnimation(self.widget_enfant, b"size", self)
        animation_moitie.setStartValue(grandeur_initiale)
        animation_moitie.setEndValue(grandeur_initiale/2)
        animation_moitie.setDuration(500)
        animation_moitie.setEasingCurve(QEasingCurve.Type.OutElastic)
        return animation_moitie

    def translation_bas_droite(self):
        animation = QPropertyAnimation(self.widget_enfant, b"pos", self)
        animation.setEndValue(QPoint(self.widget_enfant.pos().x()+150, self.widget_enfant.pos().y()+150))
        animation.setDuration(1500)
        animation.setEasingCurve(QEasingCurve.Type.InOutBack)
        return animation

    def translation_haut_gauche(self):
        animation = QPropertyAnimation(self.widget_enfant, b"pos", self)
        animation.setEndValue(QPoint(self.widget_enfant.pos().x() - 150, self.widget_enfant.pos().y() - 150))
        animation.setDuration(1500)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuint)
        return animation



app = QApplication()
ex1 = Ex1()
ex1.show()
app.exec()