import os
import sys
import re
from PIL import ImageFont, Image
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QAction, QGradient, QIcon, QImage, QKeySequence, QPageSize, QPainter, QPalette, QPixmap, QMouseEvent, QCursor
from PyQt6.QtCore import QLine, QSize, Qt, QPoint, QSizeF
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QFormLayout, QHBoxLayout, QMainWindow, QLabel, QRadioButton, QScrollArea, QSizePolicy, QStackedLayout, QStatusBar, QTabWidget, QToolBar, QGridLayout, QVBoxLayout, QWidget, QLineEdit, QPushButton, QSpinBox, QDialog
from PyQt6.QtPrintSupport import QPrintPreviewDialog, QPrinter, QPrintDialog
from image_functions import draw_board, submit, test_fen, unpack_fen, flip_fen, repack_fen, flip_sym, flip_arrows, getCenter, getSquare
from req_functions import getFenFromId, openPgnFile

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
        self.changedFile = False
        self.changedInfo = False
        self.implement_dict()
        
        # Définition des actions
        self.act_Settings = QAction(QIcon.fromTheme("document-properties"), "&Paramètres", self)
        self.act_Settings.setStatusTip("Paramètres")
        self.act_Settings.setShortcut(QKeySequence("Ctrl+Shift+p"))
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

        self.act_Save_diags = QAction(QIcon.fromTheme("folder-pictures"), "&Enregistrer les diagrammes", self)
        self.act_Save_diags.setStatusTip("Enregistrer une image par diagramme")
        self.act_Save_diags.setShortcut(QKeySequence("Ctrl+Shift+i"))
        self.act_Save_diags.triggered.connect(self.saveDiags)

        self.act_Save_img = QAction(QIcon.fromTheme("image"), "&Page", self)
        self.act_Save_img.setStatusTip("Enregistrer l'image de la page")
        self.act_Save_img.setShortcut(QKeySequence("Ctrl+i"))
        self.act_Save_img.triggered.connect(self.saveImg)

        self.act_Img = QAction(QIcon.fromTheme("view-preview"), "&Aperçu de la page de diagrammes", self)
        self.act_Img.setStatusTip("Aperçu de la page de diagrammes")
        self.act_Img.setShortcut(QKeySequence("Ctrl+Shift+o"))
        self.act_Img.triggered.connect(self.preview)

        self.act_PGN = QAction(QIcon.fromTheme("text-plain"), "PGN", self)
        self.act_PGN.setStatusTip("Ouvrir un fichier pgn")
        self.act_PGN.setShortcut(QKeySequence("Ctrl+t"))
        self.act_PGN.triggered.connect(self.openPgn)

#       self.act_PGN = QAction(QIcon.fromTheme("document-print"), "Imprimer", self)
#       self.act_PGN.setStatusTip("Imprimer")
#       self.act_PGN.setShortcut(QKeySequence("Ctrl+p"))
#       self.act_PGN.triggered.connect(self.print)

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
        self.toolbar.addAction(self.act_PGN)
        self.toolbar.addAction(self.act_Save)
        self.toolbar.addAction(self.act_Save_as)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Img)
        self.toolbar.addAction(self.act_Save_img)
        self.toolbar.addAction(self.act_Save_diags)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Settings)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Help)
        self.toolbar.addAction(self.act_About)

        # Définition de la barre de menu
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("&Fichier")

        self.fileMenu.addAction(self.act_New)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Open)
        self.fileMenu.addAction(self.act_PGN)
        self.fileMenu.addAction(self.act_Save)
        self.fileMenu.addAction(self.act_Save_as)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Img)
        self.fileMenu.addAction(self.act_Save_img)
        self.fileMenu.addAction(self.act_Save_diags)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Settings)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Exit)


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
        self.info["color_state"] = True
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
        self.info["lichess"] = list()

        # variables manipulées par le programme
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
            self.title_text.setText(self.info["title_text"])
            self.title_text.textChanged.connect(self.change_title_text)
            self.layTitle.addWidget(self.title_text, 0, 1)

        # Section de formulaire
        self.layForm.addWidget(QLabel("Saisir un FEN ou un identifiant de problème Lichess            "), 0, 1)

        if self.info["legend_state"]:
            self.layForm.addWidget(QLabel("Saisir une légende"), 0, 3)

        self.fens = list()
        self.legends = list()
        self.edits = list()

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
            self.edits.append(QPushButton("Éditeur graphique"))
            self.edits[i-1].id = i-1
            self.edits[i-1].clicked.connect(self.openEdit)
            self.layForm.addWidget(self.edits[i-1], i, 4)
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

    def openProp(self):
        dialog = PropDialog(self)
        dialog.exec()

        result = dialog.result()
        if result == 1:
            for widget in self.centralWidget().findChildren(QWidget):
                widget.deleteLater()


            self.load_widgets()
            self.adjustSize()

    def saveForm(self):
        if self.newFileName != self.currentFileName or self.newFileName == "" or "Nouveau document" in self.currentFileName:
            self.saveAs()
        else:
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
                
            self.setWindowTitle(os.path.basename(self.currentFileName) + " | CuteFEN Diagramm Generator")
            self.changedFile = False

    def saveAs(self):
        self.newFileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","")
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

        else:
            self.newFileName = self.currentFileName

    def newDoc(self):
        if self.changedFile:
            dialog = SaveBeforeDialog()
            dialog.exec()
            result = dialog.result()

            if result == 1:
                self.saveForm()
            elif result == 3:
                return(0)

        self.implement_dict()
        self.load_default_settings()
        for widget in self.centralWidget().findChildren(QWidget):
            widget.deleteLater()

        self.load_widgets()
        self.currentFileName = "Nouveau document"
        self.newFileName = ""
        self.setWindowTitle(self.currentFileName + " | CuteFEN Diagramm Generator")

    def openDoc(self):
        if self.changedFile:
            dialog = SaveBeforeDialog()
            dialog.exec()
            result = dialog.result()

            if result == 1:
                self.saveForm()
            elif result == 3:
                return(0)
        fileName, _ = QFileDialog.getOpenFileName(self, "Selectionner le fichier","","")
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

    def quit(self):
        if self.changedFile:
            dialog = SaveBeforeDialog()
            dialog.exec()
            result = dialog.result()

            if result == 1:
                self.saveForm()
            elif result == 3:
                return(0)
        self.close()

    # Divers
    def preview(self):
        self.test = ""
        i = 0
        for fen in self.info["fens"]:
            if fen[0] == "#":
                self.info["fens"][i] = getFenFromId(fen)
                self.fens[i].setText(self.info["fens"][i])
            i += 1
        i = 0
        for fen in self.info["fens"]:
            self.test = test_fen(fen)
            if self.test != "OK":
                self.test += " dans le fen n°"
                self.test += str(i-1)

                alertDialog = ViewAlertDialog(self)
                alertDialog.exec()
                return(0)
            i += 1

        submit(self, self.info)

        view = ViewDialog(self)
        view.exec()

    def openPgn(self):
        pgn_diag = PGNDialog(self)
        pgn_diag.exec()
        print("imprimer")

    def saveDiags(self):
        self.test = ""
        i = 0
        for fen in self.info["fens"]:
            if fen[0] == "#":
                self.info["fens"][i] = getFenFromId(fen)
                self.fens[i].setText(self.info["fens"][i])
            i += 1
        i = 0
        for fen in self.info["fens"]:
            self.test = test_fen(fen)
            if self.test != "OK":
                self.test += " dans le fen n°"
                self.test += str(i-1)

                return(0)
            i += 1

        submit(self, self.info)
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","images","All Files (*);;PNG Files (*.png)")
        if fileName:
            if re.search('[.]png$', fileName):
                fileName += 'png'
            i = 0
            for box in self.info["boxes"]:
                if self.info["numDiag_state"]:
                    box.save(fileName + str(self.info["numDiag_value"] + i) + '.png')
                else:
                    box.save(fileName + str(i + 1) + '.png')
                i += 1

    def saveImg(self):
        self.test = ""
        i = 0
        for fen in self.info["fens"]:
            if fen[0] == "#":
                self.info["fens"][i] = getFenFromId(fen)
                self.fens[i].setText(self.info["fens"][i])
            i += 1
        i = 0
        for fen in self.info["fens"]:
            self.test = test_fen(fen)
            if self.test != "OK":
                self.test += " dans le fen n°"
                self.test += str(i-1)

                return(0)
            i += 1

        submit(self, self.info)
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","images","All Files (*);;PNG Files (*.png)")
        if fileName:
            if not re.search('[.]png$', fileName):
                fileName += '.png'
            self.info["page"].save(fileName)

        
    def openHelp(self):
        print("help")
    
    def openAbout(self):
        print("About")

    # Slots des Widgets
    def change_title_text(self, text):
        self.info["title_text"] = text
        self.changedFile = True
        self.setWindowTitle(os.path.basename(self.currentFileName) + "* | CuteFEN Diagramm Generator")

    def change_fens(self, text):
        i = 0
        while i < self.info["max_diags"]:
            if self.sender().id == i:
                self.info["fens"][i] = text
                break
            i += 1
        self.changedFile = True
        self.setWindowTitle(os.path.basename(self.currentFileName) + "* | CuteFEN Diagramm Generator")

    def change_legends(self, text):
        i = 0
        while i < self.info["max_diags"]:
            if self.sender().id == i:
                self.info["legends"][i] = text
                break
            i += 1
        self.changedFile = True
        self.setWindowTitle(os.path.basename(self.currentFileName) + "* | CuteFEN Diagramm Generator")

    def change_numPage_value(self, value):
        self.info["numPage_value"] = value
        self.changedFile = True
        self.setWindowTitle(os.path.basename(self.currentFileName) + "* | CuteFEN Diagramm Generator")

    def change_numDiag_value(self, value):
        self.info["numDiag_value"] = value
        self.changedFile = True
        self.setWindowTitle(os.path.basename(self.currentFileName) + "* | CuteFEN Diagramm Generator")

    def openEdit(self):
        self.info["active_editor"] = self.sender().id
        if self.info["fens"][self.info["active_editor"]][0] == "#":

            self.info["fens"][self.info["active_editor"]] = getFenFromId(self.info["fens"][self.info["active_editor"]])

        test = test_fen(self.info["fens"][self.info["active_editor"]])
        if test != "OK":
            self.info["fens"][self.info["active_editor"]] ="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w" 
            alertDialog = EditAlertDialog(self)
            alertDialog.exec()

        dialog = EditDialog(self)
        dialog.exec()

        result = dialog.result()
        if result == 1:
            for fen, text in zip(self.fens, self.info["fens"]):
                fen.setText(text)

class PGNDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)


        fileName, _ = QFileDialog.getOpenFileName(self, "Selectionner le fichier","","")
        self.setWindowTitle(os.path.basename(fileName))
        self.palette = app.palette()
        self.active_move = 0
        self.player = "w"

        self.pgn_data = openPgnFile(fileName)
        self.ext_fen = unpack_fen(self.pgn_data["fens"][self.active_move], False)
        self.board = draw_board(self.ext_fen,self.pgn_data["symbols"][self.active_move],self.pgn_data["arrows"][self.active_move])
        self.board.save("temp_board.jpg")
        pixmap = QPixmap("temp_board.jpg")

        self.label = QLabel()
        self.label.setFixedSize(600,600)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.setMouseTracking(True)

        self.headerLabel = list()
        for header in self.pgn_data["headers"]:
            self.headerLabel.append(QLabel(header))

        self.headerLayout = QVBoxLayout()
        for header in self.headerLabel:
            self.headerLayout.addWidget(header)

        self.movesLayout = QGridLayout()
        if len(self.pgn_data["piecesMoves"])%2 != 0:
            self.pgn_data["piecesMoves"].append("")

        self.moveLabels = list()
        for move in self.pgn_data["piecesMoves"]:
            self.moveLabels.append(QLabel(move))
        self.moveLabels[self.active_move].setStyleSheet(f"""
            QLabel {{
                background-color: {self.palette.color(QPalette.ColorRole.WindowText).name()};
                color: {self.palette.color(QPalette.ColorRole.Window).name()};
            }}
        """)
        i = 0
        j = 1
        while i < len(self.pgn_data["piecesMoves"]):
            self.movesLayout.addWidget(QLabel(str(j)),j-1,0)
            self.movesLayout.addWidget(self.moveLabels[i],j-1,1)
            self.movesLayout.addWidget(self.moveLabels[i+1],j-1,2)
            j += 1
            i += 2

        self.contentWidget = QWidget()
        self.contentWidget.setLayout(self.movesLayout)
        self.scollArea = QScrollArea()
        self.scollArea.setWidget(self.contentWidget)

        self.startButton = QPushButton("<<")
        self.startButton.clicked.connect(self.start)
        self.prevButton = QPushButton("<")
        self.prevButton.clicked.connect(self.prev)
        self.nextButton = QPushButton(">")
        self.nextButton.clicked.connect(self.next)
        self.endButton = QPushButton(">>")
        self.endButton.clicked.connect(self.end)

        self.activeFenLabel = QLabel("FEN : " +self.pgn_data["fens"][self.active_move])
        self.activeFenLabel.setFixedWidth(600)
        self.importFenButton = QPushButton("importer comme diagramme n°")
        self.importFenButton.clicked.connect(self.importFen)
        self.targetDiag = QSpinBox()
        self.targetDiag.setRange(1,self.parent().info["diags_value"])
        self.fenLayout = QHBoxLayout()
        self.fenLayout.addWidget(self.activeFenLabel)
        self.fenLayout.addWidget(self.importFenButton)
        self.fenLayout.addWidget(self.targetDiag)

        self.buttons_layout = QGridLayout()
        self.buttons_layout.addWidget(self.startButton,0,0)
        self.buttons_layout.addWidget(self.prevButton,1,0)
        self.buttons_layout.addWidget(self.nextButton,1,1)
        self.buttons_layout.addWidget(self.endButton,0,1)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.scollArea)
        self.rightLayout.addLayout(self.buttons_layout)

        self.imageLayout = QHBoxLayout()
        self.imageLayout.addLayout(self.headerLayout)
        self.imageLayout.addWidget(self.label)
        self.imageLayout.addLayout(self.rightLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.imageLayout)
        self.mainLayout.addLayout(self.fenLayout)
        self.setLayout(self.mainLayout)

    def start(self):
        self.active_move = 0
        self.activeFenLabel.setText("FEN : " +self.pgn_data["fens"][self.active_move])
        self.refresh()

    def prev(self):
        if self.active_move > 0:
            self.active_move -= 1
        self.activeFenLabel.setText("FEN : " +self.pgn_data["fens"][self.active_move])
        self.refresh()

    def next(self):
        if self.active_move < len(self.pgn_data["fens"])-1:
            self.active_move += 1
        self.activeFenLabel.setText("FEN : " +self.pgn_data["fens"][self.active_move])
        self.refresh()

    def end(self):
        self.active_move = len(self.pgn_data["fens"])-1
        self.activeFenLabel.setText("FEN : " +self.pgn_data["fens"][self.active_move])
        self.refresh()

    def importFen(self):
        self.parent().info["fens"][self.targetDiag.value()-1]=self.pgn_data["fens"][self.active_move]
        self.parent().fens[self.targetDiag.value()-1].setText(self.pgn_data["fens"][self.active_move])
        if self.targetDiag.value() < self.parent().info["diags_value"]:
            self.targetDiag.setValue(self.targetDiag.value()+1)

    def refresh(self):
        self.ext_fen = unpack_fen(self.pgn_data["fens"][self.active_move],False)
        self.board = draw_board(self.ext_fen,self.pgn_data["symbols"][self.active_move],self.pgn_data["arrows"][self.active_move])
        self.board.save("temp_board.jpg")
        pixmap = QPixmap("temp_board.jpg")
        self.label.setPixmap(pixmap)

        for label in self.moveLabels:
            label.setStyleSheet(f"""
                QLabel {{
                    color: {self.palette.color(QPalette.ColorRole.WindowText).name()};
                    background-color: {self.palette.color(QPalette.ColorRole.Window).name()};
                }}
            """)

        self.moveLabels[self.active_move].setStyleSheet(f"""
            QLabel {{
                background-color: {self.palette.color(QPalette.ColorRole.WindowText).name()};
                color: {self.palette.color(QPalette.ColorRole.Window).name()};
            }}
        """)

class EditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Édition du diagramme n°"+ str(self.parent().info["active_editor"]+1))

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.arrows_dir = os.path.join(self.current_dir, "arrows")
        # identification du fen a éditer
        self.diag_id = self.parent().info["active_editor"]

        # listes pours stocker les chaines de caractères qui encodent la position
        # (fen : pour l'export)
        # (ext_fen : usage interne à l'application)
        # (symbol_fen : pour les symboles)
        self.fen = self.parent().info["fens"][self.diag_id]
        self.color = self.fen.split()[1]
        self.ext_fen = unpack_fen(self.fen,False)
        self.symbol_fen = self.parent().info["symbols"][self.diag_id]
        self.printed_arrows = self.parent().info["arrows"][self.diag_id]
        if self.parent().info["flip_state"] and self.color == 'b':
            self.symbol_fen = flip_sym(self.symbol_fen)
            self.printed_arrows = flip_arrows(self.printed_arrows)

        # creation de l'image du plateau
        self.board_dir = os.path.join(self.current_dir, 'board')
        empty_board_path = os.path.join(self.board_dir, 'empty_board.jpg')

        # informations sur les boutons, le dictionnaire sera envoyé à la fonction create_button
        pieces_dir = os.path.join(self.current_dir, 'pieces')
        self.buttons = list()
        self.infos = {}
        bK_path = os.path.join(pieces_dir, 'bK.png')
        self.infos["k"]= bK_path
        bQ_path = os.path.join(pieces_dir, 'bQ.png')
        self.infos["q"]= bQ_path
        bB_path = os.path.join(pieces_dir, 'bB.png')
        self.infos["b"]= bB_path
        bN_path = os.path.join(pieces_dir, 'bN.png')
        self.infos["n"]= bN_path
        bR_path = os.path.join(pieces_dir, 'bR.png')
        self.infos["r"]= bR_path
        bP_path = os.path.join(pieces_dir, 'bP.png')
        self.infos["p"]= bP_path
        wK_path = os.path.join(pieces_dir, 'wK.png')
        self.infos["K"]= wK_path
        wQ_path = os.path.join(pieces_dir, 'wQ.png')
        self.infos["Q"]= wQ_path
        wB_path = os.path.join(pieces_dir, 'wB.png')
        self.infos["B"]= wB_path
        wN_path = os.path.join(pieces_dir, 'wN.png')
        self.infos["N"]= wN_path
        wR_path = os.path.join(pieces_dir, 'wR.png')
        self.infos["R"]= wR_path
        wP_path = os.path.join(pieces_dir, 'wP.png')
        self.infos["P"]= wP_path

        symbols_dir = os.path.join(self.current_dir, 'symbols')
        bt_path = os.path.join(symbols_dir, 'bt.png')
        self.infos["t"]= bt_path
        by_path = os.path.join(symbols_dir, 'by.png')
        self.infos["y"]= by_path
        bg_path = os.path.join(symbols_dir, 'bg.png')
        self.infos["g"]= bg_path
        bo_path = os.path.join(symbols_dir, 'bo.png')
        self.infos["o"]= bo_path

        wt_path = os.path.join(symbols_dir, 'wt.png')
        self.infos["T"]= wt_path
        wy_path = os.path.join(symbols_dir, 'wy.png')
        self.infos["Y"]= wy_path
        wg_path = os.path.join(symbols_dir, 'wg.png')
        self.infos["G"]= wg_path
        wo_path = os.path.join(symbols_dir, 'wo.png')
        self.infos["O"]= wo_path

        # création des widget
        combo = QComboBox()
        combo.setMaximumWidth(200)
        combo.addItems(["Pièces", "Formes", "Flèches"])
        combo.currentTextChanged.connect(self.text_changed)

        # choix du trait
        self.radio_white = QRadioButton("Trait aux blancs")
        self.radio_white.id = 'w'
        self.radio_white.clicked.connect(self.set_color)
        if self.color == 'w':
            self.radio_white.setChecked(True)
        self.radio_black = QRadioButton("Trait aux noirs")
        self.radio_black.id = 'b'
        self.radio_black.clicked.connect(self.set_color)
        if self.color == 'b':
            self.radio_black.setChecked(True)
        self.prev_color = self.color

        # renversement du plateau
        self.check_flip = QCheckBox("Retourner le plateau")
        self.check_flip.clicked.connect(self.flip_board)
        
        self.start_pos = QPushButton("Position de départ")
        self.start_pos.clicked.connect(self.pos_click)
        self.start_pos.id = 0
        self.empty_sym = QPushButton("Effacer les annotations")
        self.empty_sym.clicked.connect(self.pos_click)
        self.empty_sym.id = 2
        self.empty_pos = QPushButton("Vider l'échiquier")
        self.empty_pos.clicked.connect(self.pos_click)
        self.empty_pos.id = 1
        self.save_pos = QPushButton("Enregistrer l'image")
        self.save_pos.clicked.connect(self.pos_click)
        self.save_pos.id = 3
        self.submit = QPushButton("Valider")
        self.submit.id = "edit"
        self.submit.clicked.connect(self.submit_click)

        # création du label à afficher dans la fenêtre

        pixmap = QPixmap(empty_board_path)
        self.label = QLabel()
        self.label.setFixedSize(600,600)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.setMouseTracking(True)
        self.label.mousePressEvent = self.pressEvent
        self.label.mouseReleaseEvent = self.releaseEvent
        
        # création des boutons
        for k,v in self.infos.items():
            self.buttons.append(self.create_button(k,v))
        for button in self.buttons:
            button.setChecked(False)

        # pour récupérer la valeur de la pièce à coller dans l'éditeur
        # par défaut, le roi noir
        self.active_piece = 'k'
        # pour récupérer la valeur de la pièce à déplacer dans l'éditeur
        self.dragged_piece = '0'

        # image de la pièce à déplacer
        self.dragged_image = None
        # position du curseur
        self.position = None

        # position de départ et d'arrivée d'une flèche
        self.arrow_start = None
        self.arrow_end = None
        self.arr_img = None

        #layouts de pièces
        blacks_layout = QVBoxLayout()
        whites_layout = QVBoxLayout()
        b_sym_layout = QVBoxLayout()
        b_sym2_layout = QVBoxLayout()
        for button in self.buttons:
            if button.id in ['k','q','b','n','r','p']:
                blacks_layout.addWidget(button)
            elif button.id in ['K','Q','B','N','R','P']:
                whites_layout.addWidget(button)
            elif button.id in ['g','t','o','y']:
                b_sym_layout.addWidget(button)
            elif button.id in ['G','T','O','Y']:
                b_sym2_layout.addWidget(button)

        label_layout = QVBoxLayout()
        label_layout.addWidget(self.label)
        bot_layout = QHBoxLayout()
        bot_layout2 = QHBoxLayout()
        label_layout.addLayout(bot_layout2)
        label_layout.addLayout(bot_layout)
        
        # création des onglets
        pieces_tab = QWidget()
        pieces_layout = QHBoxLayout()
        pieces_layout.addLayout(blacks_layout)
        pieces_layout.addLayout(whites_layout)
        pieces_tab.setLayout(pieces_layout)

        symbols_tab =QWidget()
        symbols_layout = QHBoxLayout()
        symbols_layout.addLayout(b_sym_layout)
        symbols_layout.addLayout(b_sym2_layout)
        symbols_tab.setLayout(symbols_layout)

        arrows_tab = QWidget()
        arrows_layout = QVBoxLayout()
        arrows_tab.setLayout(arrows_layout)

        # création du stacked layout
        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(pieces_tab)
        self.stack_layout.addWidget(symbols_tab)
        self.stack_layout.addWidget(arrows_tab)

        left_layout = QVBoxLayout()
        left_layout.addWidget(combo)
        left_layout.addLayout(self.stack_layout)
        left_layout.addWidget(self.check_flip)
        left_layout.addWidget(self.radio_white)
        left_layout.addWidget(self.radio_black)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.start_pos)
        right_layout.addWidget(self.empty_pos)
        right_layout.addWidget(self.empty_sym)
        right_layout.addWidget(self.save_pos)
        right_layout.addWidget(self.submit)
        right_layout.setAlignment(self.save_pos, Qt.AlignmentFlag.AlignBottom)
        right_layout.setAlignment(self.submit, Qt.AlignmentFlag.AlignBottom)

        # layout général
        upper_layout = QVBoxLayout()
        layout = QHBoxLayout()

        layout.addLayout(left_layout)
        layout.addLayout(label_layout)
        layout.addLayout(right_layout)
        upper_layout.addLayout(layout)
        self.setLayout(upper_layout)

        self.refresh()

    def create_button(self,k,v):
        button = QPushButton()
        button.setFixedSize(75,75)
        button.setIconSize(QSize(60,60))
        button.id = k
        button.path = v
        button.setIcon(QIcon(v))
        button.setCheckable(True)
        button.clicked.connect(self.pieces_click)
        button.image = Image.open(v)
        button.image = button.image.resize((75,75))
        return(button)

    def set_color(self):
        self.color = self.sender().id
        if self.color != self.prev_color:
            self.prev_color = self.color

    def flip_board(self):
        self.ext_fen = flip_fen(self.ext_fen)
        self.symbol_fen = flip_sym(self.symbol_fen)
        self.printed_arrows = flip_arrows(self.printed_arrows)
        self.refresh()

    def text_changed(self, s):
        if s == "Formes":
            self.stack_layout.setCurrentIndex(1)
            self.active_piece = '0'
        elif s == "Pièces":
            self.stack_layout.setCurrentIndex(0)
            self.active_piece = '0'
        elif s == "Flèches":
            self.stack_layout.setCurrentIndex(2)
            self.active_piece = '0'

    def pos_click(self):
        if self.sender().id == 0:
            self.ext_fen = 'rnbqkbnrpppppppp00000000000000000000000000000000PPPPPPPPRNBQKBNR'
            self.symbol_fen = '0000000000000000000000000000000000000000000000000000000000000000'
            if self.color == 'b':
#               self.ext_fen = flip_fen(self.ext_fen)
                self.color = "w"
                self.radio_white.setChecked(True)
        elif self.sender().id == 2:
            self.symbol_fen = '0000000000000000000000000000000000000000000000000000000000000000'
            self.printed_arrows = []
        elif self.sender().id == 1:
            self.ext_fen = '0000000000000000000000000000000000000000000000000000000000000000'
            self.symbol_fen = '0000000000000000000000000000000000000000000000000000000000000000'
        elif self.sender().id == 3:
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","images","PNG Files (*.png)")
            if fileName:
                if not re.search('[.]png$', fileName):
                    fileName += '.png'
                self.board_img.save(fileName)

        self.refresh()

    def pieces_click(self):
        if self.active_piece == self.sender().id:
            self.active_piece = '0'
        else:
            self.active_piece = self.sender().id
        for button in self.buttons:
            if button.id != self.sender().id:
                button.setChecked(False)

    def pressEvent(self, event: QMouseEvent):
        self.position = event.pos()
        i = 1
        j = 1
        x = 0
        y = 0
        blit_x = 0
        blit_y = 0
        # renvoie blit_x et blit_y (orignie de la case cliquée)
        while x < 600:
            if self.position.x() > x and self.position.x() <= x+75:
                blit_x = x
            i += 1
            x += 75
        
        while y < 600:
            if self.position.y() > y and self.position.y() <= y+75:
                blit_y = y
            j += 1
            y += 75

        # blit_pos récupère le rang de la case cliquée (de 0 à 63)
        blit_pos = int((((blit_x/75)+1) + (blit_y/75) * 8)-1)

        # modification des codes *_state
        # par drag n' drop au clic central
        if event.button() == Qt.MouseButton.MiddleButton:

            self.dragged_piece = self.ext_fen[blit_pos]
            for button in self.buttons:
                if self.dragged_piece == button.id:
                    self.dragged_image = QPixmap.fromImage(ImageQt(button.image))
                    cursor = QCursor(self.dragged_image)
                    self.setCursor(cursor)
            self.ext_fen = self.ext_fen[:blit_pos] + '0' + self.ext_fen[blit_pos+1:]

        else:
            if self.stack_layout.currentIndex() == 0:
                # par collage de la pièce active au clic gauche
                if event.button() == Qt.MouseButton.LeftButton:
                    if self.ext_fen[blit_pos] == self.active_piece:
                        self.ext_fen = self.ext_fen[:blit_pos] + '0' + self.ext_fen[blit_pos+1:]
                    else:
                        self.ext_fen = self.ext_fen[:blit_pos] + self.active_piece + self.ext_fen[blit_pos+1:]
                # par collage de la pièce de couleur opposée au clic droit
                elif event.button() == Qt.MouseButton.RightButton:
                    if self.active_piece.isupper():
                        mirror_piece = self.active_piece.lower()
                    else:
                        mirror_piece = self.active_piece.upper()
                    if self.ext_fen[blit_pos] == mirror_piece:
                        self.ext_fen = self.ext_fen[:blit_pos] + self.active_piece + self.ext_fen[blit_pos+1:]
                    else:
                        self.ext_fen = self.ext_fen[:blit_pos] + mirror_piece + self.ext_fen[blit_pos+1:]
            elif self.stack_layout.currentIndex() == 1:
                # collage de la forme active au clic gauche
                if event.button() == Qt.MouseButton.LeftButton:
                    if self.symbol_fen[blit_pos] == self.active_piece:
                        self.symbol_fen = self.symbol_fen[:blit_pos] + '0' + self.symbol_fen[blit_pos+1:]
                    else:
                        self.symbol_fen = self.symbol_fen[:blit_pos] + self.active_piece + self.symbol_fen[blit_pos+1:]
                # collage de la forme de couleur opposée au clic droit
                elif event.button() == Qt.MouseButton.RightButton:
                    if self.active_piece.isupper():
                        mirror_piece = self.active_piece.lower()
                    else:
                        mirror_piece = self.active_piece.upper()
                    if self.symbol_fen[blit_pos] == mirror_piece:
                        self.symbol_fen = self.symbol_fen[:blit_pos] + self.active_piece + self.symbol_fen[blit_pos+1:]
                    else:
                        self.symbol_fen = self.symbol_fen[:blit_pos] + mirror_piece + self.symbol_fen[blit_pos+1:]
            elif self.stack_layout.currentIndex() == 2:
                self.arrow_start = blit_pos

        self.refresh()
        
    def releaseEvent(self, event):
        self.position = event.pos()
        i = 1
        j = 1
        x = 0
        y = 0
        blit_x = 0
        blit_y = 0

        # renvoie blit_x et blit_y (orignie de la case cliquée)
        while x < 600:
            if self.position.x() > x and self.position.x() <= x+75:
                blit_x = x
            i += 1
            x += 75
        
        while y < 600:
            if self.position.y() > y and self.position.y() <= y+75:
                blit_y = y
            j += 1
            y += 75

        # blit_pos récupère le rang de la case cliquée (de 0 à 63)
        blit_pos = int((((blit_x/75)+1) + (blit_y/75) * 8)-1)
       
        # déplace une pièce
        if event.button() == Qt.MouseButton.MiddleButton:
            self.ext_fen = self.ext_fen[:blit_pos] + self.dragged_piece + self.ext_fen[blit_pos+1:]
            
            self.refresh()
            self.setCursor(Qt.CursorShape.ArrowCursor)

        elif self.stack_layout.currentIndex() == 2:
            # déssine une flèche
            if blit_pos != self.arrow_start:
                self.arrow_end = blit_pos

                # identification du point de collage de la flèche
                start_x = self.arrow_start%8+1
                start_y = int(self.arrow_start/8+1)
                end_x = self.arrow_end%8+1
                end_y = int(self.arrow_end/8+1)

                if start_x > end_x:
                    img_x = (end_x-1)*75
                else:
                    img_x = (start_x-1)*75

                if start_y > end_y:
                    img_y = (end_y-1)*75
                else:
                    img_y = (start_y-1)*75

                # identification du sens de la flèche et de la taille de l'image
                if start_y < end_y:
                    height = end_y - start_y + 1
                    if start_x < end_x:
                        width = end_x - start_x +1
                        direction = 3
                    elif start_x > end_x:
                        width = start_x - end_x +1
                        direction = 1
                    else:
                        width = 1
                        direction = 2
                elif start_y > end_y:
                    height = start_y - end_y + 1
                    if start_x < end_x:
                        width = end_x - start_x +1
                        direction = 9
                    elif start_x > end_x:
                        width = start_x - end_x +1
                        direction = 7
                    else:
                        width = 1
                        direction = 8
                else:
                    height = 1
                    if start_x < end_x:
                        width = end_x - start_x +1
                        direction = 6
                    elif start_x > end_x:
                        width = start_x - end_x +1
                        direction = 4
                arrow_name = str(direction) + str(width) + str(height) + '.png'
                arrow_path = os.path.join(self.arrows_dir, arrow_name)


                try:
                    # vérifie que la flèche correspondante existe
                    self.arr_img = Image.open(arrow_path)
                    # teste si la même flèche est déjà trâcée
                    new_arrow = [arrow_name, img_x, img_y]
                    same_arrow = False
                    for arrow in self.printed_arrows:
                        # si oui elle est effacée
                        if new_arrow == arrow:
                            self.printed_arrows.remove(arrow)
                            same_arrow = True
                            new_arrow = None

                    # si non elle est ajoutée
                    if not same_arrow:
                        self.printed_arrows.append(new_arrow)

                    self.refresh()
                except:
                    print('pas de fleche pour ce tracé')

    def refresh(self):
        empty1_path = os.path.join(self.board_dir, 'empty1.png')
        self.pieces_img = Image.open(empty1_path)
        self.pieces_img = self.pieces_img.resize((600,600))
        self.symbols_img = Image.open(empty1_path)
        self.symbols_img = self.symbols_img.resize((600,600))
        self.arrows_img = Image.open(empty1_path)
        self.arrows_img = self.arrows_img.resize((600,600))

        # colle les pièces sur l'overlay
        i = 0
        for char in self.ext_fen:
            for button in self.buttons:
                if char == button.id:
                    self.pieces_img.paste(button.image, ((i%8)*75,int(i/8)*75), button.image)
            i += 1

        i = 0
        for sym in self.symbol_fen:
            for button in self.buttons:
                if sym == button.id:
                    self.symbols_img.paste(button.image, ((i%8)*75,int(i/8)*75), button.image)
            i +=1

        i = 0
        for arr in self.printed_arrows:
            rs_x= int(arr[0][1])*75
            rs_y= int(arr[0][2])*75
            img_path = os.path.join(self.arrows_dir, arr[0])
            img = Image.open(img_path)
            img = img.resize((rs_x,rs_y))
            self.arrows_img.paste(img, (arr[1], arr[2]), img) 

        # réinitialise l'image du plateau vide
        empty_board_path = os.path.join(self.board_dir, 'empty_board.jpg')
        self.board_img = Image.open(empty_board_path)
        self.board_img = self.board_img.resize((600,600))
        # colle l'overlay sur le plateau
        self.symbols_img.paste(self.arrows_img, (0,0), self.arrows_img)
        self.pieces_img.paste(self.symbols_img, (0,0), self.symbols_img)
        self.board_img.paste(self.pieces_img, (0,0), self.pieces_img)
        temp_board_path = os.path.join(self.current_dir,"temp_board.jpg")
        self.board_img.save(temp_board_path)
        # raffraichit le pixmap à afficher dans le label
        new_pixmap = QPixmap(temp_board_path)
        self.label.setPixmap(new_pixmap)

        self.fen = repack_fen(self.ext_fen)

    def submit_click(self):
        if self.check_flip.isChecked():
            self.fen = flip_fen(self.fen)
            self.symbol_fen = flip_sym(self.symbol_fen)
            self.printed_arrows = flip_arrows(self.printed_arrows)
        self.fen += (' ' + self.color)
        self.parent().info["fens"][self.parent().info["active_editor"]]=self.fen
        self.parent().info["symbols"][self.parent().info["active_editor"]]=self.symbol_fen
        self.parent().info["arrows"][self.parent().info["active_editor"]]=self.printed_arrows
        self.done(1)

class EditAlertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Erreur")
        label = QLabel("Le code saisi est incorrect.\nLa position de départ sera chargée par défaut.")
        closeDialog = QPushButton("Ok")
        closeDialog.clicked.connect(self.pushQuit)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(closeDialog)
        self.setLayout(layout)

    def pushQuit(self):
        self.close()

class PropDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        if self.parent().changedInfo:
            self.setWindowTitle("Paramètres*")
        else:
            self.setWindowTitle("Paramètres")

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

        self.numDiag_state = QCheckBox("Numéroter les diagrammes")
        self.numDiag_state.clicked.connect(self.set_numDiag_state)
        self.numDiag_state.setChecked(self.info["numDiag_state"])
        diag_tab_layout.addWidget(self.numDiag_state,2,0)

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

        if not self.info["coord_state"]:
            self.up_state.setEnabled(False)
            self.down_state.setEnabled(False)
            self.right_state.setEnabled(False)
            self.left_state.setEnabled(False)
        else:
            self.up_state.setEnabled(True)
            self.down_state.setEnabled(True)
            self.right_state.setEnabled(True)
            self.left_state.setEnabled(True)

        tab_widget.addTab(page_tab, "Page")
        tab_widget.addTab(diag_tab, "Diagrammes")

        bottom_layout = QHBoxLayout()
        self.save_settings_push = QPushButton("Définir comme paramètres par défaut")
        self.save_settings_push.clicked.connect(self.new_save_settings)
        bottom_layout.addWidget(self.save_settings_push)

        self.exit_push = QPushButton("Fermer")
        self.exit_push.clicked.connect(self.new_exit)
        bottom_layout.addWidget(self.exit_push)
        
        self.cancel_push = QPushButton("Annuler")
        self.cancel_push.clicked.connect(self.new_cancel)
        bottom_layout.addWidget(self.cancel_push)

        main_layout.addWidget(tab_widget)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def implement_dicts(self):
        for main_info in self.parent().info.items():
            self.info[main_info[0]] = main_info[1]

    def set_title_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["title_state"] = True
        else:
            self.info["title_state"] = False

    def set_numPage_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["numPage_state"] = True
        else:
            self.info["numPage_state"] = False

    def set_format_text(self, text):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if text == "portrait":
            self.info["format_text"] = "portrait"
        else:
            self.info["format_text"] = "paysage"

    def set_diags_value(self, value):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        self.info["diags_value"] = value

    def set_cols_value(self, value):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        self.info["cols_value"] = value

    def set_margin_value(self, value):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        self.info["margin_value"] = value

    def set_flip_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["flip_state"] = True
        else:
            self.info["flip_state"] = False

    def set_color_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["color_state"] = True
        else:
            self.info["color_state"] = False

    def set_numDiag_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["numDiag_state"] = True
        else:
            self.info["numDiag_state"] = False

    def set_legend_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["legend_state"] = True
        else:
            self.info["legend_state"] = False

    def set_coord_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["coord_state"] = True
            self.up_state.setEnabled(True)
            self.down_state.setEnabled(True)
            self.right_state.setEnabled(True)
            self.left_state.setEnabled(True)
        else:
            self.info["coord_state"] = False
            self.up_state.setEnabled(False)
            self.down_state.setEnabled(False)
            self.right_state.setEnabled(False)
            self.left_state.setEnabled(False)
        
    def set_up_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["up_state"] = True
        else:
            self.info["up_state"] = False

    def set_down_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["down_state"] = True
        else:
            self.info["down_state"] = False

    def set_left_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["left_state"] = True
        else:
            self.info["left_state"] = False

    def set_right_state(self, state):
        self.parent().changedInfo = True
        self.setWindowTitle("Paramètres*")
        if state:
            self.info["right_state"] = True
        else:
            self.info["right_state"] = False

    def new_save_settings(self):
        self.parent().changedInfo = False
        self.setWindowTitle("Paramètres")
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
            file.write("numDiag_state,")
            file.write(str(self.info["numDiag_state"]) + "|")
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

    def new_exit(self):

        self.parent().info["title_state"] = self.info["title_state"]
        self.parent().info["numPage_state"] = self.info["numPage_state"]
        self.parent().info["format_text"] = self.info["format_text"]
        self.parent().info["diags_value"] = self.info["diags_value"]
        self.parent().info["cols_value"] = self.info["cols_value"]
        self.parent().info["margin_value"] = self.info["margin_value"]
        self.parent().info["flip_state"] = self.info["flip_state"]
        self.parent().info["color_state"] = self.info["color_state"]
        self.parent().info["numDiag_state"] = self.info["numDiag_state"]
        self.parent().info["legend_state"] = self.info["legend_state"]
        self.parent().info["coord_state"] = self.info["coord_state"]
        self.parent().info["up_state"] = self.info["up_state"]
        self.parent().info["down_state"] = self.info["down_state"]
        self.parent().info["left_state"] = self.info["left_state"]
        self.parent().info["right_state"] = self.info["right_state"]
        self.done(1)

    def new_cancel(self):
        self.done(3)

class SaveBeforeDialog(QDialog):
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
        self.done(1)

    def doNotSave_clicked(self):
        self.done(2)

    def cancel_clicked(self):
        self.done(3)

class ViewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(os.path.basename(self.parent().currentFileName))
        temp_jpg = "temp.jpg"
        pixmap = QPixmap(temp_jpg)
        self.label = QLabel()
        if self.parent().info["format_text"] == "portrait":
            self.label.setFixedSize(473, 668)
#           self.setFixedSize(493, 733)
        else:
            self.label.setFixedSize(891, 630)
#           self.setFixedSize(911, 690)
        
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.save_page_push = QPushButton("Enregistrer la page")
        self.save_page_push.id = "page"
        self.save_page_push.clicked.connect(self.push)
        self.save_diags_push = QPushButton("Enregistrer les diagrammes")
        self.save_diags_push.id = "diags"
        self.save_diags_push.clicked.connect(self.push)
        self.print_push = QPushButton("Imprimer la page")
        self.print_push.id = "diags"
        self.print_push.clicked.connect(self.push)
        self.cancel_push = QPushButton("Fermer")
        self.cancel_push.id = "cancel"
        self.cancel_push.clicked.connect(self.push)

        page_layout = QHBoxLayout()
        page_layout.setStretchFactor(self.label, 3)
        buttons_layout = QVBoxLayout()

        buttons_layout.addWidget(self.save_page_push)
        buttons_layout.addWidget(self.save_diags_push)
        buttons_layout.addWidget(self.print_push)
        buttons_layout.addWidget(self.cancel_push)
        buttons_layout.setAlignment(self.cancel_push, Qt.AlignmentFlag.AlignBottom)

        page_layout.addWidget(self.label)
        page_layout.addLayout(buttons_layout)

        self.setLayout(page_layout)

    def push(self):
        if self.sender().id == "page":
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","images","All Files (*);;PNG Files (*.png)")
            if fileName:
                if not re.search('[.]png$', fileName):
                    fileName += '.png'
                self.parent().info["page"].save(fileName)

        elif self.sender().id == "diags":
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","images","All Files (*);;PNG Files (*.png)")
            if fileName:
                if re.search('[.]png$', fileName):
                    fileName += 'png'
                i = 0
                for box in self.parent().info["boxes"]:
                    if self.parent().info["index_state"]:
                        box.save(fileName + str(self.parent().info["index_value"] + i) + '.png')
                    else:
                        box.save(fileName + str(i + 1) + '.png')
                    i += 1
        elif self.sender().id == "cancel":
            self.close()

class ViewAlertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Erreur")
        label = QLabel(self.parent().test)
        closeDialog = QPushButton("Ok")
        closeDialog.clicked.connect(self.pushQuit)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(closeDialog)
        self.setLayout(layout)

    def pushQuit(self):
        self.close()

class Alert(QDialog):
    def __init__(self, error):
        super().__init__()

        self.setWindowTitle("Erreur")
        alert_msg = QLabel(error)
        self.layout = QHBoxLayout()
        self.layout.addWidget(alert_msg)
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
