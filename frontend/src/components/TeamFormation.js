// frontend/src/components/TeamFormation.js
import React, { useState } from "react";
import "../styles/TeamFormation.css";
import Swal from 'sweetalert2';
import substitutionIcon from "../images/substitution.png";

function TeamFormation({ selectedPlayers, setSelectedPlayers }) {
  const [isPickTeamMode, setIsPickTeamMode] = useState(false);
  const [activePlayer, setActivePlayer] = useState(null);

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

  const handleSubstitution = (player) => {
    if (activePlayer && activePlayer.id === player.id) {
      // If the same player is clicked again, deactivate
      setActivePlayer(null);
    } else {
      // Otherwise, activate the clicked player
      setActivePlayer(player);
    }
  };

  const handlePlayerSwap = (player1, player2) => {
    // Allow swapping between any players
    const canSwap =
      (player1.position === player2.position) || // Same position
      (player1.position !== 1 && player2.position !== 1 && getPositionCount(2) > 3) || // Field player swaps maintaining 3 defenders
      (player1.position === 2 && player2.position === 2); // Defender-to-defender swap
  
    if (canSwap) {
      const updatedPlayers = [...selectedPlayers];
      const index1 = updatedPlayers.findIndex((p) => p.id === player1.id);
      const index2 = updatedPlayers.findIndex((p) => p.id === player2.id);
  
      // Perform the swap
      [updatedPlayers[index1], updatedPlayers[index2]] = [
        updatedPlayers[index2],
        updatedPlayers[index1],
      ];
  
      setSelectedPlayers(updatedPlayers);
      setActivePlayer(null); // Reset active player
    } else {
      Swal.fire({
        text: "Invalid substitution. Ensure you maintain at least 3 defenders.",
        icon: "warning",
        confirmButtonText: "OK",
      });
    }
  };

  const isEligibleForSubstitution = (player) => {
    if (!activePlayer) return false; // No active player, no substitutions possible
    if (activePlayer.id === player.id) return false; // Same player cannot swap with itself
    // Goalkeeper substitution logic: GK can only swap with another GK
    if (activePlayer.position === 1 || player.position === 1) {
      return activePlayer.position === 1 && player.position === 1;
    }
    // Determine if players are starters or substitutes
    const activePlayerIsStarter = starters.includes(activePlayer);
    const targetPlayerIsStarter = starters.includes(player);
    const activePlayerIsSubstitute = substitutes.includes(activePlayer);
    // Allow starters to swap with other starters of the same position
    if (activePlayerIsStarter && targetPlayerIsStarter && activePlayer.position === player.position) {
      return true;
    }
    // Allow substitutes to swap with starters or substitutes of different positions (except GK)
    if (activePlayerIsSubstitute && player.position !== 1) {
      return true;
    }
    // Default logic: Allow swapping only for the same position
    return activePlayer.position === player.position;
  };

  const getPlayerClass = (player) => {
    if (activePlayer && activePlayer.id === player.id) return "active";
    if (activePlayer && isEligibleForSubstitution(player)) return "eligible";
    if (activePlayer && !isEligibleForSubstitution(player)) return "disabled";
    return "";
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
            {Array.from({ length: isPickTeamMode ? getPositionCount(1) : 2 }).map((_, index) => {
                const player = selectedPlayers.filter((p) => p.position === 1)[index];
                return (
                <div
                    key={index}
                    className={`player-slot ${getPlayerClass(player)}`}
                >
                    {isPickTeamMode && (
                    <img
                        src={substitutionIcon}
                        alt="Sub"
                        className="sub-icon"
                        onClick={() => handleSubstitution(player)}
                    />
                    )}
                    <span
                    className="player-name"
                    onClick={() =>
                        activePlayer && handlePlayerSwap(activePlayer, player)
                    }
                    >
                    {player?.last_name || ""}
                    </span>
                </div>
                );
            })}
        </div>

        {/* Defenders */}
        <div className="player-row">
            {Array.from({ length: isPickTeamMode ? getPositionCount(2) : 5 }).map((_, index) => {
                const player = selectedPlayers.filter((p) => p.position === 2)[index];
                return (
                <div
                    key={index}
                    className={`player-slot ${getPlayerClass(player)}`}
                >
                    {isPickTeamMode && (
                    <img
                        src={substitutionIcon}
                        alt="Sub"
                        className="sub-icon"
                        onClick={() => handleSubstitution(player)}
                    />
                    )}
                    <span
                    className="player-name"
                    onClick={() =>
                        activePlayer && handlePlayerSwap(activePlayer, player)
                    }
                    >
                    {player?.last_name || ""}
                    </span>
                </div>
                );
            })}
        </div>

        {/* Midfielders */}
        <div className="player-row">
            {Array.from({ length: isPickTeamMode ? getPositionCount(3) : 5 }).map((_, index) => {
                const player = selectedPlayers.filter((p) => p.position === 3)[index];
                return (
                <div
                    key={index}
                    className={`player-slot ${getPlayerClass(player)}`}
                >
                    {isPickTeamMode && (
                    <img
                        src={substitutionIcon}
                        alt="Sub"
                        className="sub-icon"
                        onClick={() => handleSubstitution(player)}
                    />
                    )}
                    <span
                    className="player-name"
                    onClick={() =>
                        activePlayer && handlePlayerSwap(activePlayer, player)
                    }
                    >
                    {player?.last_name || ""}
                    </span>
                </div>
                );
            })}
        </div>

        {/* Forwards */}
        <div className="player-row">
            {Array.from({ length: isPickTeamMode ? getPositionCount(4) : 3 }).map((_, index) => {
                const player = selectedPlayers.filter((p) => p.position === 4)[index];
                return (
                <div
                    key={index}
                    className={`player-slot ${getPlayerClass(player)}`}
                >
                    {isPickTeamMode && (
                    <img
                        src={substitutionIcon}
                        alt="Sub"
                        className="sub-icon"
                        onClick={() => handleSubstitution(player)}
                    />
                    )}
                    <span
                    className="player-name"
                    onClick={() =>
                        activePlayer && handlePlayerSwap(activePlayer, player)
                    }
                    >
                    {player?.last_name || ""}
                    </span>
                </div>
                );
            })}
        </div>

        {/* Substitutes (only in Pick Team mode) */}
        {isPickTeamMode && (
            <div className="player-row substitutes-row">
                {substitutes.map((player, index) => (
                <div
                    key={index}
                    className={`player-slot ${getPlayerClass(player)}`}
                >
                    {isPickTeamMode && (
                    <img
                        src={substitutionIcon}
                        alt="Sub"
                        className="sub-icon"
                        onClick={() => handleSubstitution(player)}
                    />
                    )}
                    <span
                    className="player-name"
                    onClick={() => activePlayer && handlePlayerSwap(activePlayer, player)}
                    >
                    {player?.last_name || ""}
                    </span>
                </div>
                ))}
            </div>
        )}
      </div>
    </div>
  );
}

export default TeamFormation;