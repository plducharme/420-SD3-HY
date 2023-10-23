from PySide6.QtCore import QPoint, QTimer, QPropertyAnimation, Property, QObject, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PySide6.QtGui import QPixmap, QPainter, QColorConstants


class BitmapAnimation(QMainWindow):

    def __init__(self):
        super().__init__()
        self.disposition = QVBoxLayout()

        widget_central = QWidget()
        widget_central.setLayout(self.disposition)

        self.etiquette = QLabel()
        self.canevas = QPixmap(800, 500)
        self.canevas.fill(QColorConstants.White)
        self.etiquette.setPixmap(self.canevas)
        self.bouton_avancer = QPushButton("Démarrer/Arrêter")
        self.bouton_avancer.clicked.connect(self.bouton_start_stop_clicked)
        self.disposition.addWidget(self.etiquette)
        self.disposition.addWidget(self.bouton_avancer)

        self.image_animee = ImageAnimee("./images/chat", 8, self)
        self.image_animee.dessiner()

        self.demarre = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.image_animee.dessiner)

        self.animation_position = QPropertyAnimation(self.image_animee, b"position", self)
        self.animation_position.setEndValue(QPoint(700, 25))
        self.animation_position.setDuration(3000)
        self.animation_position.start()
        self.timer.start(500)

        self.setCentralWidget(widget_central)

    def bouton_start_stop_clicked(self):
        if self.demarre:
            self.timer.stop()
            self.animation_position.stop()
            self.demarre = False
        else:
            self.timer.start(500)
            self.animation_position.start()
            self.demarre = True

class ImageAnimee(QObject):

    def __init__(self, prefixe_image: str, nb_images: int, vue: BitmapAnimation):
        super().__init__()
        self.prefixe_image = prefixe_image
        self.nb_images = nb_images
        self.vue = vue
        self.liste_images = []
        self._position = QPoint(25,25)
        for i in range(0, nb_images):
            pixmap = QPixmap(self.prefixe_image + "_" + str(i) + ".png")
            pixmap = pixmap.scaled(QSize(100, 100))
            self.liste_images.append(pixmap)
        self.index_image = 0

    @Property(QPoint)
    def position(self):
        return self._position

    @position.setter
    def position(self, position: QPoint):
        self._position = position

    def pixmap(self, index: int):
        return self.liste_images[index % self.nb_images]

    def dessiner(self):
        canevas = self.vue.etiquette.pixmap()
        canevas.fill(QColorConstants.White)
        painter = QPainter(canevas)
        painter.drawPixmap(self._position, self.pixmap(self.index_image))
        painter.end()
        self.vue.etiquette.setPixmap(canevas)
        self.index_image += 1


app = QApplication()
ba = BitmapAnimation()
ba.show()
app.exec()