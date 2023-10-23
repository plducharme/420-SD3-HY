from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QFileDialog, QPushButton, QLineEdit,
                               QWidget, QGridLayout)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QRect

# Image pris de https://docs.coronalabs.com/images/simulator/sprites-cat-running.png

class CoupeImage(QMainWindow):

    def __init__(self):
        super().__init__()

        widget_central = QWidget()
        self.disposition = QGridLayout()
        widget_central.setLayout(self.disposition)
        self.setWindowTitle("Couper d'images")
        self.bouton_fichier = QPushButton("Sélectionner fichier")
        self.bouton_fichier.clicked.connect(self.afficher_dialogue_fichier)
        self.etiquette_fichier = QLabel("Fichier:")
        self.nom_fichier = QLineEdit("Fichier")
        self.etiquette_hauteur = QLabel("Hauteur:")
        self.hauteur_coupe = QLineEdit("256")
        self.etiquette_largeur = QLabel("Largeur:")
        self.largeur_coupe = QLineEdit("512")
        self.bouton_coupe = QPushButton("Coupez!")
        self.bouton_coupe.clicked.connect(self.couper_image)

        self.disposition.addWidget(self.etiquette_fichier, 0, 0)
        self.disposition.addWidget(self.nom_fichier, 0, 1)
        self.disposition.addWidget(self.bouton_fichier, 0, 2)
        self.disposition.addWidget(self.etiquette_hauteur, 1, 0)
        self.disposition.addWidget(self.hauteur_coupe, 1, 1, 1, 2)
        self.disposition.addWidget(self.etiquette_largeur, 2, 0)
        self.disposition.addWidget(self.largeur_coupe, 2, 1, 1, 2)
        self.disposition.addWidget(self.bouton_coupe, 3, 1, 1, 2)

        self.setCentralWidget(widget_central)


    def afficher_dialogue_fichier(self):
        fichier = QFileDialog.getOpenFileName(self, "Ouvrir Image", "./images", "Images (*.png)")
        self.nom_fichier.setText(fichier[0])

    def couper_image(self):
        nom_fichier = self.nom_fichier.text()
        image_originale = QImage(nom_fichier)
        index = 0

        largeur_totale = image_originale.width()
        hauteur_totale = image_originale.height()

        largeur_image = int(self.largeur_coupe.text())
        hauteur_image = int(self.hauteur_coupe.text())

        fichier_prefixe = nom_fichier.split(".")[0]

        for y in range(0, hauteur_totale, hauteur_image):
            for x in range(0, largeur_totale, largeur_image):
                frame = image_originale.copy(QRect(x, y, largeur_image, hauteur_image))
                nouveau_fichier = fichier_prefixe+"_"+str(index)+".png"
                print(nouveau_fichier)
                frame.save(nouveau_fichier)
                index += 1


app = QApplication()
ci = CoupeImage()
ci.show()
app.exec()