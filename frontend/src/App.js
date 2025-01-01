import React, { useState, useEffect, useCallback } from "react";
import "./styles/App.css";
import PlayerList from "./components/PlayerList";
import TeamFormation from "./components/TeamFormation";
import Analytics from "./components/Analytics";
import Swal from 'sweetalert2';

function App() {
  const [playerData, setPlayerData] = useState([]);
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [isPickTeamMode, setIsPickTeamMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

  const fetchPlayerData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/players`);
      if (!response.ok) {
        throw new Error(`Error fetching player data: ${response.statusText}`);
      }
      const data = await response.json();
      const updatedData = data.map((player) => ({
        ...player,
        position:
          player.position === "Forward"
            ? 4
            : player.position === "Midfielder"
            ? 3
            : player.position === "Defender"
            ? 2
            : 1, // GKP
      }));
      setPlayerData(updatedData);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }, [API_BASE_URL]);

  const scrapeAndSave = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/scrape-and-save`, {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error(`Error scraping and saving data: ${response.statusText}`);
      }
      const result = await response.json();
      Swal.fire({
        text: `${result.message}`,
        icon: 'success',
        confirmButtonText: 'OK',
      });
      await fetchPlayerData();
    } catch (error) {
      setError(error.message);
      console.error("Error scraping and saving data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlayerData();
  }, [fetchPlayerData]);

  return (
    <div className="App">
      <h1>Fantasy Premier League Assistant</h1>
      <p>Employ a machine learning assistant manager to build the best team, score more points, and defeat your rivals.</p>
      <div className="columns">
        <PlayerList
          playerData={playerData}
          selectedPlayers={selectedPlayers}
          setSelectedPlayers={setSelectedPlayers}
          loading={loading}
        />
        <TeamFormation
          selectedPlayers={selectedPlayers}
          setSelectedPlayers={setSelectedPlayers}
          isPickTeamMode={isPickTeamMode}
          setIsPickTeamMode={setIsPickTeamMode}
        />
        <Analytics 
          selectedPlayers={selectedPlayers}
          setSelectedPlayers={setSelectedPlayers}
          isPickTeamMode={isPickTeamMode}
        />
      </div>
    </div>
  );
}

export default App;