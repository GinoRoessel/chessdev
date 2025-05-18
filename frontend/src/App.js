import logo from './logo.svg';
import './App.css';
import {ChessBoardWrapper, renderBoard} from './board.js';
import React, { useEffect, useState, useRef } from 'react';

function App() {
  const [gameKey, setGameKey] = useState(Date.now());
  const chessgamedata_id= useRef(null);
  const chessboard_id= useRef(null);
  const [status, setStatus] = useState('');
  const [currentPlayer, setCurrentPlayer] = useState('');
  const [boardData, setBoardData] = useState([]);


  useEffect(() => {
  fetch("http://localhost:5000/game", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({})
  })
    .then((res) => res.json())
    .then((data) => {
      chessgamedata_id.current=data.chessgamedata_id;
      chessboard_id.current=data.chessboard_id;
      setStatus(data.status);
      setCurrentPlayer(data.current_player);
      setBoardData(data.board); 
      console.log("Backend-Daten:", data);
    })
    .catch((err) => {
      console.error("Fehler beim Laden der Spieldaten:", err);
    });
}, []);

  const handleRestart = () =>{
  fetch("http://localhost:5000/game", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({})
  })
    .then((res) => res.json())
    .then((data) => {
      chessgamedata_id.current=data.chessgamedata_id;
      chessboard_id.current=data.chessboard_id;
      setStatus(data.status);
      setCurrentPlayer(data.current_player);
      setBoardData(data.board); 
      setGameKey(Date.now())
      console.log("Backend-Daten:", data);
    })
    .catch((err) => {
      console.error("Fehler beim Laden der Spieldaten:", err);
    });
};;

  const handleLastGame = () => {
    console.log("Typ gamedata_id:", typeof chessgamedata_id.current);
    console.log("Wert gamedata_id:", chessgamedata_id.current);
    console.log("letzter check davor",chessgamedata_id.current, chessboard_id.current)
    const query= new URLSearchParams({
      gamedata_id: String(chessgamedata_id.current),
      board_id: String(chessboard_id.current),
      before:'true',
      after:'false'
    }).toString();
    console.log("wirklich letzter check davor",query)
  fetch(`http://localhost:5000/game/get?${query}`, {
    method: "GET"
  })
    .then((res) => res.json())
    .then((data) => {
      chessgamedata_id.current=data.chessgamedata_id;
      chessboard_id.current=data.chessboard_id;
      setStatus(data.status);
      setCurrentPlayer(data.current_player);
      setBoardData(data.board); 
      setGameKey(Date.now())
      console.log("Backend-Daten:", data);
    })
    .catch((err) => {
      console.error("Fehler beim Laden der Spieldaten:", err);
    });
};;;


  const handleNextGame = () => {
    console.log("Typ gamedata_id:", typeof chessgamedata_id.current);
    console.log("Wert gamedata_id:", chessgamedata_id.current);
    console.log("letzter check davor",chessgamedata_id.current, chessboard_id.current)
    const query= new URLSearchParams({
      gamedata_id: String(chessgamedata_id.current),
      board_id: String(chessboard_id.current),
      before:'false',
      after:'true'
    }).toString();
    console.log("wirklich letzter check davor",query)
  fetch(`http://localhost:5000/game/get?${query}`, {
    method: "GET"
  })
    .then((res) => res.json())
    .then((data) => {
      chessgamedata_id.current=data.chessgamedata_id;
      chessboard_id.current=data.chessboard_id;
      setStatus(data.status);
      setCurrentPlayer(data.current_player);
      setBoardData(data.board); 
      setGameKey(Date.now())
      console.log("Backend-Daten:", data);
    })
    .catch((err) => {
      console.error("Fehler beim Laden der Spieldaten:", err);
    });
};;;


  const handleLastMove = () => {
    const requestData = {
      chessgamedata_id: chessgamedata_id.current,
      chessboard_id: chessboard_id.current,
      startrow: null,
      startcol: null,
      endrow: null,
      endcol: null,
      nextmove: false,
      lastmove: true,
    };
    fetch("http://localhost:5000/game/move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestData)
    })
    .then(res => res.json())
    .then(data => {
      console.log("Antwort vom Server:", data);
      setStatus(data.status);
      setCurrentPlayer(data.current_player);
      setBoardData(data.board)
    })
    .catch(err => {
      console.error("Fehler bei der Anfrage:", err);
    });;
  }
  const handleNextMove = () => {
    const requestData = {
      chessgamedata_id: chessgamedata_id.current,
      chessboard_id: chessboard_id.current,
      startrow: null,
      startcol: null,
      endrow: null,
      endcol: null,
      nextmove: true,
      lastmove: false,
    };
    fetch("http://localhost:5000/game/move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestData)
    })
    .then(res => res.json())
    .then(data => {
      console.log("Antwort vom Server:", data);
      setStatus(data.status);
      setCurrentPlayer(data.current_player);
      setBoardData(data.board)
    })
    .catch(err => {
      console.error("Fehler bei der Anfrage:", err);
    });;
  };


  return (
    <div className="app-container">
      <div className="top-frame">
        <div className="status-label">{status}</div>
        <div className="current-player-label">{currentPlayer}</div>
        <div className="board-frame">
          <ChessBoardWrapper
          key={gameKey}
          board={boardData} 
          chessgamedataId={chessgamedata_id.current} 
          chessboardId={chessboard_id.current}
          setStatus={setStatus}
          setCurrentPlayer={setCurrentPlayer}
          setBoardData={setBoardData}
      />
        </div>
      </div>

      <div className="bottom-frame">
        <button onClick={handleRestart}>restart</button>
        <button onClick={handleLastGame}>lastgame</button>
        <button onClick={handleNextGame}>nextgame</button>
        <button onClick={handleLastMove}>lastmove</button>
        <button onClick={handleNextMove}>nextmove</button>
      </div>
    </div>
  );


}

export default App;