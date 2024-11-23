import React, { useState } from "react";
import "../styles/PlayerList.css";

function PlayerList({ playerData, selectedPlayers, setSelectedPlayers }) {
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
    const position = ["GKP", "DEF", "MID", "FWD"][player.element_type - 1];
    const currentCount = selectedPlayers.filter(
      (p) => ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === position,
    ).length;

    if (currentCount < positionCounts[position]) {
      setSelectedPlayers([...selectedPlayers, player]);
    } else {
      alert(`You already have the maximum number of ${position}s`);
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
    const position = ["GKP", "DEF", "MID", "FWD"][player.element_type - 1];
    if (filter !== "All players" && filter !== position) {
      return false;
    }
    if (
      searchTerm &&
      !`${player.first_name} ${player.second_name}`
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  return (
    <div className="left-column">
      <h2>Player Selection</h2>
      <div>
        <select value={filter} onChange={handleFilterChange}>
          <option value="All players">All players</option>
          <option value="GKP">Goalkeepers</option>
          <option value="DEF">Defenders</option>
          <option value="MID">Midfielders</option>
          <option value="FWD">Attackers</option>
        </select>
        <input
          type="text"
          placeholder="Search by name"
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>
      <div className="player-list">
        {filteredPlayers.map((player) => (
          <div
            key={player.id}
            onClick={() => handlePlayerSelect(player)}
            className={
              selectedPlayers.find((p) => p.id === player.id) ? "selected" : ""
            }
          >
            {player.first_name} {player.second_name}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PlayerList;