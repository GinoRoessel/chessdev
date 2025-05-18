import logo from './logo.svg';
import './App.css';
import {ChessBoardWrapper, renderBoard} from './board.js';
import React, { useEffect, useState, useRef } from 'react';

function App() {
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

  const handleRestart = () => alert('Restart');
  const handleLastGame = () => alert('Last Game');
  const handleNextGame = () => alert('Next Game');
  const handleLastMove = () => alert('Last Move');
  const handleNextMove = () => alert('Next Move');


  return (
    <div className="app-container">
      <div className="top-frame">
        <div className="status-label">{status}</div>
        <div className="current-player-label">{currentPlayer}</div>
        <div className="board-frame">
          <ChessBoardWrapper
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