from ctypes import alignment
import sys
import re
import os

from PIL import ImageFont, Image
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap, QIcon, QMouseEvent, QDropEvent, QDrag, QImage, QPainter, QCursor, QPen, QColor
from PyQt6.QtCore import QSize, Qt, QPoint
import PyQt6.QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QTabWidget,
    QStackedLayout,
    QComboBox,
    QWidget,
    QRadioButton,
    QMainWindow,
    QSpinBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QCheckBox,
    QLabel,
    QLineEdit,
    QDialog,
    QFrame,
    QFileDialog
)

from fonctions import submit, test, unpack_fen, flip_fen, repack_fen, flip_sym, flip_arrows, getCenter, getSquare

class ViewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        temp_jpg = os.path.join("temp","temp.jpg")
        pixmap = QPixmap(temp_jpg)
        self.label = QLabel()
        if self.parent().parent().info["format"] == "portrait":
            self.label.setFixedSize(473, 668)
            self.setFixedSize(493, 733)
        else:
            self.label.setFixedSize(891, 630)
            self.setFixedSize(911, 690)
        
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.save_page_push = QPushButton("Enregistrer la page")
        self.save_page_push.id = "page"
        self.save_page_push.clicked.connect(self.push)
        self.save_diags_push = QPushButton("Enregistrer les diagrammes")
        self.save_diags_push.id = "diags"
        self.save_diags_push.clicked.connect(self.push)
        self.cancel_push = QPushButton("Annuler")
        self.cancel_push.id = "cancel"
        self.cancel_push.clicked.connect(self.push)

        page_layout = QVBoxLayout()
        page_layout.setStretchFactor(self.label, 3)
        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(self.save_page_push)
        buttons_layout.addWidget(self.save_diags_push)
        buttons_layout.addWidget(self.cancel_push)

        page_layout.addWidget(self.label)
        page_layout.addLayout(buttons_layout)

        self.setLayout(page_layout)

    def push(self):
        if self.sender().id == "page":
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;PNG Files (*.png)")
            if fileName:
                if not re.search('[.]png$', fileName):
                    fileName += '.png'
                self.parent().parent().info["page"].save(fileName)

        elif self.sender().id == "diags":
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;PNG Files (*.png)")
            if fileName:
                if re.search('[.]png$', fileName):
                    fileName += 'png'
                i = 0
                for box in self.parent().parent().info["boxes"]:
                    if self.parent().parent().info["index_state"]:
                        box.save(fileName + str(self.parent().parent().info["index_value"] + i) + '.png')
                    else:
                        box.save(fileName + str(i + 1) + '.png')
                    i += 1
        elif self.sender().id == "cancel":
            self.close()

class EditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.arrows_dir = os.path.join(self.current_dir, "arrows")
        self.setFixedSize(820,690)
        def create_button(k,v):
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

        # identification du fen a éditer
        self.diag_id = self.parent().parent().info["active_editor"]

        # listes pours stocker les chaines de caractères qui encodent la position
        # (fen : pour l'export)
        # (ext_fen : usage interne à l'application)
        # (symbol_fen : pour les symboles)
        self.fen = self.parent().parent().info["fens"][self.diag_id]
        self.color = self.fen.split()[1]
        self.ext_fen = unpack_fen(self.fen, self.parent().parent().info["flip_state"])
        self.symbol_fen = self.parent().parent().info["symbols"][self.diag_id]
        self.printed_arrows = self.parent().parent().info["arrows"][self.diag_id]
        if self.parent().parent().info["flip_state"] and self.color == 'b':
            self.symbol_fen = flip_sym(self.symbol_fen)
            self.printed_arrows = flip_arrows(self.printed_arrows)

        # creation de l'image du plateau
        self.board_dir = os.path.join(self.current_dir, 'board')
        empty_board_path = os.path.join(self.board_dir, 'empty_board.jpg')
#       self.board_img = Image.open(empty_board_path)
#       self.board_img = self.board_img.resize((600,600))

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

        # choix du trait (renversement du plateau)
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
        
        self.start_pos = QPushButton("Position de départ")
        self.start_pos.clicked.connect(self.pos_click)
        self.start_pos.id = 0
        self.empty_sym = QPushButton("Effacer les annotations")
        self.empty_sym.clicked.connect(self.pos_click)
        self.empty_sym.id = 2
        self.empty_pos = QPushButton("Vider l'échiquier")
        self.empty_pos.clicked.connect(self.pos_click)
        self.empty_pos.id = 1
        self.save_pos = QPushButton("Sauvegarder la position")
        self.save_pos.clicked.connect(self.pos_click)
        self.save_pos.id = 3
        self.submit = QPushButton("Valider")
        self.submit.id = 'edit'
        self.submit.clicked.connect(self.submit_click)
        self.submit.clicked.connect(self.parent().change_fen)

        # création du label à afficher dans la fenêtre
#       pixmap = QPixmap.fromImage(ImageQt(self.board_img))

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
            self.buttons.append(create_button(k,v))

        # pour récupérer la valeur de la pièce à coller dans l'éditeur
        self.active_piece = '0'
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
        left_layout.addWidget(self.radio_white)
        left_layout.addWidget(self.radio_black)
        bot_layout2.addWidget(self.start_pos)
        bot_layout2.addWidget(self.empty_sym)
        bot_layout2.addWidget(self.empty_pos)
        bot_layout.addWidget(self.save_pos)
        bot_layout.addWidget(self.submit)

        # layout général
        upper_layout = QVBoxLayout()
        layout = QHBoxLayout()

        layout.addLayout(left_layout)
        layout.addLayout(label_layout)
        upper_layout.addLayout(layout)
        self.setLayout(upper_layout)

        self.refresh()

    def set_color(self):
        # retourne le ext_fen pour que le joueur ayant le trait soit en bas
        # il sera remis à l'endroit avant d'être envoyé au formulaire
        self.color = self.sender().id
        if self.color != self.prev_color:
            self.ext_fen = flip_fen(self.ext_fen)
            self.symbol_fen = flip_sym(self.symbol_fen)
            self.printed_arrows = flip_arrows(self.printed_arrows)
            self.refresh()
            self.prev_color = self.color

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
                self.ext_fen = flip_fen(self.ext_fen)
        elif self.sender().id == 2:
            self.symbol_fen = '0000000000000000000000000000000000000000000000000000000000000000'
            self.printed_arrows = []
        elif self.sender().id == 1:
            self.ext_fen = '0000000000000000000000000000000000000000000000000000000000000000'
            self.symbol_fen = '0000000000000000000000000000000000000000000000000000000000000000'
        elif self.sender().id == 3:
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","PNG Files (*.png)")
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
        # récupération de la case 
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
        # crée l'overlay sur lequel vont être imprimées les pièces
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
        temp_board_path = os.path.join(self.current_dir,"temp","temp_board.jpg")
        self.board_img.save(temp_board_path)
        # raffraichit le pixmap à afficher dans le label
        new_pixmap = QPixmap(temp_board_path)
        self.label.setPixmap(new_pixmap)

        self.fen = repack_fen(self.ext_fen)


    def submit_click(self):
        # rétablit le fen dans le bon sens s'il a été retourné dans l'éditeur
        if self.color == 'b':
            self.fen = flip_fen(self.fen)
            self.symbol_fen = flip_sym(self.symbol_fen)
            self.printed_arrows = flip_arrows(self.printed_arrows)
        self.fen += (' ' + self.color)
        self.parent().parent().info["fens"][self.parent().parent().info["active_editor"]]=self.fen
        self.parent().parent().info["symbols"][self.parent().parent().info["active_editor"]]=self.symbol_fen
        self.parent().parent().info["arrows"][self.parent().parent().info["active_editor"]]=self.printed_arrows
        self.close()

class Alert(QDialog):
    def __init__(self, error):
        super().__init__()

        self.setWindowTitle("Erreur")
        alert_msg = QLabel(error)
        self.layout = QHBoxLayout()
        self.layout.addWidget(alert_msg)
        self.setLayout(self.layout)

class FormDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Saisie des codes FEN")

        i = 0
        # listes qui vont recevoir les widgets du formulaire
        self.fen_labels = list()
        self.legend_labels = list()
        self.fens = list()
        self.legends = list()
        self.edits = list()

        # fens récupérés depuis l'éditeur visuel
        self.edited_fens = list()

        while i < self.parent().info["max_diags"]:

            # création des labels
            self.fen_labels.append(QLabel("FEN "+str(i+1)))
            self.legend_labels.append(QLabel("légende "+str(i+1)))

            # création des lignes à éditer
            self.fens.append(QLineEdit(self.parent().info["fens"][i]))
            self.fens[i].setMinimumWidth(450)
            self.fens[i].id = i
            self.fens[i].textChanged.connect(self.change_fen)
            self.legends.append(QLineEdit(self.parent().info["legends"][i]))
            self.legends[i].setMinimumWidth(250)
            self.legends[i].setMaxLength(138)
            self.legends[i].id = i
            self.legends[i].textChanged.connect(self.change_legend)

            # création du bouton d'édition visuelle
            self.edits.append(QPushButton("éditeur graphique"))
            self.edits[i].id = i
            self.edits[i].clicked.connect(self.click_edit)

            i += 1
        i = 0

        self.push_submit = QPushButton("Créer")
        self.push_submit.id = "submit"
        self.push_submit.clicked.connect(self.click)
        self.push_save = QPushButton("Enregistrer")
        self.push_save.id = "save"
        self.push_save.clicked.connect(self.click)
        self.push_cancel = QPushButton("Annuler")
        self.push_cancel.id = "cancel"
        self.push_cancel.clicked.connect(self.click)
        self.push_clear = QPushButton("Effacer")
        self.push_clear.id = "clear"
        self.push_clear.clicked.connect(self.click)

        # définition des layouts
        hbox = list()
        while i < self.parent().info["max_diags"]:
            hbox.append(QHBoxLayout())
            hbox[i].addWidget(self.fen_labels[i])
            hbox[i].addWidget(self.fens[i])
            if self.parent().info["legend_state"]:
                hbox[i].addWidget(self.legend_labels[i])
                hbox[i].addWidget(self.legends[i])
            hbox[i].addWidget(self.edits[i])
            i += 1
        i = 0

        hbox.append(QHBoxLayout())
        hbox[self.parent().info["max_diags"]].addWidget(self.push_submit)
        hbox[self.parent().info["max_diags"]].addWidget(self.push_save)
        hbox[self.parent().info["max_diags"]].addWidget(self.push_cancel)
        hbox[self.parent().info["max_diags"]].addWidget(self.push_clear)

        layout = QVBoxLayout()
        while i < self.parent().info["diag_value"]:
            layout.addLayout(hbox[i])
            i += 1
        i = 0
        layout.addLayout(hbox[self.parent().info["max_diags"]])

        self.setLayout(layout)

    def change_fen(self, text):
        i = 0
        while i < self.parent().info["max_diags"]:
            if self.sender().id == i:
                self.parent().info["fens"][i] = text
                break
            i += 1
        # si le slot est appelé depuis la fenêtre d'édition
        # le fen est renvoyée depuis le dico de la fenêtre principale où il a été modifié par l'éditeur
        if self.sender().id == "edit":
            self.fens[self.parent().info["active_editor"]].setText(self.parent().info["fens"][self.parent().info["active_editor"]])

    def change_legend(self, text):
        i = 0
        while i < self.parent().info["max_diags"]:
            if self.sender().id == i:
                self.parent().info["legends"][i] = text
                break
            i += 1

    def click_edit(self):
        # le numéro du fen à éditer est gardé en mémoire dans le dico principal
        # ouverture de l'éditeur
        self.parent().info["active_editor"] = self.sender().id
        edit = EditDialog(self)
        edit.exec()

    def click(self):
        if self.sender().id == "submit" or self.sender().id == "save":
            # supprime les codes gardés dans le dico principal
            self.parent().info["trimmed_fens"].clear()
            self.parent().info["trimmed_legends"].clear()
            self.parent().info["trimmed_symbols"].clear()

            i = 0
            # remplacement des codes supprimés par ceux envoyés par le formulaire
            # les entrées vides sont ignorées
            while i < self.parent().info["diag_value"]:
                if self.parent().info["fens"][i] != '':
                    self.parent().info["trimmed_fens"].append(self.parent().info["fens"][i])
                    self.parent().info["trimmed_legends"].append(self.parent().info["legends"][i])
                    self.parent().info["trimmed_symbols"].append(self.parent().info["symbols"][i])
                i += 1

            if self.sender().id == "save":
                fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Text Files (*.txt)")
                if not re.search('[.]txt$', fileName):
                    fileName += ".txt"
                with open(fileName, "w") as file:
                    file.write("title_state,")
                    file.write(str(self.parent().info["title_state"]) + "|")
                    file.write("title_text,")
                    file.write(self.parent().info["title_text"] + "|")
                    file.write("num_state,")
                    file.write(str(self.parent().info["num_state"]) + "|")
                    file.write("num_value,")
                    file.write(str(self.parent().info["num_value"]) + "|")
                    file.write("index_state,")
                    file.write(str(self.parent().info["index_state"]) + "|")
                    file.write("index_value,")
                    file.write(str(self.parent().info["index_value"]) + "|")
                    file.write("color_state,")
                    file.write(str(self.parent().info["color_state"]) + "|")
                    file.write("format,")
                    file.write(self.parent().info["format"] + "|")
                    file.write("flip_state,")
                    file.write(str(self.parent().info["flip_state"]) + "|")
                    file.write("legend_state,")
                    file.write(str(self.parent().info["legend_state"]) + "|")
                    file.write("col_value,")
                    file.write(str(self.parent().info["col_value"]) + "|")
                    file.write("diag_value,")
                    file.write(str(self.parent().info["diag_value"]) + "|")
                    file.write("margin_value,")
                    file.write(str(self.parent().info["margin_value"]) + "|")
                    file.write("coord_state,")
                    file.write(str(self.parent().info["coord_state"]) + "|")
                    file.write("down_state,")
                    file.write(str(self.parent().info["down_state"]) + "|")
                    file.write("up_state,")
                    file.write(str(self.parent().info["up_state"]) + "|")
                    file.write("left_state,")
                    file.write(str(self.parent().info["left_state"]) + "|")
                    file.write("right_state,")
                    file.write(str(self.parent().info["right_state"]) + "|")
                    for fen, leg, sym in zip(self.parent().info["trimmed_fens"],self.parent().info["trimmed_legends"],self.parent().info["trimmed_symbols"]):
                        file.write( '\n' + fen + '|' + leg + '|' + sym)
                    for arr in self.parent().info["arrows"]:
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
                            i += 1

            elif self.sender().id == "submit":
                # vérifie que la liste contienne au moins un fen
                i = 0
                for fen in self.parent().info["trimmed_fens"]:
                    i += 1
                    
                if i == 0:
                    alert = Alert("Pas de code saisi")
                    alert.exec()
                else:
                    i = 0
                    error = ''
                    for fen in self.parent().info["trimmed_fens"]:
                        i += 1
                        # teste la correction des codes FEN
                        result = test(fen)
                        # si le retour est de type str, il s'agit d'un message d'erreur
                        if type(result) == str:
                            error += ("FEN " + str(i) +" incorrect\n" + result) 
                            alert = Alert(error)
                            alert.exec()
                            break
                    if result == 1:
                        self.parent().info["page"] = submit(self, self.parent().info)
                        view = ViewDialog(self)
                        view.exec()

        elif self.sender().id == "cancel":
            self.close()
        elif self.sender().id == "clear":
            i = 0
            while i < self.parent().info["max_diags"]:
                self.parent().info["fens"][i] = ''
                self.fens[i].setText(self.parent().info["fens"][i])
                self.parent().info["legends"][i] = ''
                self.legends[i].setText(self.parent().info["legends"][i])
                i += 1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CuteFen")

        i = 0

        # dico principal. données accessibles et modifiables depuis les fenêtres filles
        self.info = {}
        self.info["title_state"] = True 
        self.info["title_text"] = ''
        self.info["num_state"] = True
        self.info["num_value"] = 1
        self.info["index_state"] = True
        self.info["index_value"] = 1
        self.info["color_state"] = True
        self.info["format"] = "portrait"
        self.info["flip_state"] = True
        self.info["legend_state"] = True
        self.info["col_value"] = 1
        self.info["diag_value"] = 1
        self.info["max_cols"] = 5
        self.info["max_diags"] = 15
        self.info["margin_value"] = 20
        self.info["coord_state"] = True
        self.info["down_state"] = True
        self.info["up_state"] = True
        self.info["left_state"] = True
        self.info["right_state"] = True
        self.info["fens"] = list()
        self.info["legends"] = list()
        self.info["symbols"] = list()
        self.info["arrows"] = list()
        self.info["trimmed_fens"] = list()
        self.info["trimmed_legends"] = list()
        self.info["trimmed_symbols"] = list()
        self.info["active_editor"] = int()
        self.info["page"] = None
        self.info["boxes"] = list()

        # valeurs par défaut des listes fens et legends
        while i < self.info["max_diags"]:
            self.info["fens"].append('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w')
            self.info["legends"].append('position de départ')
            self.info["symbols"].append('0000000000000000000000000000000000000000000000000000000000000000')
            self.info["arrows"].append([])
            i += 1
        i = 0

        # délimiteurs
        self.empty_box = QFrame()
        self.empty_box.setFrameShape(QFrame.Shape.Box)
        self.empty_box.setFrameStyle(0)
        self.empty_box.setMaximumWidth(15)

        self.h_line = QFrame()
        self.h_line1 = QFrame()
        self.h_line.setFrameShape(QFrame.Shape.HLine)
        self.h_line1.setFrameShape(QFrame.Shape.HLine)


# Grid 1
        # titre
        self.check_title = QCheckBox()
        self.check_title.setChecked(2)
        self.check_title.setFixedSize(QSize(15, 20))
        self.check_title.id = "title_state"
        self.check_title.clicked.connect(self.change_state)

        self.label_title = QLabel("Afficher un titre")

        self.line_title = QLineEdit('')
        self.line_title.id = "title_text"
        self.line_title.setMinimumWidth(300)
        self.line_title.textChanged.connect(self.change_text)

        # numérotation des pages
        self.check_pn = QCheckBox()
        self.check_pn.setChecked(2)
        self.check_pn.setFixedSize(QSize(15, 20))
        self.check_pn.id = "num_state"
        self.check_pn.clicked.connect(self.change_state)

        self.label_pn = QLabel("Afficher un numéro de page")

        self.spin_pn = QSpinBox()
        self.spin_pn.setValue(1)
        self.spin_pn.setFixedSize(QSize(75, 25))
        self.spin_pn.id = "num_value"
        self.spin_pn.valueChanged.connect(self.change_value)

        # numérotation des diagrammes
        self.check_index = QCheckBox()
        self.check_index.setChecked(2)
        self.check_index.setFixedSize(QSize(15, 20))
        self.check_index.id = "index_state"
        self.check_index.clicked.connect(self.change_state)

        self.label_index = QLabel("Numéroter les diagrammes")
        self.label_index2 = QLabel("Démarrer avec :")

        self.spin_index = QSpinBox()
        self.spin_index.setValue(1)
        self.spin_index.setFixedSize(QSize(75, 25))
        self.spin_index.id = "index_value"
        self.spin_index.valueChanged.connect(self.change_value)

        # orientation de la page
        self.label_format = QLabel("Orientation de la page")

        self.radio_format0 = QRadioButton()
        self.radio_format0.id = "portrait"
        self.radio_format0.setChecked(True)
        self.radio_format0.clicked.connect(self.change_state)

        self.label_format0 = QLabel("Portrait")

        self.radio_format1 = QRadioButton()
        self.radio_format1.id = "paysage"
        self.radio_format1.clicked.connect(self.change_state)

        self.label_format1 = QLabel("Paysage")

        grid1 = QGridLayout()
        grid1.addWidget(self.check_title, 0,0)
        grid1.addWidget(self.label_title, 0,1)
        grid1.addWidget(self.line_title, 1,0,1,3)
        grid1.addWidget(self.check_pn, 2,0)
        grid1.addWidget(self.label_pn, 2,1)
        grid1.addWidget(self.spin_pn, 2,2)
        grid1.addWidget(self.label_format, 3,0,1,2)
        grid1.addWidget(self.radio_format0, 4,0)
        grid1.addWidget(self.label_format0, 4,1)
        grid1.addWidget(self.radio_format1, 5,0)
        grid1.addWidget(self.label_format1, 5,1)
        grid1.addWidget(self.h_line, 6,0,1,3)

        # retournement du plateau en fonction du trait
        self.check_flip = QCheckBox()
        self.check_flip.setChecked(2)
        self.check_flip.setFixedSize(QSize(15, 20))
        self.check_flip.id = "flip_state"
        self.check_flip.clicked.connect(self.change_state)

        self.label_flip = QLabel("Retourner le plateau quand le trait est aux noirs")

        # retournement du plateau en fonction du trait
        self.check_color = QCheckBox()
        self.check_color.setChecked(2)
        self.check_color.setFixedSize(QSize(15, 20))
        self.check_color.id = "color_state"
        self.check_color.clicked.connect(self.change_state)

        self.label_color = QLabel("Indiquer le trait par un pastille noire ou blanche")

        # affichage d'un texte court sous le diagramme
        self.check_legend = QCheckBox()
        self.check_legend.setChecked(2)
        self.check_legend.setFixedSize(QSize(15, 20))
        self.check_legend.id = "legend_state"
        self.check_legend.clicked.connect(self.change_state)

        self.label_legend = QLabel("Afficher du texte sous les diagrammes")

# Grid 3
        # définition du nombre de colonnes
        self.label_col = QLabel("Définir le nombre de colonnes")

        self.spin_col = QSpinBox()
        self.spin_col.setValue(1)
        self.spin_col.setRange(1, self.info["max_cols"])
        self.spin_col.setFixedSize(QSize(75, 25))
        self.spin_col.id = "col_value"
        self.spin_col.valueChanged.connect(self.change_value)

        # définition du nombre de diagrammes
        self.label_diag = QLabel("Définir le nombre de diagrammes")

        self.spin_diag = QSpinBox()
        self.spin_diag.setValue(1)
        self.spin_diag.setRange(1, self.info["max_diags"])
        self.spin_diag.setFixedSize(QSize(75, 25))
        self.spin_diag.id = "diag_value"
        self.spin_diag.valueChanged.connect(self.change_value)

        # dimentionnement des marges
        self.label_margin = QLabel("Largeur des marges (en pixels)")

        self.spin_margin = QSpinBox()
        self.spin_margin.setValue(20)
        self.spin_margin.setRange(0, 200)
        self.spin_margin.setFixedSize(QSize(75, 25))
        self.spin_margin.id = "margin_value"
        self.spin_margin.valueChanged.connect(self.change_value)

        grid3 =QGridLayout()
        grid3.addWidget(self.label_col, 0, 0)
        grid3.addWidget(self.spin_col, 0, 1)
        grid3.addWidget(self.label_diag, 1, 0)
        grid3.addWidget(self.spin_diag, 1, 1)
        grid3.addWidget(self.label_margin, 2, 0)
        grid3.addWidget(self.spin_margin, 2, 1)

# Grid 4
        # affichage des coordonnées
        self.label_coord = QLabel("affichage des coordonnées")

        self.check_coord = QCheckBox()
        self.check_coord.setChecked(2)
        self.check_coord.setFixedSize(QSize(15, 20))
        self.check_coord.id = "coord_state"
        self.check_coord.clicked.connect(self.change_state)

        # côtés où afficher les coordonnées
        self.label_down = QLabel("sous le diagramme")
        self.check_down = QCheckBox()
        self.check_down.setChecked(2)
        self.check_down.setFixedSize(QSize(15, 20))
        self.check_down.id = "down_state"
        self.check_down.clicked.connect(self.change_state)

        self.label_up = QLabel("au dessus du diagramme")
        self.check_up = QCheckBox()
        self.check_up.setChecked(2)
        self.check_up.setFixedSize(QSize(15, 20))
        self.check_up.id = "up_state"
        self.check_up.clicked.connect(self.change_state)

        self.label_left = QLabel("à gauche du diagramme")
        self.check_left = QCheckBox()
        self.check_left.setChecked(2)
        self.check_left.setFixedSize(QSize(15, 20))
        self.check_left.id = "left_state"
        self.check_left.clicked.connect(self.change_state)

        self.label_right = QLabel("à droite du diagramme")
        self.check_right = QCheckBox()
        self.check_right.setChecked(2)
        self.check_right.setFixedSize(QSize(15, 20))
        self.check_right.id = "right_state"
        self.check_right.clicked.connect(self.change_state)

        grid4 = QGridLayout()
        grid4.addWidget(self.check_flip, 0,0)
        grid4.addWidget(self.label_flip, 0,1)
        grid4.addWidget(self.check_color, 1,0)
        grid4.addWidget(self.label_color, 1,1)
        grid4.addWidget(self.h_line1, 2,0,1,3)
        grid4.addWidget(self.check_index, 3,0)
        grid4.addWidget(self.label_index, 3,1)
        grid4.addWidget(self.label_index2, 4,1)
        grid4.addWidget(self.spin_index, 4,2)
        grid4.addWidget(self.check_legend, 5,0)
        grid4.addWidget(self.label_legend, 5,1)
        grid4.addWidget(self.check_coord, 7, 0)
        grid4.addWidget(self.label_coord, 7, 1)

        grid5 = QGridLayout()
        grid5.addWidget(self.check_down, 0, 1)
        grid5.addWidget(self.label_down, 0, 2)
        grid5.addWidget(self.check_up, 1, 1)
        grid5.addWidget(self.label_up, 1, 2)
        grid5.addWidget(self.check_left, 2, 1)
        grid5.addWidget(self.label_left, 2, 2)
        grid5.addWidget(self.check_right, 3, 1)
        grid5.addWidget(self.label_right, 3, 2)
        grid5.addWidget(self.empty_box, 0, 0)
        grid5.addWidget(self.empty_box, 1, 0)
        grid5.addWidget(self.empty_box, 2, 0)
        grid5.addWidget(self.empty_box, 3, 0)

# QHBoxLayouts
        #  ouverture du formulaire
        self.push_form = QPushButton("Continuer")
        self.push_form.id = "form_push"
        self.push_form.clicked.connect(self.click_form)

        #  chargement d'un formulaire
        self.push_load = QPushButton("Charger")
        self.push_load.id = "load_push"
        self.push_load.clicked.connect(self.click_load)

        # quitter
        self.push_exit = QPushButton("Quitter")
        self.push_exit.id = "exit_push"
        self.push_exit.clicked.connect(self.click_exit)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.push_form)
        hbox1.addWidget(self.push_load)
        hbox1.addWidget(self.push_exit)

# Global layout
        layout = QVBoxLayout()
        layout.addLayout(grid1)
        layout.addLayout(grid3)
        layout.addLayout(grid4)
        layout.addLayout(grid5)
        layout.addLayout(hbox1)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # SLOTS

    def change_state(self, state):
        if self.sender().id == "title_state":
            self.info["title_state"] = state
            if not state:
                self.line_title.setEnabled(False)
            else:
                self.line_title.setEnabled(True)

        elif self.sender().id == "num_state":
            self.info["num_state"] = state
            if not state:
                self.spin_pn.setEnabled(False)
            else:
                self.spin_pn.setEnabled(True)

        elif self.sender().id == "index_state":
            self.info["index_state"] = state
            if not state:
                self.spin_index.setEnabled(False)
            else:
                self.spin_index.setEnabled(True)

        elif self.sender().id == "portrait":
            self.info["format"] = "portrait"

        elif self.sender().id == "paysage":
            self.info["format"] = "paysage"

        elif self.sender().id == "flip_state":
            self.info["flip_state"] = state

        elif self.sender().id == "color_state":
            self.info["color_state"] = state

        elif self.sender().id == "legend_state":
            self.info["legend_state"] = state

        elif self.sender().id == "coord_state":
            self.info["coord_state"] = state
            if not state:
                self.check_down.setEnabled(False)
                self.check_up.setEnabled(False)
                self.check_left.setEnabled(False)
                self.check_right.setEnabled(False)
            else:
                self.check_down.setEnabled(True)
                self.check_up.setEnabled(True)
                self.check_left.setEnabled(True)
                self.check_right.setEnabled(True)

        elif self.sender().id == "down_state":
            self.info["down_state"] = state
        elif self.sender().id == "up_state":
            self.info["up_state"] = state
        elif self.sender().id == "left_state":
            self.info["left_state"] = state
        elif self.sender().id == "right_state":
            self.info["right_state"] = state

    def change_text(self, text):
        if self.sender().id == "title_text":
            self.info["title_text"] = text

    def change_value(self, value):
        if self.sender().id == "num_value":
            self.info["num_value"] = value

        if self.sender().id == "index_value":
            self.info["index_value"] = value

        if self.sender().id == "col_value":
            self.info["col_value"] = value

        if self.sender().id == "diag_value":
            self.info["diag_value"] = value

        if self.sender().id == "margin_value":
            self.info["margin_value"] = value

    def click_exit(self):
        self.close()

    def click_form(self):
        form = FormDialog(self)
        form.exec()

    def click_load(self):
        lines_value = 0
        fileName, _ = QFileDialog.getOpenFileName(self, "Selectionner le fichier","","Text Files (*.txt)")

        if fileName != '':
            with open(fileName, 'r') as file:
                lines = file.read().split('\n')
                for l in lines:
                    lines_value += 1
                lines_value -= 1

                fields = lines[0].split('|')
                for field in fields:
                    f = field.split(',')
                    if re.search('state', f[0]):
                       if f[1] == 'True':
                            self.info[f[0]] = True
                       else: 
                            self.info[f[0]] = False
                    elif re.search('value', f[0]):
                        self.info[f[0]] = int(f[1])
                    elif re.search('text', f[0]):
                        self.info[f[0]] = str(f[1])
                    elif re.search('format', f[0]):
                        self.info[f[0]] = str(f[1])

                
                i = 1
                while i <= lines_value:
                    line = lines[i].split('|')
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

                self.actualize()
                self.click_form()


    def actualize(self):
        self.check_title.setChecked(self.info["title_state"])
        self.line_title.setText(self.info["title_text"])
        self.check_pn.setChecked(self.info["num_state"])
        self.spin_pn.setValue(self.info["num_value"])
        self.check_color.setChecked(self.info["color_state"])
        if self.info["format"] == "portrait":
            self.radio_format0.setChecked(True)
        else:
            self.radio_format1.setChecked(True)
        self.check_flip.setChecked(self.info["flip_state"])
        self.check_legend.setChecked(self.info["legend_state"])
        self.spin_col.setValue(self.info["col_value"])
        self.spin_diag.setValue(self.info["diag_value"])
        self.spin_margin.setValue(self.info["margin_value"])
        self.check_coord.setChecked(self.info["coord_state"])
        self.check_down.setChecked(self.info["down_state"])
        self.check_up.setChecked(self.info["up_state"])
        self.check_left.setChecked(self.info["left_state"])
        self.check_right.setChecked(self.info["right_state"])


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
