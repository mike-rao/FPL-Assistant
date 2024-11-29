import React, { useState, useEffect } from "react";
import "./styles/App.css";
import PlayerList from "./components/PlayerList";
import TeamFormation from "./components/TeamFormation";
import TransferSuggestions from "./components/TransferSuggestions";

function App() {
  const [playerData, setPlayerData] = useState([]);
  const [selectedPlayers, setSelectedPlayers] = useState([]);

  const API_BASE_URL =
    process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/get_player_data`);
        const data = await response.json();
        const updatedData = data.map((player) => ({
          ...player,
          position:
            player.position === "FWD"
              ? 4
              : player.position === "MID"
              ? 3
              : player.position === "DEF"
              ? 2
              : 1, // GKP
        }));
        setPlayerData(updatedData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [API_BASE_URL]);

  return (
    <div className="App">
      <h1>Fantasy Premier League Assistant</h1>
      <p>Employ a machine learning assistant manager to build the best team, score more points, and defeat your rivals.</p>
      <div className="columns">
        <PlayerList
          playerData={playerData}
          selectedPlayers={selectedPlayers}
          setSelectedPlayers={setSelectedPlayers}
        />
        <TeamFormation
          selectedPlayers={selectedPlayers}
          setSelectedPlayers={setSelectedPlayers}
        />
        <TransferSuggestions />
      </div>
    </div>
  );
}

export default App;