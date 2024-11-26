// frontend/src/components/TeamFormation.js
import React, { useState } from "react";
import "../styles/TeamFormation.css";
import Swal from 'sweetalert2';

function TeamFormation({ selectedPlayers, setSelectedPlayers }) {
  const [isPickTeamMode, setIsPickTeamMode] = useState(false);

  const handleClearTeam = () => {
    setSelectedPlayers([]);
    setIsPickTeamMode(false); // Reset to Team Formation mode
  };

  const handleSetTeam = () => {
    if (selectedPlayers.length === 15) {
      const positionCounts = { GKP: 1, DEF: 4, MID: 4, FWD: 2 }; // Starters count
      const sortedPlayers = [];
      let remainingPlayers = [...selectedPlayers];

      // Iterate through positions and add starters, then subs
      for (const position of [1, 2, 3, 4]) { 
        const positionPlayers = remainingPlayers.filter(p => p.position === position);
        sortedPlayers.push(...positionPlayers.slice(0, positionCounts[["GKP", "DEF", "MID", "FWD"][position - 1]]));
        remainingPlayers = remainingPlayers.filter(p => !sortedPlayers.includes(p));
      }

      sortedPlayers.push(...remainingPlayers); // Add the remaining players as subs

      setSelectedPlayers(sortedPlayers);
      setIsPickTeamMode(true);
    } else {
      Swal.fire({
        text: "You need to pick 15 players",
        icon: "warning",
        confirmButtonText: "OK",
      });
    }
  };

  const handleToggleMode = () => {
    setIsPickTeamMode(!isPickTeamMode); // Toggle between modes
  };

  const getPositionCount = (position, includeSubs = false) => {
    const players = includeSubs ? selectedPlayers : selectedPlayers.slice(0, 11);
    return players.filter((p) => p.position === position).length;
  };

  const starters = selectedPlayers.slice(0, 11);
  const substitutes = selectedPlayers.slice(11).sort((a, b) => {
    if (a.position === 1 && b.position !== 1) return -1;
    if (a.position !== 1 && b.position === 1) return 1;
    return 0;
  });

  const totalCost = selectedPlayers.reduce((sum, player) => sum + player.price, 0);

  return (
    <div className={`middle-column ${isPickTeamMode ? 'pick-team-mode' : ''}`}>
      <div className="header">
        <div className="title">
          <h2>{isPickTeamMode ? "Pick Team" : "Team Formation"}</h2>
        </div>
        <div className="budget-container">
          <span className="budget">Budget: £{totalCost.toFixed(1)}m</span>
          <div className="buttons-container">
          {isPickTeamMode ? (
            <button className="mode-button" onClick={handleToggleMode}>
              Team Formation
            </button>
          ) : (
            <>
              <button className="mode-button" onClick={handleSetTeam}>
                Set Team
              </button>
              <button className="clear-button" onClick={handleClearTeam}>
                Clear
              </button>
            </>
          )}
          </div>
        </div>
      </div>
      <div className="formation">
        {/* Goalkeeper */}
        <div className="player-row">
          {Array.from({
            length: isPickTeamMode ? getPositionCount(1) : 2, // Display all GKs in Team Formation mode
          }).map((_, index) => (
            <div key={index} className="player-slot">
              {selectedPlayers.filter((p) => p.position === 1)[index]
                ?.last_name || ""}
            </div>
          ))}
        </div>

        {/* Defenders */}
        <div className="player-row">
          {Array.from({
            length: isPickTeamMode ? getPositionCount(2) : 5, // Display all DEFs in Team Formation mode
          }).map((_, index) => (
            <div key={index} className="player-slot">
              {selectedPlayers.filter((p) => p.position === 2)[index]
                ?.last_name || ""}
            </div>
          ))}
        </div>

        {/* Midfielders */}
        <div className="player-row">
          {Array.from({
            length: isPickTeamMode ? getPositionCount(3) : 5, // Display all MIDs in Team Formation mode
          }).map((_, index) => (
            <div key={index} className="player-slot">
              {selectedPlayers.filter((p) => p.position === 3)[index]
                ?.last_name || ""}
            </div>
          ))}
        </div>

        {/* Forwards */}
        <div className="player-row">
          {Array.from({
            length: isPickTeamMode ? getPositionCount(4) : 3, // Display all FWDS in Team Formation mode
          }).map((_, index) => (
            <div key={index} className="player-slot">
              {selectedPlayers.filter((p) => p.position === 4)[index]
                ?.last_name || ""}
            </div>
          ))}
        </div>

        {/* Substitutes (only in Pick Team mode) */}
        {isPickTeamMode && (
          <div className="player-row">
            {substitutes.map((player, index) => (
              <div key={index} className="player-slot">
                {player.last_name}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default TeamFormation;