import os
from pickle import load
import sys
import re
import copy
from PyQt6.QtGui import QAction, QGradient, QIcon, QKeySequence, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QFormLayout, QHBoxLayout, QMainWindow, QLabel, QSizePolicy, QStatusBar, QTabWidget, QToolBar, QGridLayout, QVBoxLayout, QWidget, QLineEdit, QPushButton, QSpinBox, QDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.currentFileName = "Nouveau document"
        self.newFileName = ""
        self.setWindowTitle(self.currentFileName + " | CuteFEN Diagramm Generator")
        
        self.mainWidget = QWidget()

        self.setCentralWidget(self.mainWidget)

        self.layMain = QVBoxLayout()
        self.layTitle = QGridLayout()
        self.layNum = QGridLayout()
        self.layForm = QGridLayout()

        self.layMain.addLayout(self.layTitle)
        self.layMain.addLayout(self.layForm)
        self.layMain.addLayout(self.layNum)
        self.mainWidget.setLayout(self.layMain)

        self.info = {}
        self. changedFile = False
        self.implement_dict()
        
        # Définition des actions
        self.act_Settings = QAction(QIcon.fromTheme("document-properties"), "&Paramètres", self)
        self.act_Settings.setStatusTip("Paramètres")
        self.act_Settings.triggered.connect(self.openProp)

        self.act_New = QAction(QIcon.fromTheme("document-new"), "Nouveau document", self)
        self.act_New.setStatusTip("Nouveau document")
        self.act_New.setShortcut(QKeySequence("Ctrl+n"))
        self.act_New.triggered.connect(self.newDoc)

        self.act_Save = QAction(QIcon.fromTheme("document-save"), "Enregistrer le formulaire", self)
        self.act_Save.setStatusTip("Enregistrer le formulaire")
        self.act_Save.setShortcut(QKeySequence("Ctrl+s"))
        self.act_Save.triggered.connect(self.saveForm)

        self.act_Save_as = QAction(QIcon.fromTheme("document-save-as"), "Enregistrer sous", self)
        self.act_Save_as.setStatusTip("Enregistrer sous")
        self.act_Save_as.setShortcut(QKeySequence("Ctrl+Shift+s"))
        self.act_Save_as.triggered.connect(self.saveAs)

        self.act_Open = QAction(QIcon.fromTheme("document-open"), "Ouvrir un formulaire", self)
        self.act_Open.setStatusTip("Ouvrir un formulaire")
        self.act_Open.setShortcut(QKeySequence("Ctrl+o"))
        self.act_Open.triggered.connect(self.openDoc)
#       self.act_Open.triggered.connect(self.update_display)

        self.act_Undo = QAction(QIcon.fromTheme("edit-undo"), "Annuler", self)
        self.act_Undo.setStatusTip("Annuler")
        self.act_Undo.setShortcut(QKeySequence("Ctrl+z"))
        self.act_Undo.triggered.connect(self.undo)

        self.act_Redo = QAction(QIcon.fromTheme("edit-redo"), "Rétablir", self)
        self.act_Redo.setStatusTip("Rétablir")
        self.act_Redo.setShortcut(QKeySequence("Ctrl+y"))
        self.act_Redo.triggered.connect(self.redo)

        self.act_Img = QAction(QIcon.fromTheme("media-playback-start"), "&Aperçu de la page de diagrammes", self)
        self.act_Img.setStatusTip("Aperçu de la page de diagrammes")
        self.act_Img.setShortcut(QKeySequence("Ctrl+Shift+o"))
        self.act_Img.triggered.connect(self.preview)

        self.act_Print = QAction(QIcon.fromTheme("document-print"), "Imprimer", self)
        self.act_Print.setStatusTip("Imprimer")
        self.act_Print.setShortcut(QKeySequence("Ctrl+p"))
        self.act_Print.triggered.connect(self.print)

        self.act_Help = QAction(QIcon.fromTheme("help-contents"), "Aide", self)
        self.act_Help.setStatusTip("Aide")
        self.act_Help.setShortcut(QKeySequence("Ctrl+h"))
        self.act_Help.triggered.connect(self.openHelp)

        self.act_About = QAction(QIcon.fromTheme("help-about"), "À propos", self)
        self.act_About.setStatusTip("À propos")
        self.act_About.triggered.connect(self.openAbout)

        self.act_Exit = QAction(QIcon.fromTheme("application-exit"), "Quitter", self)
        self.act_Exit.setStatusTip("Quitter")
        self.act_Exit.setShortcut(QKeySequence("Ctrl+q"))
        self.act_Exit.triggered.connect(self.quit)

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

        self.load_widgets()

    def implement_dict(self):
        self.info["max_cols"] = 5
        self.info["max_diags"] = 15

        # paramètres généraux
        self.info["title_state"] = True 
        self.info["numPage_state"] = True
        self.info["numDiag_state"] = True
        self.info["numDiag_text"] = "à gauche"
        self.info["color_state"] = True
        self.info["color_text"] = "à gauche"
        self.info["format_text"] = "portrait"
        self.info["flip_state"] = True
        self.info["legend_state"] = True
        self.info["cols_value"] = 3
        self.info["diags_value"] = 15
        self.info["margin_value"] = 20
        self.info["coord_state"] = True
        self.info["down_state"] = True
        self.info["up_state"] = True
        self.info["left_state"] = True
        self.info["right_state"] = True

        self.load_default_settings()
        
        # données de page saisies par l'utilisateur
        self.info["title_text"] = ''
        self.info["numPage_value"] = 1
        self.info["numDiag_value"] = 1

        # données de diagramme saisies par l'utilisateur
        self.info["fens"] = list()
        self.info["legends"] = list()
        self.info["symbols"] = list()
        self.info["arrows"] = list()

        # variables manipulées par le programme
        self.info["trimmed_fens"] = list()
        self.info["trimmed_legends"] = list()
        self.info["trimmed_symbols"] = list()
        self.info["active_editor"] = int()

        # images
        self.info["page"] = None
        self.info["boxes"] = list()

        i = 0
        while i < self.info["max_diags"]:
            self.info["fens"].append("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
            self.info["legends"].append("Position de départ")
            self.info["symbols"].append("0000000000000000000000000000000000000000000000000000000000000000")
            self.info["arrows"].append([])
            i += 1
        i = 0
        self.load_default_settings()

    def load_default_settings(self):
        fileName = os.path.join("settings","default.txt")

        with open(fileName, "r") as file:
            settings = file.read().split("|")
            for setting in settings:
                sett = setting.split(",")

                if re.search("state",sett[0]):
                    if sett[1] == "True":
                        self.info[sett[0]] = True
                    else:
                        self.info[sett[0]] = False

                elif re.search("text",sett[0]):
                    self.info[sett[0]] = sett[1]

                elif re.search("value",sett[0]):
                    self.info[sett[0]] = int(sett[1])

    def load_widgets(self):
        i = 1
        # Section de titre
        if self.info["title_state"] == True:
            self.layTitle.addWidget(QLabel("Titre : "), 0, 0)
            self.title_text = QLineEdit("")
            self.title_text.textChanged.connect(self.change_title_text)
            self.layTitle.addWidget(self.title_text, 0, 1)

        # Section de formulaire
        self.layForm.addWidget(QLabel("Saisir un FEN ou un identifiant de problème Lichess"), 0, 1)

        if self.info["legend_state"] == True:
            self.layForm.addWidget(QLabel("Saisir une légende"), 0, 3)

        self.fens = list()
        self.legends = list()

        while i <= int(self.info["diags_value"]):

            self.layForm.addWidget(QLabel("Fig." + str(i)), i, 0)

            self.fens.append(QLineEdit(self.info["fens"][i-1]))
            self.fens[i-1].id = i-1
            self.fens[i-1].textChanged.connect(self.change_fens)
            self.layForm.addWidget(self.fens[i-1], i, 1)

            if self.info["legend_state"] == True:
                self.legends.append(QLineEdit(self.info["legends"][i-1]))
                self.legends[i-1].id = i-1
                self.legends[i-1].textChanged.connect(self.change_legends)
                self.layForm.addWidget(self.legends[i-1], i, 3)

            self.layForm.addWidget(QPushButton("Charger un fichier"), i, 2)
            self.layForm.addWidget(QPushButton("Éditeur graphique"), i, 4)
            i += 1

        # Section de numérotation
        if self.info["numPage_state"] == True:
            self.layNum.addWidget(QLabel("Numéro de page"), 0, 0)
            self.numPage_value = QSpinBox()
            self.numPage_value.setValue(self.info["numPage_value"]) 
            self.numPage_value.valueChanged.connect(self.change_numPage_value)
            self.layNum.addWidget(self.numPage_value, 0, 1)
        if self.info["numDiag_state"] == True:
            self.layNum.addWidget(QLabel("Numéro du premier diagramme"), 1, 0)
            self.numDiag_value = QSpinBox()
            self.numDiag_value.setValue(self.info["numDiag_value"]) 
            self.numDiag_value.valueChanged.connect(self.change_numDiag_value)
            self.layNum.addWidget(self.numDiag_value, 1, 1)

    def saveForm(self):
        if self.newFileName != self.currentFileName or self.newFileName == "":
            self.saveAs()
        else:
            print(self.currentFileName)
            with open(self.currentFileName, "w") as file:
                file.write("title_state,")
                file.write(str(self.info["title_state"]) + "|")
                file.write("numDiag_state,")
                file.write(str(self.info["numDiag_state"]) + "|")
                file.write("numDiag_text,")
                file.write(str(self.info["numDiag_text"]) + "|")
                file.write("color_state,")
                file.write(str(self.info["color_state"]) + "|")
                file.write("color_text,")
                file.write(str(self.info["color_text"]) + "|")
                file.write("format_text,")
                file.write(self.info["format_text"] + "|")
                file.write("flip_state,")
                file.write(str(self.info["flip_state"]) + "|")
                file.write("legend_state,")
                file.write(str(self.info["legend_state"]) + "|")
                file.write("cols_value,")
                file.write(str(self.info["cols_value"]) + "|")
                file.write("diags_value,")
                file.write(str(self.info["diags_value"]) + "|")
                file.write("margin_value,")
                file.write(str(self.info["margin_value"]) + "|")
                file.write("coord_state,")
                file.write(str(self.info["coord_state"]) + "|")
                file.write("down_state,")
                file.write(str(self.info["down_state"]) + "|")
                file.write("up_state,")
                file.write(str(self.info["up_state"]) + "|")
                file.write("left_state,")
                file.write(str(self.info["left_state"]) + "|")
                file.write("right_state,")
                file.write(str(self.info["right_state"]) + "|")

                file.write("title_text,")
                file.write(self.info["title_text"] + "|")
                file.write("numPage_value,")
                file.write(str(self.info["numPage_value"]) + "|")
                file.write("numDiag_value,")
                file.write(str(self.info["numDiag_value"]))

                for fen, leg, sym in zip(self.info["fens"],self.info["legends"],self.info["symbols"]):
                    file.write( '\n' + fen + '|' + leg + '|' + sym)
                
            self.changedFile = False

    def saveAs(self):
        self.newFileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","save","")
        if os.path.basename(self.newFileName) != "":
            self.currentFileName = self.newFileName
            self.setWindowTitle(os.path.basename(self.currentFileName) + " | CuteFEN Diagramm Generator")
            with open(self.currentFileName, "w") as file:
                file.write("title_state,")
                file.write(str(self.info["title_state"]) + "|")
                file.write("numDiag_state,")
                file.write(str(self.info["numDiag_state"]) + "|")
                file.write("numDiag_text,")
                file.write(str(self.info["numDiag_text"]) + "|")
                file.write("color_state,")
                file.write(str(self.info["color_state"]) + "|")
                file.write("color_text,")
                file.write(str(self.info["color_text"]) + "|")
                file.write("format_text,")
                file.write(self.info["format_text"] + "|")
                file.write("flip_state,")
                file.write(str(self.info["flip_state"]) + "|")
                file.write("legend_state,")
                file.write(str(self.info["legend_state"]) + "|")
                file.write("cols_value,")
                file.write(str(self.info["cols_value"]) + "|")
                file.write("diags_value,")
                file.write(str(self.info["diags_value"]) + "|")
                file.write("margin_value,")
                file.write(str(self.info["margin_value"]) + "|")
                file.write("coord_state,")
                file.write(str(self.info["coord_state"]) + "|")
                file.write("down_state,")
                file.write(str(self.info["down_state"]) + "|")
                file.write("up_state,")
                file.write(str(self.info["up_state"]) + "|")
                file.write("left_state,")
                file.write(str(self.info["left_state"]) + "|")
                file.write("right_state,")
                file.write(str(self.info["right_state"]) + "|")

                file.write("title_text,")
                file.write(self.info["title_text"] + "|")
                file.write("numPage_value,")
                file.write(str(self.info["numPage_value"]) + "|")
                file.write("numDiag_value,")
                file.write(str(self.info["numDiag_value"]))

                for fen, leg, sym in zip(self.info["fens"],self.info["legends"],self.info["symbols"]):
                    file.write( '\n' + fen + '|' + leg + '|' + sym)
                for arr in self.info["arrows"]:
                    arrows_num = 0
                    for a in arr:
                        arrows_num += 1
                    i = 1
                    if arrows_num != 0:
                        file.write('|')
                    for a in arr:
                        file.write(a[0] + ' ' + str(a[1]) + ' ' + str(a[2]))
                        if i < arrows_num:
                            file.write(',')

            self.changedFile = False

    def saveBeforeNew(self, result):
        if result == QDialog.DialogCode.Accepted:
            self.saveAs()
            self.currentFileName = "Nouveau document"
            self.setWindowTitle(self.currentFileName + " | CuteFEN Diagramm Generator")

            self.info["fens"].clear()
            self.info["legends"].clear()
            self.info["symbols"].clear()
            self.info["arrows"].clear()

            i = 0
            while i < self.info["max_diags"]:
                self.info["fens"].append("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
                self.info["legends"].append("Position de départ")
                self.info["symbols"].append("0000000000000000000000000000000000000000000000000000000000000000")
                self.info["arrows"].append([])
                i += 1

        if result == QDialog.DialogCode.Rejected:
            self.currentFileName = "Nouveau document"
            self.setWindowTitle(self.currentFileName + " | CuteFEN Diagramm Generator")

        self.load_default_settings()
        self.update_display(QDialog.DialogCode.Accepted)

    def update_display(self, result):
        if result == QDialog.DialogCode.Accepted:
            for widget in self.centralWidget().findChildren(QWidget):
                widget.deleteLater()

            self.load_widgets()

    def newDoc(self):
        if self.changedFile:
            dialog = SaveBeforeDialog(self)
            dialog.finished.connect(self.saveBeforeNew)
            dialog.exec()

    def openDoc(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selectionner le fichier","save","")
        if os.path.basename(fileName) == "":
            return(0)
        else:
            self.currentFileName = fileName
            self.newFileName = fileName

        self.setWindowTitle(os.path.basename(self.currentFileName) + " | CuteFEN Diagramm Generator")

        with open(fileName, 'r') as file:
            fields = file.read().split("\n")
            firsLine = fields[0].split("|")
            for pair in firsLine:
                info = pair.split(",")
                if re.search("state", info[0]):
                    if info[1] == "True":
                        self.info[info[0]] = True
                    else:
                        self.info[info[0]] = False
                elif re.search("value", info[0]):
                    self.info[info[0]] = int(info[1])
                elif re.search("text", info[0]):
                    self.info[info[0]] = info[1]

            i = 1
            while i <= self.info["diags_value"]:
                line = fields[i].split('|')
                self.info['fens'][i-1]=line[0]
                self.info['legends'][i-1]=line[1]
                self.info['symbols'][i-1]=line[2]
                fields_num = 0
                for l in line:
                    fields_num += 1

                if fields_num > 3:
                    arrows = line[3].split(',')
                    for arrow in arrows:
                        arr = arrow.split(' ')
                        self.info['arrows'][i-1].append([arr[0],int(arr[1]),int(arr[2])])
                i += 1

        for widget in self.centralWidget().findChildren(QWidget):
            widget.deleteLater()

        self.load_widgets()
        self.changedFile = False

    def preview(self):
        print("Afficher la page")

    def print(self):
        print("Imprimer")

    def openProp(self):
        dialog = PropDialog(self)
        dialog.finished.connect(self.update_display)
        dialog.exec()

    def undo(self):
        print("annuler")

    def redo(self):
        print("retablir")
        
    def openHelp(self):
        print("help")
    
    def openAbout(self):
        print("About")

    def saveBeforQuit(self, result):
        if result == QDialog.DialogCode.Accepted:
            self.saveAs()
            self.currentFileName = "Nouveau document"
            self.setWindowTitle(self.currentFileName + " | CuteFEN Diagramm Generator")

            self.info["fens"].clear()
            self.info["legends"].clear()
            self.info["symbols"].clear()
            self.info["arrows"].clear()

            i = 0
            while i < self.info["max_diags"]:
                self.info["fens"].append("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
                self.info["legends"].append("Position de départ")
                self.info["symbols"].append("0000000000000000000000000000000000000000000000000000000000000000")
                self.info["arrows"].append([])
                i += 1

        if result == QDialog.DialogCode.Rejected:
            self.currentFileName = "Nouveau document"
            self.setWindowTitle(self.currentFileName + " | CuteFEN Diagramm Generator")

        self.close()

    def quit(self):
        dialog = SaveBeforeDialog(self)
        dialog.finished.connect(self.saveBeforQuit)
        dialog.exec()

    # Slots des Widgets
    def change_title_text(self, text):
        self.info["title_text"] = text
        self.changedFile = True

    def change_fens(self, text):
        i = 0
        while i < self.info["max_diags"]:
            if self.sender().id == i:
                self.info["fens"][i] = text
                break
            i += 1
        self.changedFile = True

    def change_legends(self, text):
        i = 0
        while i < self.info["max_diags"]:
            if self.sender().id == i:
                self.info["legends"][i] = text
                break
            i += 1
        self.changedFile = True

    def change_numPage_value(self, value):
        self.info["numPage_value"] = value
        self.changedFile = True

    def change_numDiag_value(self, value):
        self.info["numDiag_value"] = value
        self.changedFile = True

class PropDialog(QDialog):
    finished = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Propriétés")


        self.info = {}
        self.implement_dicts()

        main_layout = QVBoxLayout()

        tab_widget = QTabWidget()

        page_tab = QWidget()
        diag_tab = QWidget()

        page_tab_layout = QGridLayout()
        diag_tab_layout = QGridLayout()

        page_tab.setLayout(page_tab_layout)
        diag_tab.setLayout(diag_tab_layout)

        self.title_state = QCheckBox("Afficher un titre")
        self.title_state.clicked.connect(self.set_title_state)
        self.title_state.setChecked(self.info["title_state"])
        page_tab_layout.addWidget(self.title_state,0,0)

        self.numPage_state = QCheckBox("Afficher un numéro de page")
        self.numPage_state.clicked.connect(self.set_numPage_state)
        self.numPage_state.setChecked(self.info["numPage_state"])
        page_tab_layout.addWidget(self.numPage_state,1,0)

        page_tab_layout.addWidget(QLabel("Orientation de la page"),2,0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["portrait","paysage"])
        self.format_combo.currentTextChanged.connect(self.set_format_text)
        self.format_combo.setCurrentText(self.info["format_text"])
        page_tab_layout.addWidget(self.format_combo,2,1)


        page_tab_layout.addWidget(QLabel("Nombre de diagrammes"),3,0)
        self.diags_value = QSpinBox()
        self.diags_value.setRange(1,15)
        self.diags_value.setValue(self.info["diags_value"])
        self.diags_value.valueChanged.connect(self.set_diags_value)
        page_tab_layout.addWidget(self.diags_value,3,1)

        page_tab_layout.addWidget(QLabel("Nombre de colonnes"),4,0)
        self.cols_value = QSpinBox()
        self.cols_value.setRange(1,5)
        self.cols_value.setValue(self.info["cols_value"])
        self.cols_value.valueChanged.connect(self.set_cols_value)
        page_tab_layout.addWidget(self.cols_value,4,1)

        page_tab_layout.addWidget(QLabel("Marges en pixels"),5,0)
        self.margin_value = QSpinBox()
        self.margin_value.setValue(20)
        self.margin_value.setRange(0, 200)
        self.margin_value.valueChanged.connect(self.set_margin_value)
        page_tab_layout.addWidget(self.margin_value,5,1)


        self.flip_state = QCheckBox("Retourner le plateau quand le trait est aux noirs")
        self.flip_state.clicked.connect(self.set_flip_state)
        self.flip_state.setChecked(self.info["flip_state"])
        diag_tab_layout.addWidget(self.flip_state,0,0)

        self.color_state = QCheckBox("Indiquer le trait par une pastille de couleur")
        self.color_state.clicked.connect(self.set_color_state)
        self.color_state.setChecked(self.info["color_state"])
        diag_tab_layout.addWidget(self.color_state,1,0)

        self.color_text_combo = QComboBox()
        self.color_text_combo.addItems(["à gauche","à droite"])
        self.color_text_combo.currentTextChanged.connect(self.set_color_text)
        self.color_text_combo.setCurrentText(self.info["color_text"])
        diag_tab_layout.addWidget(self.color_text_combo,1,1)

        self.numDiag_state = QCheckBox("Numéroter les diagrammes")
        self.numDiag_state.clicked.connect(self.set_numDiag_state)
        self.numDiag_state.setChecked(self.info["numDiag_state"])
        diag_tab_layout.addWidget(self.numDiag_state,2,0)

        self.numDiag_text_combo = QComboBox()
        self.numDiag_text_combo.addItems(["à gauche","à droite"])
        self.numDiag_text_combo.currentTextChanged.connect(self.set_numDiag_text)
        self.numDiag_text_combo.setCurrentText(self.info["numDiag_text"])
        diag_tab_layout.addWidget(self.numDiag_text_combo,2,1)

        self.legend_state = QCheckBox("Afficher une légende sous les diagrammes")
        self.legend_state.clicked.connect(self.set_legend_state)
        self.legend_state.setChecked(self.info["legend_state"])
        diag_tab_layout.addWidget(self.legend_state,3,0)

        self.coord_state = QCheckBox("Afficher les coordonnées")
        self.coord_state.clicked.connect(self.set_coord_state)
        self.coord_state.setChecked(self.info["coord_state"])
        diag_tab_layout.addWidget(self.coord_state,4,0)

        self.up_state = QCheckBox("au dessus")
        self.up_state.clicked.connect(self.set_up_state)
        self.up_state.setChecked(self.info["up_state"])
        diag_tab_layout.addWidget(self.up_state,5,0)

        self.down_state = QCheckBox("en dessous")
        self.down_state.clicked.connect(self.set_down_state)
        self.down_state.setChecked(self.info["down_state"])
        diag_tab_layout.addWidget(self.down_state,6,0)

        self.left_state = QCheckBox("à gauche")
        self.left_state.clicked.connect(self.set_left_state)
        self.left_state.setChecked(self.info["left_state"])
        diag_tab_layout.addWidget(self.left_state,7,0)

        self.right_state = QCheckBox("à droite")
        self.right_state.clicked.connect(self.set_right_state)
        self.right_state.setChecked(self.info["right_state"])
        diag_tab_layout.addWidget(self.right_state,8,0)

        tab_widget.addTab(page_tab, "Page")
        tab_widget.addTab(diag_tab, "Diagrammes")

        bottom_layout = QHBoxLayout()
        self.save_settings_push = QPushButton("Définir comme paramètres par défaut")
        self.save_settings_push.clicked.connect(self.save_settings)
        bottom_layout.addWidget(self.save_settings_push)

        self.exit_push = QPushButton("Fermer")
        self.exit_push.clicked.connect(self.exit)
        bottom_layout.addWidget(self.exit_push)
        
        self.cancel_push = QPushButton("Annuler")
        self.cancel_push.clicked.connect(self.cancel)
        bottom_layout.addWidget(self.cancel_push)

        main_layout.addWidget(tab_widget)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Paramètres")

    

        self.load_default_settings()

    def implement_dicts(self):
        for main_info in self.parent().info.items():
            self.info[main_info[0]] = main_info[1]

    def load_default_settings(self):
        pass

    def set_title_state(self, state):
        if state:
            self.info["title_state"] = True
        else:
            self.info["title_state"] = False

    def set_numPage_state(self, state):
        if state:
            self.info["numPage_state"] = True
        else:
            self.info["numPage_state"] = False

    def set_format_text(self, text):
        if text == "portrait":
            self.info["format_text"] = "portrait"
        else:
            self.info["format_text"] = "paysage"

    def set_diags_value(self, value):
        self.info["diags_value"] = value

    def set_cols_value(self, value):
        self.info["cols_value"] = value

    def set_margin_value(self, value):
        self.info["margin_value"] = value

    def set_flip_state(self, state):
        if state:
            self.info["flip_state"] = True
        else:
            self.info["flip_state"] = False

    def set_color_state(self, state):
        if state:
            self.info["color_state"] = True
        else:
            self.info["color_state"] = False

    def set_color_text(self, text):
        if text == "à gauche":
            self.info["color_text"] = "à gauche"
        else:
            self.info["color_text"] = "à droite"

    def set_numDiag_state(self, state):
        if state:
            self.info["numDiag_state"] = True
        else:
            self.info["numDiag_state"] = False

    def set_numDiag_text(self, text):
        if text == "à gauche":
            self.info["numDiag_text"] = "à gauche"
        else:
            self.info["numDiag_text"] = "à droite"

    def set_legend_state(self, state):
        if state:
            self.info["legend_state"] = True
        else:
            self.info["legend_state"] = False

    def set_coord_state(self, state):
        if state:
            self.info["coord_state"] = True
        else:
            self.info["coord_state"] = False
        
    def set_up_state(self, state):
        if state:
            self.info["up_state"] = True
        else:
            self.info["up_state"] = False

    def set_down_state(self, state):
        if state:
            self.info["down_state"] = True
        else:
            self.info["down_state"] = False

    def set_left_state(self, state):
        if state:
            self.info["left_state"] = True
        else:
            self.info["left_state"] = False

    def set_right_state(self, state):
        if state:
            self.info["right_state"] = True
        else:
            self.info["right_state"] = False

    def save_settings(self):
        fileName = os.path.join("settings", "default.txt")
        with open(fileName, "w") as file:
            file.write("title_state,")
            file.write(str(self.info["title_state"]) + "|")
            file.write("numPage_state,")
            file.write(str(self.info["numPage_state"]) + "|")
            file.write("format_text,")
            file.write(self.info["format_text"] + "|")
            file.write("diags_value,")
            file.write(str(self.info["diags_value"]) + "|")
            file.write("cols_value,")
            file.write(str(self.info["cols_value"]) + "|")
            file.write("margin_value,")
            file.write(str(self.info["margin_value"]) + "|")
            file.write("flip_state,")
            file.write(str(self.info["flip_state"]) + "|")
            file.write("color_state,")
            file.write(str(self.info["color_state"]) + "|")
            file.write("color_text,")
            file.write(str(self.info["color_text"]) + "|")
            file.write("numDiag_state,")
            file.write(str(self.info["numDiag_state"]) + "|")
            file.write("numDiag_text,")
            file.write(str(self.info["numDiag_text"]) + "|")
            file.write("legend_state,")
            file.write(str(self.info["legend_state"]) + "|")
            file.write("coord_state,")
            file.write(str(self.info["coord_state"]) + "|")
            file.write("up_state,")
            file.write(str(self.info["up_state"]) + "|")
            file.write("down_state,")
            file.write(str(self.info["down_state"]) + "|")
            file.write("left_state,")
            file.write(str(self.info["left_state"]) + "|")
            file.write("right_state,")
            file.write(str(self.info["right_state"]))
        self.close()

    def cancel(self):
        self.finished.emit(QDialog.DialogCode.Rejected)
        self.close()
    
    def exit(self):
        for diag_info in self.info.items():
            self.parent().info[diag_info[0]] = diag_info[1]
        self.finished.emit(QDialog.DialogCode.Accepted)
        self.close()

class SaveBeforeDialog(QDialog):
    finished = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Enregistrer le document?")
        self.main_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.label = QLabel("Attention, les modficiations non enregistrées seront perdues")
        self.main_layout.addWidget(self.label)

        self.save = QPushButton("Enregistrer")
        self.save.clicked.connect(self.save_clicked)
        self.doNotSave = QPushButton("Ne pas enregistrer")
        self.doNotSave.clicked.connect(self.doNotSave_clicked)
        self.cancel = QPushButton("Annuler")
        self.cancel.clicked.connect(self.cancel_clicked)

        self.buttons_layout.addWidget(self.save)
        self.buttons_layout.addWidget(self.cancel)
        self.buttons_layout.addWidget(self.doNotSave)

        self.main_layout.addLayout(self.buttons_layout)

        self.setLayout(self.main_layout)
        
    def save_clicked(self):
        self.finished.emit(QDialog.DialogCode.Accepted)
        self.close()

    def doNotSave_clicked(self):
        self.finished.emit(QDialog.DialogCode.Rejected)
        self.close()

    def cancel_clicked(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
