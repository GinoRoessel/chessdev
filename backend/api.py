from flask import Flask, request, jsonify
from chesspieces import *
from chessrules import *
from chessmove import *
from chessgui import *
from chessboard import *
from chessgame import *
from database.base import Base, create_tables,delete_tables, get_session

from main import game_


app = Flask(__name__)

@app.route("/game/move", methods=["POST"])
def move():
    session=get_session()
    data = request.get_json()
    gamedata = session.query(ChessGameData).get(data["chessgamedata_id"])
    chessboard = session.query(ChessBoard).get(data["chessboard_id"])
    nextmove = data["nextmove"]
    lastmove = data["lastmove"]
    game_=ChessGame(None,session,gamedata,chessboard)
    if nextmove:
        game_.nextmove()
        made=False
    elif lastmove:
        game_.lastmove()
        made=False
    else:
        made=True if game_.on_square_click(data["row"],data["column"]) else False
  
    
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "current_move":game_.chessboard_.current_move,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id,
                    "completed":made})

@app.route("/game", methods=["POST"])
def game():
    sess=get_session()
    game_=ChessGame(session=sess)
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})

@app.route("/game", methods=["GET"])
def games():
    sess=get_session()
    gamedata_id = request.args.get('gamedata_id', type=int)
    board_id = request.args.get('board_id', type=int)
    before_id = request.args.get('before_id', type=int)
    after_id = request.args.get('after_id', type=int)
    if before_id:
        gamedata = sess.query(ChessGameData).get(before_id)
        chessboard = sess.query(ChessBoard).get(board_id)
        game_=ChessGame(None,sess,gamedata,chessboard)
        game_.lastgame()
    elif after_id:
        gamedata = sess.query(ChessGameData).get(after_id)
        chessboard = sess.query(ChessBoard).get(board_id)
        game_=ChessGame(None,sess,gamedata,chessboard)
        game_.nextgame()
    else:
        gamedata = sess.query(ChessGameData).get(gamedata_id)
        chessboard = sess.query(ChessBoard).get(board_id)
        game_=ChessGame(None,sess,gamedata,chessboard)

    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})

@app.route("/game/board", methods=["POST"])
def board():
    session=get_session()
    data = request.get_json()
    gamedata = session.query(ChessGameData).get(data["chessgamedata_id"])
    chessboard = session.query(ChessBoard).get(data["chessboard_id"])
    replay=data["replay"]
    game_=ChessGame(None,session,gamedata,chessboard)
    if replay:
        game_.replay_game_mode()
    
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})

