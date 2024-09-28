#possible moves:
#e4
#Nc3
#Nbd7
#Nxc3
#N1xc3
#exc8=Q

def drawBoard(position):
    board = []
    row = ''
    for p in position:
        if p != '/':
            try:
                p = int(p)
                while p > 0:
                    row += '|   '
                    p -= 1

            except:
                row += '| ' + p + ' '
        else:
            row += '|'
            board.append(row)
            row = ""

    row += '|'
    board.append(row)
    return(board)

#remplissage de la matrice avec la position
def getBoard(position):
    board = list()
    
    i = 0
    while i < 64:
        board.append('')
        i += 1
        
    i = 0
    for p in position:
        if p != '/':
            try:
                p = int(p)
                while p > 0:
                    board[i] = '0'
                    p -= 1
                    i += 1
            except:
                board[i] = p
                i += 1
    return(board)

#reconstitution d'un segment de FEN
def getPosition(board):
    position = ''
    i = 0
    n = 0
    for p in board:
        if i == 8:
            position += '/'
            i = 0
        if p == '0':
            n += 1
            i += 1
            if i == 8:
                position += str(n)
                n = 0
        else:
            if n != 0:
                position += str(n)
                n = 0
            position += p
            i += 1
    return(position)

#reconstitution d'un FEN complet
def getFen(infos):
    fen = infos['position'] + ' '    
    fen += infos['opponent'] + ' '
    fen += infos['castle'] + ' '
    fen += infos['enPassant'] + ' '
    fen += infos['fifty'] + ' '
    fen += infos['number'] + ' '
    return(fen)

#conversion entre un nom de case et sa position dans la matrice (ex: a8 -> 0, h1 -> 63)
def squareToNum(square):
    alphabet = 'abcdefgh'
    if not square[0] in alphabet or not square[1] in '12345678':
        return(-1)
    else:
        column = 0
        for letter in alphabet:
            if square[0] != letter:
                column += 1
            else:
                break

        row = 8
        n = 0
        while row >= 0:
            if int(square[1]) != row:
                row -= 1
                n += 1
            else:
                break
        num = n * 8 + column
        return(num)

#conversion entre une position dans la matrice et un nom de case (ex: 0 -> a8, 63 -> h1)
def numToSquare(num):
    alphabet = 'abcdefgh'
    numbers = '87654321'
    if num < 0 or num > 63:
        return(-1)
    else:
        column = num % 8
        row = int(num / 8)

        column = alphabet[column]
        row = numbers[row]
        return(column + row)

#renvoie la pièce qui occupe la case
def getPiece(board, square):
    num = squareToNum(square)
    return(board[num])

#renvoie la case d'arrivée
def moveUp(oldSquare):
    if oldSquare == -1:
        return(-1)
    numSquare = squareToNum(oldSquare)
    if numSquare > 7:
        numSquare -= 8
    else:
        return(-1)
    newSquare = numToSquare(numSquare)
    return(newSquare)

def moveDown(oldSquare):
    if oldSquare == -1:
        return(-1)
    numSquare = squareToNum(oldSquare)
    if numSquare < 56:
        numSquare += 8
    else:
        return(-1)
    newSquare = numToSquare(numSquare)
    return(newSquare)

def moveRight(oldSquare):
    if oldSquare == -1:
        return(-1)
    numSquare = squareToNum(oldSquare)
    if numSquare % 8 < 7:
        numSquare += 1
    else:
        return(-1)
    newSquare = numToSquare(numSquare)
    return(newSquare)

def moveLeft(oldSquare):
    if oldSquare == -1:
        return(-1)
    numSquare = squareToNum(oldSquare)
    if numSquare % 8 > 0:
        numSquare -= 1
    else:
        return(-1)
    newSquare = numToSquare(numSquare)
    return(newSquare)

def isSquareFree(board, square):
    if square != -1 and getPiece(board, square) == '0':
        return(True)
    else:
        return(False)

def isPieceAttacked(board, square, piece):
    if square != -1:
        if piece.isupper() and getPiece(board, square).islower():
            return(True)
        elif piece.islower() and getPiece(board, square).isupper():
            return(True)
    else:
        return(False)

def isPawnOnStartingRank(piece, num):
    if (piece.isupper() and 48 <= num <= 55) or (piece.islower() and 8 <= num <= 15):
        return(True)
    else:
        return(False)

#lister les cases couvertes (player détermine la couleur des pièces dont on veut lister les coups possibles. Par défaut, les déplacements de toutes les pièces sont renvoyés)
def getSeenSquares(board, player = 'n'):
    seenSquaresList = list()
    num = 0
    j = 0
    for piece in board:
        j += 1
        square = numToSquare(num)

        if piece in 'rqkRQK':
            nextSquare = moveDown(square)
            while nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
                if piece in 'Kk' or not isSquareFree(board, nextSquare):
                    break
                nextSquare = moveDown(nextSquare)

            nextSquare = moveUp(square)
            while nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
                if piece in 'Kk' or not isSquareFree(board, nextSquare):
                    break
                nextSquare = moveUp(nextSquare)

            nextSquare = moveLeft(square)
            while nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
                if piece in 'Kk' or not isSquareFree(board, nextSquare):
                    break
                nextSquare = moveLeft(nextSquare)

            nextSquare = moveRight(square)
            while nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
                if piece in 'Kk' or not isSquareFree(board, nextSquare):
                    break
                nextSquare = moveRight(nextSquare)

        if piece in 'bqkBQK':
            nextSquare = moveDown(moveRight(square))
            while nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
                if piece in 'Kk' or not isSquareFree(board, nextSquare):
                    break
                nextSquare = moveDown(moveRight(nextSquare))

            nextSquare = moveDown(moveLeft(square))
            while nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
                if piece in 'Kk' or not isSquareFree(board, nextSquare):
                    break
                nextSquare = moveDown(moveLeft(nextSquare))
            
            nextSquare = moveUp(moveRight(square))
            while nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
                if piece in 'Kk' or not isSquareFree(board, nextSquare):
                    break
                nextSquare = moveUp(moveRight(nextSquare))

            nextSquare = moveUp(moveLeft(square))
            while nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
                if piece in 'Kk' or not isSquareFree(board, nextSquare):
                    break
                nextSquare = moveUp(moveLeft(nextSquare))

        if piece in 'Nn':
            nextSquare = moveUp(moveUp(moveRight(square)))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])

            nextSquare = moveUp(moveUp(moveLeft(square)))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])

            nextSquare = moveDown(moveDown(moveRight(square)))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])

            nextSquare = moveDown(moveDown(moveLeft(square)))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])

            nextSquare = moveRight(moveRight(moveUp(square)))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])

            nextSquare = moveRight(moveRight(moveDown(square)))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])

            nextSquare = moveLeft(moveLeft(moveUp(square)))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])

            nextSquare = moveLeft(moveLeft(moveDown(square)))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])

        if piece == 'p':
            nextSquare = moveDown(moveRight(square))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
            nextSquare = moveDown(moveLeft(square))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
            nextSquare = moveDown(square)

        if piece == 'P':
            nextSquare = moveUp(moveRight(square))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
            nextSquare = moveUp(moveLeft(square))
            if nextSquare != -1:
                seenSquaresList.append([square, piece, nextSquare, getPiece(board, nextSquare)])
        num += 1
            
    if player == 'n':
        return(seenSquaresList)
    elif player == 'w':
        whiteMoves = list()
        for move in seenSquaresList:
            if move[1].isupper():
                whiteMoves.append(move)
        return(whiteMoves)

    elif player == 'b':
        blackMoves = list()
        for move in seenSquaresList:
            if move[1].islower():
                blackMoves.append(move)
        return(blackMoves)

#lister les pièces clouées
def getPinnedPieces(board):
    num = 0
    pins = list()
    middlePieces = list()
    for piece in board:
        square = numToSquare(num)
        i = 0
        # si je tombe sur le roi | après avoir traversé une seule pièce | de la couleur opposée
        # j'ajoute la pièce à la liste des pièces clouée
        # pins[0] = attacking square
        # pins[1] = attacking piece
        # pins[2] = pinned square
        # pins[3] = pinned piece
        # pins[4] = king's square
        # pins[5] = king 

        if piece in 'rqb':
            if piece in 'rq':
                nextSquare = moveDown(square)
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'K'and i == 1 and middlePieces[0][1] in 'RNBQP':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'K'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveDown(nextSquare)
                i = 0
                middlePieces.clear()

                nextSquare = moveUp(square)
                # teste la case de dessus
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'K'and i == 1 and middlePieces[0][1] in 'RNBQP':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'K'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveUp(nextSquare)
                i = 0
                middlePieces.clear()

                nextSquare = moveRight(square)
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'K'and i == 1 and middlePieces[0][1] in 'RNBQP':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'K'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveRight(nextSquare)
                i = 0
                middlePieces.clear()

                nextSquare = moveLeft(square)
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'K'and i == 1 and middlePieces[0][1] in 'RNBQP':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'K'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveLeft(nextSquare)
                i = 0
                middlePieces.clear()
            if piece in 'bq':
                nextSquare = moveRight(moveDown(square))
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'K'and i == 1 and middlePieces[0][1] in 'RNBQP':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'K'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveRight(moveDown(nextSquare))
                i = 0
                middlePieces.clear()

                nextSquare = moveRight(moveUp(square))
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'K'and i == 1 and middlePieces[0][1] in 'RNBQP':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'K'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveRight(moveUp(nextSquare))
                i = 0
                middlePieces.clear()

                nextSquare = moveLeft(moveDown(square))
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'K'and i == 1 and middlePieces[0][1] in 'RNBQP':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'K'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveLeft(moveDown(nextSquare))
                i = 0
                middlePieces.clear()

                nextSquare = moveLeft(moveUp(square))
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'K'and i == 1 and middlePieces[0][1] in 'RNBQP':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'K'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveLeft(moveUp(nextSquare))
                i = 0
                middlePieces.clear()

        elif piece in 'RQB':
            if piece in 'RQ':
                nextSquare = moveDown(square)
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'k'and i == 1 and middlePieces[0][1] in 'rnbqp':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'k'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveDown(nextSquare)
                i = 0
                middlePieces.clear()

                nextSquare = moveUp(square)
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'k'and i == 1 and middlePieces[0][1] in 'rnbqp':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'k'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveUp(nextSquare)
                i = 0
                middlePieces.clear()

                nextSquare = moveRight(square)
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'k'and i == 1 and middlePieces[0][1] in 'rnbqp':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'k'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveRight(nextSquare)
                i = 0
                middlePieces.clear()

                nextSquare = moveLeft(square)
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'k'and i == 1 and middlePieces[0][1] in 'rnbqp':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'k'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveLeft(nextSquare)
                i = 0
                middlePieces.clear()
            if piece in 'BQ':
                nextSquare = moveRight(moveDown(square))
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'k'and i == 1 and middlePieces[0][1] in 'rnbqp':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'k'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveRight(moveDown(nextSquare))
                i = 0
                middlePieces.clear()

                nextSquare = moveRight(moveUp(square))
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'k'and i == 1 and middlePieces[0][1] in 'rnbqp':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'k'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveRight(moveUp(nextSquare))
                i = 0
                middlePieces.clear()

                nextSquare = moveLeft(moveDown(square))
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'k'and i == 1 and middlePieces[0][1] in 'rnbqp':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'k'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveLeft(moveDown(nextSquare))
                i = 0
                middlePieces.clear()

                nextSquare = moveLeft(moveUp(square))
                # teste la case de dessous
                while  nextSquare != -1:
                    if getPiece(board, nextSquare) == 'k'and i == 1 and middlePieces[0][1] in 'rnbqp':
                        pins.append([square, piece, middlePieces[0][0], middlePieces[0][1], nextSquare, 'k'])
                        break
                    # je compte le nombre de pièces traversées
                    elif getPiece(board, nextSquare) != '0':
                        middlePieces.append([nextSquare, getPiece(board, nextSquare)])
                        i += 1
                    # je passe à la case suivante
                    nextSquare = moveLeft(moveUp(nextSquare))
                i = 0
                middlePieces.clear()

        num += 1
    return(pins)

def isSameColumn(start, end):
    if start%8 == end%8:
        return(True)
    else:
        return(False)

def isSameRow(start, end):
    if int(start/8) == int(end/8):
        return(True)
    else:
        return(False)

def isSameDiagonal(start, end):
    if (end-start)%9 == 0:
#   if start%8 < end%8 and start/8 < end/8:
        return(3)
    elif (start-end)%9 == 0:
#   elif start%8 > end%8 and start/8 > end/8:
        return(7)
    elif (start-end)%7 == 0:
#   elif start%8 < end%8 and start/8 > end/8:
        return(9)
    elif (end-start)%7 == 0:
#   elif start%8 > end%8 and start/8 < end/8:
        return(1)
    else:
        return(False)

#lister les case qui relient l'attaquant, la pièce clouée et le roi
def getPinMiddleSquares(pins):
    i = 0
    piecesRange = list()
    for pin in pins:

        piecesRange.append([pin[2],pin[3],[]])
        start = squareToNum(pin[0])
        end = squareToNum(pin[4])
        
        if isSameColumn(start, end):
            while start < end:
                piecesRange[i][2].append(numToSquare(start))
                start += 8
            while start > end:
                piecesRange[i][2].append(numToSquare(start))
                start -= 8

        elif isSameRow(start, end):
            while start < end:
                piecesRange[i][2].append(numToSquare(start))
                start += 1
            while start > end:
                piecesRange[i][2].append(numToSquare(start))
                start -= 1
        else:
            if isSameDiagonal(start, end) == 3:
                while start < end:
                    piecesRange[i][2].append(numToSquare(start))
                    start += 9
            if isSameDiagonal(start, end) == 7:
                while start > end:
                    piecesRange[i][2].append(numToSquare(start))
                    start -= 9
            if isSameDiagonal(start, end) == 9:
                while start > end:
                    piecesRange[i][2].append(numToSquare(start))
                    start -= 7
            elif isSameDiagonal(start, end) == 1:
                while start < end:
                    piecesRange[i][2].append(numToSquare(start))
                    start += 7
        i += 1
    return(piecesRange)

#renvoie la liste des cases qui séparent le roi de la pièce qui le met en échec
def getCheckMiddleSquares(check):
    checkMiddleSquares = list()
    start = squareToNum(check[0])
    end = squareToNum(check[2])

    if isSameColumn(start, end):
        if start < end:
            nextSquare = moveDown(check[0])
            while nextSquare != check[2]:
                if nextSquare == -1:
                    break
                checkMiddleSquares.append(nextSquare)
                nextSquare = moveDown(nextSquare)
        if start > end:
            nextSquare = moveUp(check[0])
            while nextSquare != check[2]:
                if nextSquare == -1:
                    break
                checkMiddleSquares.append(nextSquare)
                nextSquare = moveUp(nextSquare)

    elif isSameRow(start, end):
        if start < end:
            nextSquare = moveRight(check[0])
            while nextSquare != check[2]:
                if nextSquare == -1:
                    break
                checkMiddleSquares.append(nextSquare)
                nextSquare = moveRight(nextSquare)
        if start > end:
            nextSquare = moveLeft(check[0])
            while nextSquare != check[2]:
                if nextSquare == -1:
                    break
                checkMiddleSquares.append(nextSquare)
                nextSquare = moveLeft(nextSquare)

    elif isSameDiagonal(start, end) == 1:
        nextSquare = moveLeft(moveDown(check[0]))
        while nextSquare != check[2]:
            if nextSquare == -1:
                break
            checkMiddleSquares.append(nextSquare)
            nextSquare = moveLeft(moveDown(nextSquare))

    elif isSameDiagonal(start, end) == 3:
        nextSquare = moveRight(moveDown(check[0]))
        while nextSquare != check[2]:
            if nextSquare == -1:
                break
            checkMiddleSquares.append(nextSquare)
            nextSquare = moveRight(moveDown(nextSquare))

    elif isSameDiagonal(start, end) == 7:
        nextSquare = moveLeft(moveUp(check[0]))
        while nextSquare != check[2]:
            if nextSquare == -1:
                break
            checkMiddleSquares.append(nextSquare)
            nextSquare = moveLeft(moveUp(nextSquare))

    elif isSameDiagonal(start, end) == 9:
        nextSquare = moveRight(moveUp(check[0]))
        while nextSquare != check[2]:
            if nextSquare == -1:
                break
            checkMiddleSquares.append(nextSquare)
            nextSquare = moveRight(moveUp(nextSquare))

    return(checkMiddleSquares)

#renvoie la liste des déplacements possibles à partir des cases couvertes (ne tient pas compte des clouages / échecs / roque)
def seenSquaresToBasicMoves(board, player, enPassant):
    seenSquares = getSeenSquares(board, player)
    correctedPawnsMoves = list()
    num = 0

    #ajoute les captures de pion
    for square in seenSquares:
        if (player == 'w' and square[1] == 'P' ) or (player == 'b' and square[1] == 'p' ):
            if isPieceAttacked(board, square[2], square[1]) or square[2] == enPassant:
                correctedPawnsMoves.append(square)
        elif (player == 'w' and square[3].isupper()) or (player == 'b' and square[3].islower()):
            pass
        else:
            correctedPawnsMoves.append(square)

    for piece in board:
        if player == 'w' and piece == 'P':
            square = numToSquare(num)
            nextSquare = moveUp(square)
            if isSquareFree(board, nextSquare):
                correctedPawnsMoves.append([square, piece, nextSquare, '0'])
                if isPawnOnStartingRank(piece, num):
                    secondSquare = moveUp(nextSquare)
                    if isSquareFree(board, secondSquare):
                        correctedPawnsMoves.append([square, piece, secondSquare, '0'])
        num += 1
    num = 0
    for piece in board:
        if player == 'b' and piece == 'p':
            square = numToSquare(num)
            nextSquare = moveDown(square)
            if isSquareFree(board, nextSquare):
                correctedPawnsMoves.append([square, piece, nextSquare, '0'])
                if isPawnOnStartingRank(piece, num):
                    secondSquare = moveDown(nextSquare)
                    if isSquareFree(board, secondSquare):
                        correctedPawnsMoves.append([square, piece, secondSquare, '0'])
        num += 1

    return(correctedPawnsMoves)

#limite les cases de déplacement des pièces clouées
def restrictMovesPins(moves, mids):
    movesMinusPins = list()
    moveOk = True
    for move in moves:
        moveOk = True
        for mid in mids:
            # si le coup déplace une pièce clouée
            if move[0] == mid[0] and move[1] == mid[1]:
                moveOk = False
                for s in mid[2]:
                    if move[2] == s:
                        movesMinusPins.append(move)
        if moveOk:
            movesMinusPins.append(move)

    return(movesMinusPins)

#retire les cases de déplacement du roi qui sont couvertes par les pièces adverses
def restrictMovesKing(playersMoves, opponentsMoves):
    restrictedKing = list()
    freeSquare = True 

    for playersMove in playersMoves:
        freeSquare = True
        if playersMove[1] in 'kK':
            for opMove in opponentsMoves:
                if playersMove[2] == opMove[2]:
                    #la case move[2] est couverte par une pièce adverse
                    freeSquare = False
                    break
            if freeSquare:
                restrictedKing.append(playersMove)
        else:
            restrictedKing.append(playersMove)

    return(restrictedKing)

#ajoute la possibilité de roquer
def isCastlingOk(board, restrictedMovesKing, castle, player, opponent):
    whiteKingside = True
    whiteQueenside = True
    blackKingside = True
    blackQueenside = True

    attackedSquares = getSeenSquares(board, opponent)

    for attSquare in attackedSquares:
        if player == 'w':
            if attSquare[2] == 'e1' or attSquare[2] == 'f1' or attSquare[2] == 'g1':
                whiteKingside = False
            if attSquare[2] == 'e1' or attSquare[2] == 'd1' or attSquare[2] == 'c1':
                whiteQueenside = False
                break
        elif player == 'b':
            if attSquare[2] == 'e8' or attSquare[2] == 'f8' or attSquare[2] == 'g8':
                blackKingside = False
            if attSquare[2] == 'e8' or attSquare[2] == 'd8' or attSquare[2] == 'c8':
                blackQueenside = False
                break

    if player == 'w':
        if 'K' in castle and board[62] == '0' and board[61] == '0' and whiteKingside:
            restrictedMovesKing.append(['e1', 'K', 'g1', '0'])
        if 'Q' in castle and board[59] == '0' and board[58] == '0' and whiteQueenside:
            restrictedMovesKing.append(['e1', 'K', 'c1', '0'])
    elif player == 'b':
        if 'k' in castle and board[5] == '0' and board[6] == '0' and blackKingside:
            restrictedMovesKing.append(['e8', 'k', 'g8', '0'])
        if 'q' in castle and board[2] == '0' and board[3] == '0' and blackQueenside:
            restrictedMovesKing.append(['e8', 'k', 'c8', '0'])
    return(restrictedMovesKing)

#lister les échecs
def getChecks(moves):
    checks = list()
    for m in moves:
        if (m[3] == 'k' and m[1].isupper()) or (m[3] == 'K' and m[1].islower()):
            checks.append(m)
    return(checks)

#renvoie la liste des coups possibles en cas d'échec
def restrictMovesCheck(moves, checks):
    defenseMoves = list()

    for m in moves:
        if len(checks) >= 1:
            if m[1] in 'kK':
                defenseMoves.append(m)
        if len(checks) == 1:
            if m[2] == checks[0][0] and m[1] not in 'kK':
                defenseMoves.append(m)
    if len(checks) == 1 and checks[0][1] not in 'nN':
        midCheck = getCheckMiddleSquares(checks[0])
        for m in moves:
            if m[2] in midCheck:
                defenseMoves.append(m)

    return(defenseMoves)

def isSamePiece(move, p):
    if move == p[1] or move.lower() == p[1]:
        return(True)
    else:
        return(False)

def assessPosition(fen):
    infos = {}
    infos['position'] = fen.split()[0]
    infos['player'] = fen.split()[1]
    if infos['player'] == 'w':
        #print('white to play')
        infos['opponent'] = 'b'
    elif infos['player'] == 'b':
        #print('black to play')
        infos['opponent'] = 'w'
    else:
        infos['opponent'] = 'n'
    infos['castle'] = fen.split()[2]
    infos['enPassant'] = fen.split()[3]
    infos['fifty'] = fen.split()[4]
    infos['number'] = fen.split()[5]

    infos['board'] = getBoard(infos['position'])
    infos['pins'] = getPinnedPieces(infos['board'])
    infos['mids'] = getPinMiddleSquares(infos['pins'])
    infos['seenSquares'] = getSeenSquares(infos['board'], infos['player'])
    infos['basicMoves'] = seenSquaresToBasicMoves(infos['board'], infos['player'], infos['enPassant'])
    infos['restrictedMovesPins'] = restrictMovesPins(infos['basicMoves'], infos['mids'])
    infos['restrictedMovesKing'] = restrictMovesKing(infos['restrictedMovesPins'], getSeenSquares(infos['board'], infos['opponent']))
    infos['legalMoves'] = isCastlingOk(infos['board'], infos['restrictedMovesKing'], infos['castle'], infos['player'], infos['opponent'])
    infos['checks'] = getChecks(getSeenSquares(infos['board'], infos['opponent']))
    if infos['fifty'] == 50:
        #nulle par 50 coups
        #print('draw by 50 moves rule')
        exit()

    elif infos['checks']:
        infos['defenseMoves'] = restrictMovesCheck(infos['legalMoves'], infos['checks'])
        if not infos['defenseMoves']:
            #mat
            #print('checkmate')
            exit()
    else:
        if not infos['legalMoves']:
            #pat
            exit()

    return(infos)

#renvoie le tableau correspondant au coup à jouer
def getMove(legalMoves, move):
    moveList = list()
    whiteShort = ['e1', 'K', 'g1', '0']
    blackShort = ['e8', 'k', 'g8', '0']
    whiteLong = ['e1', 'K', 'c1', '0']
    blackLong = ['e8', 'k', 'c8', '0']
    matches = 0
    
    #e4
    if len(move) == 2:
        for p in legalMoves:
            pawn = p[1] in 'pP'
            landing_square = move == p[2]

            if pawn and landing_square:
                matches +=1
                p.append('0')
                moveList.append(p)

    elif len(move) == 3:
        if move == 'O-O':
            for p in legalMoves:
                short_castle = p in [whiteShort, blackShort]
                if short_castle:
                    matches += 1
                    p.append('0')
                    moveList.append(p)
        #Nf3
        else:
            for p in legalMoves:
                piece_name = isSamePiece(move[0], p)
                landing_square = move[1:3] == p[2]

                if piece_name and landing_square:
                    matches += 1
                    p.append('0')
                    moveList.append(p)

    elif len(move) == 4:
        promotion = move[2] == '='
        new_piece = move[3] in 'RNBQ'
        capture = move[1] == 'x'

        for p in legalMoves:
            piece_name = isSamePiece(move[0], p) and move[0].isupper()
            pawn = p[1] in "pP" and move[0].islower()
            column = move[0] in p[0]
            added_info = move[1] in p[0]
            landing_square_beg = move[0:2] == p[2]
            landing_square_end = move[2:4] == p[2]

            exd4 = pawn and column and capture and landing_square_end
            e8_Q = landing_square_beg and promotion and new_piece
            nbd7 = piece_name and added_info and landing_square_end
            nxc6 = piece_name and capture and landing_square_end

            if exd4 or nbd7 or nxc6:
                matches += 1
                p.append('0')
                moveList.append(p)
            elif e8_Q:
                matches += 1
                p.append(move[3])
                moveList.append(p)

    elif len(move) == 5:
        if move == 'O-O-O':
            for p in legalMoves:
                long_castle = p in [whiteLong, blackLong]

                if long_castle:
                    matches += 1
                    p.append('0')
                    moveList.append(p)
        else:
            #Nbxc6
            for p in legalMoves:
                piece_name = isSamePiece(move[0], p)
                added_info = move[1] in p[0]
                capture = move[2] == 'x' and p[3] != '0'
                landing_square = move[3:5] == p[2]

                nbxc6 = piece_name and added_info and capture and landing_square

                if nbxc6:
                    matches += 1
                    p.append('0')
                    moveList.append(p)

    elif len(move) == 6:
        #exd8=Q
        capture = move[1] == 'x'
        promotion = move[4] == '='
        new_piece = move[5] in 'RNBQ'
        for p in legalMoves:
            pawn = p[1] in 'pP'
            column = move[0] in p[0]
            landing_square = move[2:4] == p[2]

            exd8_Q = pawn and column and capture and landing_square and promotion and new_piece

            if exd8_Q:
                matches += 1
                p.append(move[5])
                moveList.append(p)



    if matches == 1:
        #print("coup joué :", move)
        return(moveList[0])
    elif matches == 0:
        #print("coup illégal")
        return(0)
    elif matches > 1:
        #print("information insuffisante")
        return(0)

def updateInfos(infos,playedMove):
    newCastle = ''
    # vide la case de la pièce jouée
    infos['board'][squareToNum(playedMove[0])] = '0'

    # déplacement sans promotion
    if playedMove[4] == '0':
        # la pièce déplacée vient occuper la case d'arrivée
        infos['board'][squareToNum(playedMove[2])] = playedMove[1]

        # en cas de roque, la tour correspondante est déplacée
        if playedMove == ['e1','K','g1','0','0']:
            infos["board"][squareToNum('h1')] = '0'
            infos["board"][squareToNum('f1')] = 'R'
        elif playedMove == ['e1','K','c1','0','0']:
            infos["board"][squareToNum('a1')] = '0'
            infos["board"][squareToNum('d1')] = 'R'
        elif playedMove == ['e8','k','g8','0','0']:
            infos["board"][squareToNum('h8')] = '0'
            infos["board"][squareToNum('f8')] = 'r'
        elif playedMove == ['e8','k','c8','0','0']:
            infos["board"][squareToNum('a8')] = '0'
            infos["board"][squareToNum('d8')] = 'r'

        # en cas de prise en pasant, la case du pion est libérée
        if playedMove[2] == infos["enPassant"]:
            if infos["enPassant"][1] == "3":
                pawnSquare = infos["enPassant"][0] + "4"
            elif infos["enPassant"][1] == "6":
                pawnSquare = infos["enPassant"][0] + "5"
            infos["board"][squareToNum(pawnSquare)] = "0"



    # promotion
    else:
        infos['board'][squareToNum(playedMove[2])] = playedMove[4]
    infos['position'] = getPosition(infos['board'])

    if playedMove[1] == 'K':
        for c in infos['castle']:
            if c.islower():
                newCastle += c
        infos['castle'] = newCastle
    elif playedMove[1] == 'k':
        for c in infos['castle']:
            if c.isupper():
                newCastle += c
        infos['castle'] = newCastle
    elif playedMove[0] == 'a1':
        for c in infos['castle']:
            if c != 'Q':
                newCastle += c
        infos['castle'] = newCastle
    elif playedMove[0] == 'h1':
        for c in infos['castle']:
            if c != 'K':
                newCastle += c
        infos['castle'] = newCastle
    elif playedMove[0] == 'a8':
        for c in infos['castle']:
            if c != 'q':
                newCastle += c
        infos['castle'] = newCastle
    elif playedMove[0] == 'h8':
        for c in infos['castle']:
            if c != 'k':
                newCastle += c
        infos['castle'] = newCastle
    else:
        newCastle = infos['castle']

    if newCastle == '':
        infos['castle'] = '-'

    if playedMove[0][1] == '2' and playedMove[1] == 'P' and playedMove[2][1] == '4':
        infos['enPassant'] = playedMove[0][0] + '3'
    elif playedMove[0][1] == '7' and playedMove[1] == 'p' and playedMove[2][1] == '5':
        infos['enPassant'] = playedMove[0][0] + '6'
    else:
        infos['enPassant'] = '-'

    if playedMove[1] in 'pP' or playedMove[3] != '0':
        infos['fifty'] = '0'
    else:
        infos['fifty'] = str(int(infos['fifty']) + 1 )

    if infos['player'] == 'b':
        infos['number'] = str(int(infos['number']) + 1)

    return(infos)

def getPgn(infos,move, pgn):
    if infos['player'] == 'w':
        pgn[len(pgn)-1][0] = infos['number']
        pgn[len(pgn)-1][1] = move
    if infos['player'] == 'b':
        pgn[len(pgn)-1][2] = move
        pgn.append(['','',''])

    return(pgn)
