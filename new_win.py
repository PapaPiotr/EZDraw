import sys
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QStatusBar, QToolBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CuteFEN Diagramm Generator")
        
        self.label = QLabel("Welcome to CuteFEN")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(self.label)
        
        # Définition des actions
        self.act_Settings = QAction(QIcon.fromTheme("document-properties"), "Propriétés", self)
        self.act_Settings.setStatusTip("Propriétés")
        self.act_Settings.triggered.connect(self.truc)

        self.act_New = QAction(QIcon.fromTheme("document-new"), "Nouveau document", self)
        self.act_New.setStatusTip("Nouveau document")
        self.act_New.setShortcut(QKeySequence("Ctrl+n"))
        self.act_New.triggered.connect(self.truc)

        self.act_Save = QAction(QIcon.fromTheme("document-save"), "Enregistrer le formulaire", self)
        self.act_Save.setStatusTip("Enregistrer le formulaire")
        self.act_Save.setShortcut(QKeySequence("Ctrl+s"))
        self.act_Save.triggered.connect(self.truc)

        self.act_Save_as = QAction(QIcon.fromTheme("document-save-as"), "Enregistrer sous", self)
        self.act_Save_as.setStatusTip("Enregistrer sous")
        self.act_Save_as.setShortcut(QKeySequence("Ctrl+Shift+s"))
        self.act_Save_as.triggered.connect(self.truc)

        self.act_Open = QAction(QIcon.fromTheme("document-open"), "Ouvrir un formulaire", self)
        self.act_Open.setStatusTip("Ouvrir un formulaire")
        self.act_Open.setShortcut(QKeySequence("Ctrl+o"))
        self.act_Open.triggered.connect(self.truc)

        self.act_Undo = QAction(QIcon.fromTheme("edit-undo"), "Annuler", self)
        self.act_Undo.setStatusTip("Annuler")
        self.act_Undo.setShortcut(QKeySequence("Ctrl+z"))
        self.act_Undo.triggered.connect(self.truc)

        self.act_Redo = QAction(QIcon.fromTheme("edit-redo"), "Rétablir", self)
        self.act_Redo.setStatusTip("Rétablir")
        self.act_Redo.setShortcut(QKeySequence("Ctrl+y"))
        self.act_Redo.triggered.connect(self.truc)

        self.act_Img = QAction(QIcon.fromTheme("document-preview"), "&Aperçu de la page de diagrammes", self)
        self.act_Img.setStatusTip("Aperçu de la page de diagrammes")
        self.act_Img.setShortcut(QKeySequence("Ctrl+Shift+o"))
        self.act_Img.triggered.connect(self.truc)

        self.act_Print = QAction(QIcon.fromTheme("document-print"), "Imprimer", self)
        self.act_Print.setStatusTip("Imprimer")
        self.act_Print.setShortcut(QKeySequence("Ctrl+p"))
        self.act_Print.triggered.connect(self.truc)

        self.act_Help = QAction(QIcon.fromTheme("help-contents"), "Aide", self)
        self.act_Help.setStatusTip("Aide")
        self.act_Help.setShortcut(QKeySequence("Ctrl+h"))
        self.act_Help.triggered.connect(self.truc)

        self.act_About = QAction(QIcon.fromTheme("help-about"), "À propos", self)
        self.act_About.setStatusTip("À propos")
        self.act_About.triggered.connect(self.truc)

        self.act_Exit = QAction(QIcon.fromTheme("application-exit"), "Quitter", self)
        self.act_Exit.setStatusTip("Quitter")
        self.act_Exit.setShortcut(QKeySequence("Ctrl+q"))
        self.act_Exit.triggered.connect(self.truc)

        # Définition de la barre d'outils
        self.toolbar = QToolBar("Main toolbar")
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.act_New)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Open)
        self.toolbar.addAction(self.act_Save)
        self.toolbar.addAction(self.act_Save_as)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Img)
        self.toolbar.addAction(self.act_Print)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Settings)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Undo)
        self.toolbar.addAction(self.act_Redo)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Help)
        self.toolbar.addAction(self.act_About)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Exit)

        # Définition de la barre de menu
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("&File")

        self.fileMenu.addAction(self.act_New)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Open)
        self.fileMenu.addAction(self.act_Save)
        self.fileMenu.addAction(self.act_Save_as)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Img)
        self.fileMenu.addAction(self.act_Print)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Settings)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Exit)

        self.fileEdit = self.menu.addMenu("&Édition")
        self.fileEdit.addAction(self.act_Undo)
        self.fileEdit.addAction(self.act_Redo)

        self.fileHelp = self.menu.addMenu("&Aide")
        self.fileHelp.addAction(self.act_Help)
        self.fileHelp.addAction(self.act_About)

        # Définition de la barre de status
        self.setStatusBar(QStatusBar(self))

    def truc(self,s):
        print("click",s)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
