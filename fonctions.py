import sys
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt6.QtWidgets import QDialog, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QSize

def getSquare(pos):
    squarePos = list()
    if int(pos.x() / 75) == 0:
        squarePos.append('a')
    elif int(pos.x() / 75) == 1:
        squarePos.append('b')
    elif int(pos.x() / 75) == 2:
        squarePos.append('c')
    elif int(pos.x() / 75) == 3:
        squarePos.append('d')
    elif int(pos.x() / 75) == 4:
        squarePos.append('e')
    elif int(pos.x() / 75) == 5:
        squarePos.append('f')
    elif int(pos.x() / 75) == 6:
        squarePos.append('g')
    elif int(pos.x() / 75) == 7:
        squarePos.append('h')
        
        
    if int(pos.y() / 75) == 0:
        squarePos.append('8')
    elif int(pos.y() / 75) == 1:
        squarePos.append('7')
    elif int(pos.y() / 75) == 2:
        squarePos.append('6')
    elif int(pos.y() / 75) == 3:
        squarePos.append('5')
    elif int(pos.y() / 75) == 4:
        squarePos.append('4')
    elif int(pos.y() / 75) == 5:
        squarePos.append('3')
    elif int(pos.y() / 75) == 6:
        squarePos.append('2')
    elif int(pos.y() / 75) == 7:
        squarePos.append('1')

    return(squarePos)

def getCenter(pos):
    i = 0
    squareCenter = list()
    while i < 8:
        if int(pos.x() / 75) == i:
            squareCenter.append(int(pos.x() / 75) * 75 + 37)
        i += 1
        
    i = 0
    while i < 8:
        if int(pos.y() / 75) == i:
            squareCenter.append(int(pos.y() / 75) * 75 + 37)
        i += 1
    return(squareCenter)

def submit(self, info):
    ext_fens = list()
    syms = list()
    boards = list()
    boxes = list()
    colors = list()
    arrows = list()

# formats the fens (flips if needed)
    flip = info["flip_state"]
    for fen, sym, arr  in zip(info["trimmed_fens"], info["trimmed_symbols"], info["arrows"]):
        colors.append(color_test(fen))
        ext_fens.append(unpack_fen(fen, flip))
        if color_test(fen) == 'b' and flip:
            syms.append(flip_sym(sym))
            arrows.append(flip_arrows(arr))
        else:
            syms.append(sym)
            arrows.append(arr)



# draws the boards
    for fen, sym, arr in zip(ext_fens, syms, arrows):
        boards.append(draw_board(fen, sym, arr))


    i_state = info["index_state"]
    index = info["index_value"]
    c_state = info["color_state"]
    l_state = info["legend_state"]
    legends = info["trimmed_legends"]
    coord = info["coord_state"]
    down = info["down_state"]
    up = info["up_state"]
    left = info["left_state"]
    right = info["right_state"]
    margin = info["margin_value"]
    
# draws the boxes (board + decorations)
    i = 0
    for board in boards:
        boxes.append(draw_box(board, i_state, index, l_state, legends[i], coord, down, up, left, right, c_state, colors[i], flip, margin))
        index += 1
        i +=1
    i = 0
    self.parent().info["boxes"] = boxes 

    orient = info["format"]
    t_state = info["title_state"]
    title = info["title_text"]
    n_state = info["num_state"]
    num = info["num_value"]
    col = info["col_value"]
    margin = info["margin_value"]

# draws the page
    page = draw_page(orient, t_state, title, n_state, num, col, margin, boxes)
    return(page)

def color_test(fen):
    blocks = fen.split()
    try:
        if blocks[1] == 'b':
            return('b')
        else:
            return('w')
    except:
        return('w')

def test(fen):
    blocks = fen.split()
    r = 0
    v = 0
    error = ''
    pieces = 'rnbqkpRNBQKP'

    rows = blocks[0].split('/')
    for row in rows:
        if r > 7:
            error += ('nombre de rangées trop élevé.')
            return(error)
        for s in row:
            try:
                v += int(s)
            except:
                if s in pieces:
                    v += 1
                else:
                    error += ('dans la rangée n°' + str(r+1) + ', ')
                    error += ('caractère inconnu.')
                    return(error)

        #checks if there is 8 squares in the row
        if v < 8:
            error += ('dans la rangée n°' + str(r+1) + ', ')
            error += ('nombre de cases insuffisant.')
            return(error)
        elif v > 8:
            error += ('dans la rangée n°' + str(r+1) + ', ')
            error += ('nombre de cases trop important.')
            return(error)
        else:
            r += 1
            v = 0

    if r < 8:
        error += ('nombre de rangées insuffisant')
        return(error)
    elif r == 8:
        return(1)

def unpack_fen(fen, flip):
    fen = fen.split()
    ext_fen = ''

    for char in fen[0]:
        try:
            char = int(char)
            while char != 0:
                ext_fen += '0'
                char -= 1
        except:
            if char != "/":
                ext_fen += char

    try:
        if fen[1] == 'b' and flip:
            rev_fen = ''
            i = 63
            while i >= 0:
                rev_fen += ext_fen[i]
                i -= 1
            ext_fen = rev_fen
            return(ext_fen)
        else:
            return(ext_fen)
        
    except:
        return(ext_fen)

def flip_fen(fen):
    rev_fen = ''
    i = 0
    for char in fen:
        i += 1
    i -= 1
    while i >= 0:
        rev_fen += fen[i]
        i -= 1
    return(rev_fen)

def flip_sym(sym):
    rev_sym = ''
    i = 0
    for char in sym:
        i += 1
    i -= 1
    while i >= 0:
        if sym[i] == 'A':
            rev_sym += 'C'
        elif sym[i] == 'Z':
            rev_sym += 'X'
        elif sym[i] == 'E':
            rev_sym += 'W'
        elif sym[i] == 'D':
            rev_sym += 'S'
        elif sym[i] == 'C':
            rev_sym += 'A'
        elif sym[i] == 'X':
            rev_sym += 'Z'
        elif sym[i] == 'W':
            rev_sym += 'E'
        elif sym[i] == 'S':
            rev_sym += 'D'
        elif sym[i] == 'a':
            rev_sym += 'c'
        elif sym[i] == 'z':
            rev_sym += 'x'
        elif sym[i] == 'e':
            rev_sym += 'w'
        elif sym[i] == 'd':
            rev_sym += 's'
        elif sym[i] == 'c':
            rev_sym += 'a'
        elif sym[i] == 'x':
            rev_sym += 'z'
        elif sym[i] == 'w':
            rev_sym += 'e'
        elif sym[i] == 's':
            rev_sym += 'd'
        else:
            rev_sym += sym[i]
        i -= 1
    return(rev_sym)

def flip_arrows(printed_arrows):
    rev_arrow = list()
    for arrow in printed_arrows:
        a = arrow[0][7]
        if a == "1":
            flip_a = "9"
        elif a == "2":
            flip_a = "8"
        elif a == "3":
            flip_a = "7"
        elif a == "4":
            flip_a = "6"
        elif a == "6":
            flip_a = "4"
        elif a == "7":
            flip_a = "3"
        elif a == "8":
            flip_a = "2"
        elif a == "9":
            flip_a = "1"
        # récupération du nouveau nom de la flèche
        new_arrow = arrow[0][:7] + flip_a + arrow[0][8:]

        # identification de la case qui servira d'origine après retournement
        new_o = list()
        new_x = int(arrow[1])/75 + int(arrow[0][8])
        new_y = int(arrow[2])/75 + int(arrow[0][9])

        new_o.append(new_x)
        new_o.append(new_y)

        # récupération des coordonnées de la nouvelle origine
        flip_o = list()

        for n in new_o:
            if n == 1:
                flip_n = 7
            elif n == 2:
                flip_n = 6
            elif n == 3:
                flip_n = 5
            elif n == 4:
                flip_n = 4
            elif n == 5:
                flip_n = 3
            elif n == 6:
                flip_n = 2
            elif n == 7:
                flip_n = 1
            elif n == 8:
                flip_n = 0
            flip_o.append(flip_n*75)
        
        # affectation des nouvelles valeurs
        rev_arrow.append([new_arrow, flip_o[0], flip_o[1]])

    return(rev_arrow)

def repack_fen(ext_fen):
    fen = ''
    i = 0
    count = 0
    for char in ext_fen:
        if i == 8:
            fen += '/'
            i = 0
        if char == '0':
            count +=1
            i += 1
            if i == 8:
                if count != 0:
                    fen += str(count)
                    count = 0
        else:
            if count != 0:
                fen += str(count)
                count = 0
                fen += char
                i += 1
            else:
                fen += char
                i += 1
    return(fen)

def draw_board(fen, sym, arr):
    board_side = 8*177
    board = Image.new('RGB', (board_side, board_side), 'white')
    i = 0
    j = 0
    for piece,s in zip(fen,sym):
        board.paste(draw_square(i,j,piece,s), (j*177, i*177))
        j += 1
        if j == 8:
            j = 0
            i += 1
    i = 0
    j = 0
    for a in arr:
        arr_x = int(a[1]/75)*177
        arr_y = int(a[2]/75)*177
        arr_img = Image.open(a[0]).resize((int(a[0][8])*177,int(a[0][9])*177))
        board.paste(arr_img,(arr_x,arr_y),arr_img)
    return(board)

def draw_square(i, j, p, s):
    if (i+j)%2 == 0:
        square_img = Image.new('RGB', (177, 177), 'white')
    else:
        square_img = Image.open('board/ds.jpg')
        if square_img.size != (177,177):
            square_img = square_img.resize((177,177))

    if p != '0':
        if p == 'p':
            piece_img = Image.open("pieces/bP.png")
        elif p == 'r':  
            piece_img = Image.open("pieces/bR.png")
        elif p == 'n':  
            piece_img = Image.open("pieces/bN.png")
        elif p == 'b':  
            piece_img = Image.open("pieces/bB.png")
        elif p == 'k':  
            piece_img = Image.open("pieces/bK.png")
        elif p == 'q':  
            piece_img = Image.open("pieces/bQ.png")
        elif p == 'P':
            piece_img = Image.open("pieces/wP.png")
        elif p == 'R':  
            piece_img = Image.open("pieces/wR.png")
        elif p == 'N':  
            piece_img = Image.open("pieces/wN.png")
        elif p == 'B':  
            piece_img = Image.open("pieces/wB.png")
        elif p == 'K':  
            piece_img = Image.open("pieces/wK.png")
        elif p == 'Q':  
            piece_img = Image.open("pieces/wQ.png")
        # 177 * 177 is the size of the default pieces pgn delivewhite with the program
        if piece_img.size != (177,177):
            piece_img = piece_img.resize((177,177))
        square_img.paste(piece_img, (0,0), piece_img)


    if s != '0':
        if s == 'z':
            sym_img = Image.open("symbols/bz.png")
        elif s == 'e':
            sym_img = Image.open("symbols/be.png")
        elif s == 'd':
            sym_img = Image.open("symbols/bd.png")
        elif s == 'c':
            sym_img = Image.open("symbols/bc.png")
        elif s == 'x':
            sym_img = Image.open("symbols/bx.png")
        elif s == 'w':
            sym_img = Image.open("symbols/bw.png")
        elif s == 's':
            sym_img = Image.open("symbols/bs.png")
        elif s == 'a':
            sym_img = Image.open("symbols/ba.png")
        elif s == 'Z':
            sym_img = Image.open("symbols/wz.png")
        elif s == 'E':
            sym_img = Image.open("symbols/we.png")
        elif s == 'D':
            sym_img = Image.open("symbols/wd.png")
        elif s == 'C':
            sym_img = Image.open("symbols/wc.png")
        elif s == 'X':
            sym_img = Image.open("symbols/wx.png")
        elif s == 'W':
            sym_img = Image.open("symbols/ww.png")
        elif s == 'S':
            sym_img = Image.open("symbols/ws.png")
        elif s == 'A':
            sym_img = Image.open("symbols/wa.png")
        elif s == 't':
            sym_img = Image.open("symbols/bt.png")
        elif s == 'o':
            sym_img = Image.open("symbols/bo.png")
        elif s == 'g':
            sym_img = Image.open("symbols/bg.png")
        elif s == 'y':
            sym_img = Image.open("symbols/by.png")
        elif s == 'T':
            sym_img = Image.open("symbols/wt.png")
        elif s == 'O':
            sym_img = Image.open("symbols/wo.png")
        elif s == 'G':
            sym_img = Image.open("symbols/wg.png")
        elif s == 'Y':
            sym_img = Image.open("symbols/wy.png")
        if sym_img.size != (177,177):
            sym_img = sym_img.resize((177,177))
        square_img.paste(sym_img, (0,0), sym_img)
    return(square_img)

def draw_box(board, i_state, index, l_state, legend, coord, down, up, left, right, c_state, color, flip, margin):
    box_w = board.width
    box_h = board.height
    index_w = 177
    legend_h = 2*177
    coord_l = 177
    coord_L = 8*177

    board_x = 0
    board_y = 0
    index_y = 0
    legend_y = board.height

    if i_state or c_state:
        box_w += index_w
        # déplacement des points de collage
        board_x += index_w

        index_img = draw_index(i_state, index, c_state, color, index_w, board.height)
    if coord:
        if up:
            box_h += coord_l
            # déplacement des points de collage
            board_y += coord_l
            index_y += coord_l
            legend_y += coord_l

            coordh = draw_coord_h(coord_L, coord_l, flip, color)
        if down:
            box_h += coord_l
            # déplacement des points de collage
            legend_y += coord_l
            coordh = draw_coord_h(coord_L, coord_l, flip, color)
        if left:
            box_w += coord_l
            # déplacement des points de collage
            board_x += coord_l

            coordv = draw_coord_v(coord_l, coord_L, flip, color)
        if right:
            box_w += coord_l
            coordv = draw_coord_v(coord_l, coord_L, flip, color)
    if l_state:
        box_h += legend_h
        legend_img = draw_legend(legend, box_w, legend_h, margin)

    box = Image.new('RGB', (box_w, box_h), 'white')
    draw = ImageDraw.Draw(box)


    # définition des coordonnées de collage
    box.paste(board,(board_x, board_y))
    if i_state or c_state:
        box.paste(index_img, (0, index_y))
    if coord:
        if up:
            box.paste(coordh,(board_x, 0))
        if down:
            box.paste(coordh,(board_x, board_y + board.height))
        if left:
            box.paste(coordv,(board_x - coord_l, board_y))
        if right:
            box.paste(coordv,(board_x + board.width, board_y))
    if l_state:
        box.paste(legend_img,(0, legend_y))
    return(box)
    
def draw_index(i_state, index, c_state, color, w, h):
    fontsize = 130
    index = str(index)
    font = ImageFont.truetype("fonts/FreeSerif.ttf", size = fontsize)

    img = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(img)
    if i_state:
        img_size = font.getsize(index)
        draw.text(((w-img_size[0])/2, (w-img_size[1])/2), index, font = font, fill = 'black')
    if c_state:
        if color == 'b':
            color_img = Image.open("symbols/bDot.png")
        else:
            color_img = Image.open("symbols/wDot.png")
        color_img = color_img.resize((120,120))
        color_img_size = color_img.size
        img.paste(color_img,(int((w-color_img_size[0])/2), int((w-color_img_size[1])/2)+w), color_img)
    return(img)

def draw_legend(legend, w, h, margin):
    fontsize = 113
    font = ImageFont.truetype("fonts/FreeSerif.ttf", size = fontsize)

    img = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(img)
    img_size = font.getsize(legend)
    if img_size[0] > w:
        words = legend.split()
        i = 0
        j = 0
        new_size = [0,0]
        f_line_size = [0,0]
        s_line_size = [0,0]
        t_line_size = [0,0]
        string = ''
        first_line = ''

        for word in words:
            i += 1
        while j < i and new_size[0] < w:
            first_line = string
            f_line_size = new_size
            string += words[j] + ' '
            new_size = font.getsize(string)
            j += 1
        string = words[j - 1] + ' '
        new_size = [0,0]
        while j < i and new_size[0] < w:
            second_line = string + ' '
            s_line_size = new_size
            string += words[j] + ' '
            new_size = font.getsize(string)
            j += 1
        third_line = words[j - 1] + ' '
        while j < i:
            third_line += words[j] + ' '
            t_line_size = font.getsize(third_line)
            j += 1

        draw.text(((w-f_line_size[0])/2, (0)), first_line, font = font, fill = 'black')
        draw.text(((w-s_line_size[0])/2, s_line_size[1]+ 2), second_line, font = font, fill = 'black')
        draw.text(((w-t_line_size[0])/2, t_line_size[1] * 2 + 4), third_line, font = font, fill = 'black')
    else:
        draw.text(((w-img_size[0])/2, (h-img_size[1])/2), legend, font = font, fill = 'black')
    return(img)

def draw_coord_h(w, h, flip, color):
    fontsize = 100
    font = ImageFont.truetype("fonts/FreeSerif.ttf", size = fontsize)
    coords = 'abcdefgh'

    if flip and color == 'b':
        i = 7
        rev_coords = coords
        coords = ''
        while i >= 0:
            coords += rev_coords[i]
            i -= 1

    img = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(img)
    i = 0

    while i < 8:
        img_size = font.getsize(coords[i])
        draw.text((((177-img_size[0])/2)+i*177, (177-img_size[1])/2), coords[i], font = font, fill = 'black')
        i += 1
    return(img)

def draw_coord_v(w, h, flip, color):
    fontsize = 100
    font = ImageFont.truetype("fonts/FreeSerif.ttf", size = fontsize)
    coords = '87654321'

    if flip and color == 'b':
        i = 7
        rev_coords = coords
        coords = ''
        while i >= 0:
            coords += rev_coords[i]
            i -= 1

    img = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(img)
    i = 0

    while i < 8:
        img_size = font.getsize(coords[i])
        draw.text((((177-img_size[0])/2), ((177-img_size[1])/2)+i*177), coords[i], font = font, fill = 'black')
        i += 1
    return(img)

def draw_page(orient, t_state, title, n_state, num, col, margin, boxes):
    i = 0
    j = 0
    m_w = margin
    m_h = margin
    box_w = boxes[0].width
    box_h = boxes[0].height
    margin_top = 0
    margin_bot = 0
    num = str(num)
    fontsize = 200
    num_font = ImageFont.truetype("fonts/FreeSerif.ttf", size = 80)
    title_font = ImageFont.truetype("fonts/FreeSerif.ttf", size = fontsize)

    # définition du format de la page
    if orient == "portrait":
        page_w = 2480
        page_h = 3508
    elif orient == "paysage":
        page_w = 3508
        page_h = 2480

    title_w = page_w
    title_h = 300

    num_w = page_w
    num_h = 100

    if t_state:
        margin_top = 300
    if n_state:
        margin_bot = 150

    usefull_h = page_h - margin_top - margin_bot

    # définition du nombre de diagrammes à coller et du nombre de diagrammes par colonne
    diag_n = 0
    for box in boxes:
        diag_n += 1

    diags_x_col = diag_n / col
    if diag_n % col != 0:
        diags_x_col = int(diags_x_col) + 1

    # création de la page
    page = Image.new('RGB', (page_w, page_h), 'white')

    if t_state:
        title_box = Image.new('RGB', (title_w, title_h), 'white')
        draw = ImageDraw.Draw(title_box)
        img_size = title_font.getsize(title)
        draw.text(((title_w - img_size[0])/2,(title_h - img_size[1])/2),title,font=title_font,fill='black')
        page.paste(title_box, (0,0) )

    if n_state:
        num_box = Image.new('RGB', (num_w, num_h), 'white')
        draw = ImageDraw.Draw(num_box)
        size = num_font.getsize(num)
        draw.text(((num_w-size[0])/2,0),num,font=num_font,fill='black')
        page.paste(num_box, (0, page_h - num_h))

    # dimentionnement des boîtes
    if usefull_h / (diags_x_col * box_h) >= page_w / (col * box_w):
        # BUG
        new_box_w = int((page_w - m_w * (col + 1)) / col)
        ratio = new_box_w / box_w
        box_w = new_box_w
        box_h = int(box_h * ratio)
        m_h = int((usefull_h - box_h * diags_x_col) / (diags_x_col + 1))
    else:
        new_box_h = int((usefull_h - m_h * (diags_x_col + 1)) / diags_x_col)
        ratio = new_box_h / box_h
        box_h = new_box_h
        box_w = int(box_w * ratio)
        m_w = int((page_w - box_w * col) / (col + 1))


    resized_boxes = list()

    for box in boxes:
        resized_boxes.append(box.resize((box_w, box_h)))

    for box in resized_boxes:
        x = m_w * (i + 1) + box_w * i
        y = m_h * (j + 1) + box_h * j + margin_top
        page.paste(box, (x, y))
        i += 1

        if i == col:
            i = 0
            j += 1

    return(page)
