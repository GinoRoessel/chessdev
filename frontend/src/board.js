
import React from 'react'


export const ChessBoardWrapper=({board, chessgamedataId, chessboardId, setStatus,setCurrentPlayer, setBoardData})=>{
  const selectedSquares= React.useRef([])

  const handleOnSquareClick = (row,col) =>{
    if (selectedSquares.current.length === 0){
      selectedSquares.current=[[row,col]]
    } else if (selectedSquares.current.length === 1){
      const start = selectedSquares.current[0];
      const end =[row, col]
      selectedSquares.current=[]

      const requestData = {
      chessgamedata_id: chessgamedataId,
      chessboard_id: chessboardId,
      startrow: start[0],
      startcol: start[1],
      endrow: end[0],
      endcol: end[1],
      nextmove: false,
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
    });
  }


}
  const renderBoard = (board,handleOnSquareClick) => {
    const squares = [];
    for(let row=0; row<8; row++) {
      for(let col=0; col<8; col++) {
        const isLight = (row + col) % 2 === 0;
        const symbol = board && board[row] && board[row][col] ? board[row][col][0] : '';
        const color = board && board[row] && board[row][col] ? board[row][col][1] : 'black'; 
        squares.push(
          <button
            key={`${row}-${col}`}
            className={`square ${isLight ? 'light' : 'dark'}`}
            onClick={() => handleOnSquareClick(row,col)}
            style={{color: color}}
          >
           {symbol}
          </button>
        );
      }
    }
    return squares;
  }

  return renderBoard(board,handleOnSquareClick);
};
