# from flask import Flask, request, jsonify
# from chesspieces import *
# from chessrules import *
# from chessmove import *
# from chessgui import *
# from chessboard import *
# from chessgame import *
# from database.base import Base, create_tables,delete_tables, get_session

# from main import game


app = Flask(__name__)

@app.route("/on_square_click", methods=["POST"])
def on_square_click():
    session=get_session()
    data = request.get_json()
    game = session.query(ChessGame).get(data[])
    game.on_square_click(data)
    return jsonify({"current_player":game.chessgamedata.current_player,
                    "status":game.chessgamedata.status,
                    "current_move":game.chessgamedata.current_move})

@app.route("/restartgame", methods=["POST"])
def restartgame():
    game.restartgame()
    return jsonify({"current_player":game.chessgamedata.current_player,
                    "status":game.chessgamedata.status,
                    "board":game.chessboard_.board})

@app.route("/nextgame", methods=["POST"])
def nextgame():
    game.nextgame()
    return jsonify({"current_player":game.chessgamedata.current_player,
                    "status":game.chessgamedata.status,
                    "board":game.chessboard_.board})

@app.route("/lastgame", methods=["POST"])
def lastgame():
    game.lastgame()
    return jsonify({"current_player":game.chessgamedata.current_player,
                    "status":game.chessgamedata.status,
                    "board":game.chessboard_.board})

@app.route("/nextmove", methods=["POST"])
def nextmove():
    game.nextmove()
    return jsonify({"current_player":game.chessgamedata.current_player,
                    "status":game.chessgamedata.status,
                    "current_move":game.chessgamedata.current_move})

@app.route("/lastmove", methods=["POST"])
def lastmove():
    game.lastmove()
    return jsonify({"current_player":game.chessgamedata.current_player,
                    "status":game.chessgamedata.status,
                    "current_move":game.chessgamedata.current_move})