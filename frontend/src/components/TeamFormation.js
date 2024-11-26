// frontend/src/components/TeamFormation.js
import React, { useState, useEffect } from "react";
import "../styles/TeamFormation.css";
import Swal from 'sweetalert2';
import substitutionIcon from "../images/substitution.png";

function TeamFormation({ selectedPlayers, setSelectedPlayers }) {
  const [isPickTeamMode, setIsPickTeamMode] = useState(false);
  const [activePlayer, setActivePlayer] = useState(null);
  const [previousFormation, setPreviousFormation] = useState(null);

  const handleClearTeam = () => {
    setSelectedPlayers([]);
    setIsPickTeamMode(false); // Reset to Team Formation mode
    setPreviousFormation({ GKP: 1, DEF: 4, MID: 4, FWD: 2 });
  };

  useEffect(() => {
    if (isPickTeamMode) {
      // Store the formation when switching to "Pick Team" mode
      const startersCount = selectedPlayers.slice(0, 11).reduce(
        (counts, player) => {
          const positionName = ["GKP", "DEF", "MID", "FWD"][player.position - 1];
          counts[positionName]++;
          return counts;
        },
        { GKP: 0, DEF: 0, MID: 0, FWD: 0 }
      );
      setPreviousFormation(startersCount);
    }
  }, [isPickTeamMode, selectedPlayers]); // Run effect when mode or players change

  const handleSetTeam = () => {
    if (selectedPlayers.length === 15) {
      // If no previous formation, default to 4-4-2
      const formation = previousFormation || { GKP: 1, DEF: 4, MID: 4, FWD: 2 };
      const sortedPlayers = [];
      let remainingPlayers = [...selectedPlayers];
      // Iterate through positions and add starters based on formation
      for (const position of [1, 2, 3, 4]) {
        const positionPlayers = remainingPlayers.filter(
          (p) => p.position === position
        );
        sortedPlayers.push(
          ...positionPlayers.slice(
            0,
            formation[["GKP", "DEF", "MID", "FWD"][position - 1]]
          )
        );
        remainingPlayers = remainingPlayers.filter(
          (p) => !sortedPlayers.includes(p)
        );
      }
      sortedPlayers.push(...remainingPlayers); // Add remaining as subs
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
    setActivePlayer(null); // Reset active player to clear substitution state
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
    // Get the current number of starting defenders
    const currentDefendersCount = getPositionCount(2);
    // Rule: Restrict swaps when only 3 starting defenders remain
    if (currentDefendersCount === 3) {
      if (activePlayerIsStarter && activePlayer.position === 2) {
        // Starting defenders can only swap with other starting defenders
        return targetPlayerIsStarter && player.position === 2;
      }
      if (activePlayerIsSubstitute) {
        // Substitutes cannot swap with starting defenders
        return player.position !== 2 || !targetPlayerIsStarter;
      }
    }
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

  const PlayerRow = ({ position, maxPlayers }) => {
    const players = selectedPlayers.filter((p) => p.position === position);
    return (
      <div className="player-row">
        {Array.from({ length: maxPlayers }).map((_, index) => {
          const player = players[index];
          return (
            <div
              key={index}
              className={`player-slot ${getPlayerClass(player)}`}
              onClick={() =>
                activePlayer && player && handlePlayerSwap(activePlayer, player)
              }
            >
              {isPickTeamMode && player && (
                <img
                  src={substitutionIcon}
                  alt="Sub"
                  className="sub-icon"
                  onClick={() => handleSubstitution(player)}
                />
              )}
              <span className="player-name">{player?.last_name || ""}</span>
            </div>
          );
        })}
      </div>
    );
  };

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
        <PlayerRow position={1} maxPlayers={isPickTeamMode ? getPositionCount(1) : 2} /> {/* GKPs */}
        <PlayerRow position={2} maxPlayers={isPickTeamMode ? getPositionCount(2) : 5} /> {/* DEFs */}
        <PlayerRow position={3} maxPlayers={isPickTeamMode ? getPositionCount(3) : 5} /> {/* MIDs */}
        <PlayerRow position={4} maxPlayers={isPickTeamMode ? getPositionCount(4) : 3} /> {/* FWDs */}
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