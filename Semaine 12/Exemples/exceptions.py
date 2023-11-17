from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton


class ExceptionExemple(QMainWindow):

    def __init__(self):
        super().__init__()
        self.bouton_crash = QPushButton("Crash!")
        self.bouton_crash.clicked.connect(self.bouton_crash_clicked)
        self.setCentralWidget(self.bouton_crash)


    def bouton_crash_clicked(self):
        try:
            # On force une exception
            assert(False)

        except AssertionError as e:
            # Un QMessageBox est une fenêtre modale
            boite_message = QMessageBox()
            boite_message.setText("Erreur d'assertion")
            boite_message.exec()


app = QApplication()
ee = ExceptionExemple()
ee.show()
app.exec()

