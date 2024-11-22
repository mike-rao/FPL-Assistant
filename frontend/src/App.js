import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [playerData, setPlayerData] = useState([]);

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000'; 

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/get_player_data`);
        const data = await response.json();
        setPlayerData(data); 
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [API_BASE_URL]);

  return (
    <div className="App">
      <h1>FPL Assistant</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Team</th>
            <th>Position</th>
            <th>Cost</th>
            <th>Total Points</th>
          </tr>
        </thead>
        <tbody>
          {playerData.map((player) => (
            <tr key={player.id}>
              <td>{player.first_name} {player.second_name}</td>
              <td>{player.team}</td>
              <td>{player.element_type}</td>
              <td>{player.now_cost}</td>
              <td>{player.total_points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;