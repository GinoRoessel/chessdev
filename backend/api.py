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
            board_=game_.nextmove()
            made=False
            response={"current_player":game_.chessgamedata.current_player,
                        "status":game_.chessgamedata.status,
                        "board":serialize_board(board_),
                        "chessgamedata_id":game_.chessgamedata.id,
                        "chessboard_id":game_.chessboard_.id}
        elif lastmove:
            print("lllllastmove")
            board_=game_.lastmove()
            made=False
            response={"current_player":game_.chessgamedata.current_player,
                        "status":game_.chessgamedata.status,
                        "board":serialize_board(board_),
                        "chessgamedata_id":game_.chessgamedata.id,
                        "chessboard_id":game_.chessboard_.id}
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


@app.route("/game/get", methods=["GET"])
def game_get():
    print("QQQ")
    try:
        sess=get_session()
        gamedata_id = request.args.get('gamedata_id', type=int)
        board_id = request.args.get('board_id', type=int)
        before_str = request.args.get('before', default='false')
        before = before_str.lower() == 'true'
        after_str = request.args.get('after', default='false')
        after = after_str.lower() == 'true'
        if before:
            gamedata = sess.query(ChessGameData).get(gamedata_id)
            chessboard = sess.query(ChessBoard).get(board_id)
            game_=ChessGame(None,sess,gamedata,chessboard)
            game_.lastgame()
        elif after:
            gamedata = sess.query(ChessGameData).get(gamedata_id)
            chessboard = sess.query(ChessBoard).get(board_id)
            game_=ChessGame(None,sess,gamedata,chessboard)
            game_.nextgame()
        else:
            gamedata = sess.query(ChessGameData).get(gamedata_id)
            chessboard = sess.query(ChessBoard).get(board_id)
            game_=ChessGame(None,sess,gamedata,chessboard)

        response= {"current_player":game_.chessgamedata.current_player,
                        "status":game_.chessgamedata.status,
                        "board":serialize_board(game_.chessboard_.board),
                        "chessgamedata_id":game_.chessgamedata.id,
                        "chessboard_id":game_.chessboard_.id}
    finally:
        sess.close()
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
    delete_tables()
    create_tables()
    print("mapppp",app.url_map)
    app.run(host='0.0.0.0', port=5000,debug=True)

