import React, { useState } from "react";
import "../styles/PlayerList.css";
import Swal from 'sweetalert2';

function PlayerList({ playerData, selectedPlayers, setSelectedPlayers, loading }) {
  const [filter, setFilter] = useState("All players");
  const [searchTerm, setSearchTerm] = useState("");

  const handlePlayerSelect = (player) => {
    if (selectedPlayers.find((p) => p.id === player.id)) {
      setSelectedPlayers(selectedPlayers.filter((p) => p.id !== player.id));
      return;
    }

    const positionCounts = {
      GKP: 2,
      DEF: 5,
      MID: 5,
      FWD: 3,
    };
    const position = ["GKP", "DEF", "MID", "FWD"][player.position - 1];
    const currentCount = selectedPlayers.filter(
      (p) => ["GKP", "DEF", "MID", "FWD"][p.position - 1] === position,
    ).length;
    const totalCount = selectedPlayers.length;
    const teamCount = selectedPlayers.filter((p) => p.team === player.team).length;
    
    if (totalCount === 15) {
        Swal.fire({
            text: 'You already have the maximum number of players',
            icon: 'warning',
            confirmButtonText: 'OK'
          });
    }
    else if (currentCount >= positionCounts[position]) {
        Swal.fire({
            text: `You already have the maximum number of ${position}s`,
            icon: 'warning',
            confirmButtonText: 'OK'
          });
    }
    else if (teamCount >= 3) {
        Swal.fire({
            text: `You cannot select more than 3 players from one team`,
            icon: 'warning',
            confirmButtonText: 'OK',
        });
    }
    else {
      setSelectedPlayers([...selectedPlayers, player]);
    }
  };

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
    setSearchTerm("");
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredPlayers = playerData.filter((player) => {
    const position = ["GKP", "DEF", "MID", "FWD"][player.position - 1];
    if (filter !== "All players" && filter !== position) {
      return false;
    }
    if (
      searchTerm &&
      !`${player.name}`
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  const sortedPlayers = [...filteredPlayers].sort((a, b) => b.total_pts - a.total_pts);

  return (
    <div className="left-column">
      <h2>Player Selection</h2>
      <div className = "player-filters">
        <select className = "filter" value={filter} onChange={handleFilterChange}>
          <option value="All players">All players</option>
          <option value="GKP">Goalkeepers</option>
          <option value="DEF">Defenders</option>
          <option value="MID">Midfielders</option>
          <option value="FWD">Attackers</option>
        </select>
        <input className = "search"
          type="text"
          placeholder="Search by name"
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>
      <div className="player-list">
        {loading ? (
          <div className="loader__btn">
            <div className="loader"></div>
            Loading...
          </div>
        ) : (
          sortedPlayers.map((player) => (
            <div
              key={player.id}
              onClick={() => handlePlayerSelect(player)}
              className={
                selectedPlayers.find((p) => p.id === player.id) ? "selected" : ""
              }
            >
              {player.name} 
              <span className="player-team-display"> | {["GKP", "DEF", "MID", "FWD"][player.position - 1]} | {player.team}</span> 
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default PlayerList;