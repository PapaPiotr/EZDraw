from play_functions import assessPosition, drawBoard, getMove, getFen, updateInfos
import requests
import re

def get_moves_from_id(id):
    true_id = ""
    for char in id:
        if char != "#":
            true_id += char
    url = "https://lichess.org/training/" + true_id

    try:
        response = requests.get(url)
        if response.status_code == 200:
            source = response.text
        else:
            print("Échec de la récupération de la page")
            return(0)
    except requests.RequestException as e:
            print("Error:", e)
            return(0)

    move = ""
    moves = list()
    pgn =  re.findall('pgn":".*?"', source)
    fields = pgn[0].split('"')
    moves_plus = fields[2].split()
    for m in moves_plus:
        for char in m:
            if char != "+":
                move += char
        moves.append(move)
        move = ""
    moves.append("exit")
    return(moves)

def getFenFromId(id):
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    moves = get_moves_from_id(id)
    for move in moves:
        positionStatus = assessPosition(fen)
        playedMove = getMove(positionStatus['legalMoves'], move)
        if playedMove != 0:
            infos = updateInfos(positionStatus, playedMove)
            fen = getFen(infos)
    return(fen)

def openPgnFile(fileName):
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    pgn_data = {}
    pgn_data["headers"]= list()
    pgn_data["piecesMoves"]= list()
    pgn_data["moves"]= list()
    pgn_data["fens"]= list()
    pgn_data["symbols"]= list()
    pgn_data["arrows"]= list()
    parentesis = 0
    with open(fileName, "r") as file:
        plainText = file.read()

        pgn_data["headers"] = re.findall('\[\w.*\]', plainText)
        purgedText = ""
        write = True
        for c in plainText:
            if c in "({[":
                parentesis += 1
            elif c in ")]}":
                parentesis -= 1
            if parentesis == 0:
                write = True
            else:
                write = False
            if write and c not in "()[]{}":
                purgedText += c

        moves = re.findall('[a-hRNBQKO][a-hx1-8RNBQKO\-\+\=\#]{1,6}', purgedText)
        if len(moves) % 2 != 0:
            moves.append("")

        for move in moves:
            piece = ""
            char = ""
            for l in move:
                if l in "abcdefghO123456789x-=":
                    piece += l
                    char += l
                elif l in "+#":
                    piece += l
                elif l == "K":
                    piece += "♔"
                    char += l
                elif l == "Q":
                    piece += "♕"
                    char += l
                elif l == "B":
                    piece += "♗"
                    char += l
                elif l == "N":
                    piece += "♘"
                    char += l
                elif l == "R":
                    piece += "♖"
                    char += l
            pgn_data["piecesMoves"].append(piece)
            pgn_data["moves"].append(char)

        for move in pgn_data["moves"]:
            positionStatus = assessPosition(fen)
            playedMove = getMove(positionStatus['legalMoves'], move)
            if playedMove != 0:
                infos = updateInfos(positionStatus, playedMove)
                fen = getFen(infos)
                pgn_data["fens"].append(fen)
                pgn_data["symbols"].append('0000000000000000000000000000000000000000000000000000000000000000')
                pgn_data["arrows"].append([])
    return(pgn_data)
