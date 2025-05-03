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

@app.route("/on_square_click", methods=["POST"])
def on_square_click():
    session=get_session()
    data = request.get_json()
    gamedata = session.query(ChessGameData).get(data["chessgamedata_id"])
    chessboard = session.query(ChessBoard).get(data["chessboard_id"])
    game_=ChessGame(None,session,gamedata,chessboard)
    game_.on_square_click(data["row"],data["column"])
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "current_move":game_.chessboard_.current_move,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})

@app.route("/restartgame", methods=["POST"])
def restartgame():
    sess=get_session()
    game_=ChessGame(session=sess)
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})

@app.route("/nextgame", methods=["POST"])
def nextgame():
    sess=get_session()
    data = request.get_json()
    gamedata = sess.query(ChessGameData).get(data["chessgamedata_id"])
    chessboard = sess.query(ChessBoard).get(data["chessboard_id"])
    game_=ChessGame(None,sess,gamedata,chessboard)
    game_.nextgame()
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})

@app.route("/lastgame", methods=["POST"])
def lastgame():
    sess=get_session()
    data = request.get_json()
    gamedata = sess.query(ChessGameData).get(data["chessgamedata_id"])
    chessboard = sess.query(ChessBoard).get(data["chessboard_id"])
    game_=ChessGame(None,sess,gamedata,chessboard)
    game_.lastgame()
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})


@app.route("/nextmove", methods=["POST"])
def nextmove():
    sess=get_session()
    data = request.get_json()
    gamedata = sess.query(ChessGameData).get(data["chessgamedata_id"])
    chessboard = sess.query(ChessBoard).get(data["chessboard_id"])
    game_=ChessGame(None,sess,gamedata,chessboard)
    game_.nextmove()
    replayboard=game_.session.execute(
                                        select(ChessBoard)
                                        .where(ChessBoard.gamedata_id == game_.chessboard_.gamedata_id,
                                            ChessBoard.is_replay==True)
                                        .order_by(ChessBoard.id.desc())
                                        .limit(1)
                                    ).scalar_one_or_none()
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})


@app.route("/lastmove", methods=["POST"])
def lastmove():
    sess=get_session()
    data = request.get_json()
    gamedata = sess.query(ChessGameData).get(data["chessgamedata_id"])
    chessboard = sess.query(ChessBoard).get(data["chessboard_id"])
    game_=ChessGame(None,sess,gamedata,chessboard)
    game_.lastmove()
    replayboard=game_.session.execute(
                                        select(ChessBoard)
                                        .where(ChessBoard.gamedata_id == game_.chessboard_.gamedata_id,
                                            ChessBoard.is_replay==True)
                                        .order_by(ChessBoard.id.desc())
                                        .limit(1)
                                    ).scalar_one_or_none()
    return jsonify({"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":game_.chessboard_.board,
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id})