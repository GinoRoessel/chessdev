from flask import Flask, request, jsonify
from flask import make_response
from flask_cors import CORS
from chesspieces import *
from chessrules import *
from chessmove import *
from chessgui import *
from chessboard import *
from chessgame import *
from database.base import Base, create_tables,delete_tables, get_session


def serialize_board(board):
    result = []
    for row in board:
        serialized_row = []
        for piece in row:
            if piece is None:
                serialized_row.append(None)
            else:
                serialized_row.append((piece.guisymbol,piece.color))  
        result.append(serialized_row)
    return result


app = Flask(__name__)

CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

@app.route("/test")
def test():
    return {"msg": "CORS sollte funktionieren"}

@app.route("/game/move", methods=["POST"])
def move():
    try:
        sess=get_session()
        data = request.get_json()
        gamedata = sess.query(ChessGameData).get(data["chessgamedata_id"])
        chessboard = sess.query(ChessBoard).get(data["chessboard_id"])
        nextmove = data["nextmove"]
        lastmove = data["lastmove"]
        game_=ChessGame(None,sess,gamedata,chessboard)
        if nextmove:
            game_.nextmove()
            made=False
        elif lastmove:
            game_.lastmove()
            made=False
        else:
            made=True if game_.on_square_click(data["endrow"],data["endcol"],data["startrow"],data["startcol"]) else False
  
    
        response={"current_player":game_.chessgamedata.current_player,
                        "status":game_.chessgamedata.status,
                        "board":serialize_board(game_.chessboard_.board),
                        "chessgamedata_id":game_.chessgamedata.id,
                        "chessboard_id":game_.chessboard_.id,
                        }
        return jsonify(response)
    except Exception as e:
        print("Fehler in /game",e)
        response = make_response(jsonify({"error": str(e)}), 500)
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response
    finally:
        sess.close()
    return jsonify(response)


@app.route("/game", methods=["POST"])
def game():
    print("xyz")
    try:
        sess=get_session()
        game_=ChessGame(session=sess)
        response={"current_player":game_.chessgamedata.current_player,
                    "status":game_.chessgamedata.status,
                    "board":serialize_board(game_.chessboard_.board),
                    "chessgamedata_id":game_.chessgamedata.id,
                    "chessboard_id":game_.chessboard_.id}
        print("game route success")
        return jsonify(response)
    except Exception as e:
        print("Fehler in /game",e)
        response = make_response(jsonify({"error": str(e)}), 500)
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response
    finally:
        sess.close()
    return jsonify(response) 


@app.route("/game", methods=["GET"])
def games():
    try:
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

        response= {"current_player":game_.chessgamedata.current_player,
                        "status":game_.chessgamedata.status,
                        "board":game_.chessboard_.board,
                        "chessgamedata_id":game_.chessgamedata.id,
                        "chessboard_id":game_.chessboard_.id}
    finally:
        sess.close()
    response.headers.add("Access-Control-Allow-Origin", "*")
    return jsonify(response)

@app.route("/game/board", methods=["POST"])
def board():
    try:
        sess=get_session()
        data = request.get_json()
        gamedata = sess.query(ChessGameData).get(data["chessgamedata_id"])
        chessboard = sess.query(ChessBoard).get(data["chessboard_id"])
        replay=data["replay"]
        game_=ChessGame(None,sess,gamedata,chessboard)
        if replay:
            game_.replay_game_mode()
        
        response= {"current_player":game_.chessgamedata.current_player,
                        "status":game_.chessgamedata.status,
                        "board":game_.chessboard_.board,
                        "chessgamedata_id":game_.chessgamedata.id,
                        "chessboard_id":game_.chessboard_.id}
    finally:
        sess.close()
    return jsonify(response)
    

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)

