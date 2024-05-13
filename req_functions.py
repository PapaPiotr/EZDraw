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
