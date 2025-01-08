import React, { useState, useEffect } from "react";
import "../styles/TeamFormation.css";
import Swal from 'sweetalert2';
import substitutionIcon from "../images/substitution.png";
import redxIcon from "../images/red_x.png";
import jerseyImages from '../helpers/jerseyImages';

export const showPlayerInfo = (player) => {
  Swal.fire({
    html: `
      <style>
        .tooltip-trigger {
          position: relative;
          display: inline-block;
        }

        .tooltip-text {
          visibility: hidden;
          width: 100px;
          background-color: #555;
          color: #fff;
          text-align: center;
          padding: 5px;
          border-radius: 6px;
          position: absolute;
          z-index: 1;
          bottom: 125%; /* Position the tooltip above the text */
          left: 50%;
          margin-left: -60px; /* Center the tooltip */
          opacity: 0;
          transition: opacity 0.3s;
          font-size: 0.8rem;
          font-weight: normal;
        }

        .tooltip-trigger:hover .tooltip-text {
          visibility: visible;
          opacity: 1;
        }
      </style>

      <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
        <!-- Vertical Stack: Position, Name, Team -->
        <div style="text-align: center;">
          <p style="margin: 0; font-size: 1.2em;">
            ${["GKP", "DEF", "MID", "FWD"][player.position - 1]}
          </p>
          <p style="margin: 0; font-size: 1.5em; font-weight: bold;">${player.name}</p>
          <p style="margin: 0; font-size: 1em; color: gray;">${player.team}</p>
        </div>
        
        <!-- Horizontal Stack: Other Stats -->
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 0.7rem; text-align: center; width: 100%">
          <div>
            <p style="margin: 0; font-weight: bold;">Price</p>
            <p style="margin: 0;">£${player.price.toFixed(1)}m</p>
          </div>
          <div style="border-left: 1px solid #ddd; padding-left: 0.7rem;">
            <p style="margin: 0; font-weight: bold;">Form</p>
            <p style="margin: 0;">${player.form}</p>
          </div>
          <div style="border-left: 1px solid #ddd; padding-left: 0.7rem;">
            <p style="margin: 0; font-weight: bold;">Pts/Match</p>
            <p style="margin: 0;">${player.pts_per_match}</p>
          </div>
          <div style="border-left: 1px solid #ddd; padding-left: 0.7rem;">
            <p style="margin: 0; font-weight: bold;">Total Points</p>
            <p style="margin: 0;">${player.total_pts}</p>
          </div>
          <div style="border-left: 1px solid #ddd; padding-left: 0.7rem;">
            <p style="margin: 0; font-weight: bold;">Bonus</p>
            <p style="margin: 0;">${player.total_bonus}</p>
          </div>
          <div style="border-left: 1px solid #ddd; padding-left: 0.7rem;">
            <p style="margin: 0; font-weight: bold;" class="tooltip-trigger">
              ICT Index
              <span class="tooltip-text">Influence, Creativity, and Threat Rating</span>
            </p>
            <p style="margin: 0;">${player.ict_index}</p>
          </div>
          <div style="border-left: 1px solid #ddd; padding-left: 0.7rem;">
            <p style="margin: 0; font-weight: bold;" class="tooltip-trigger">
              TSB%
              <span class="tooltip-text">Teams Selected By Percentage</span>
            </p>
            <p style="margin: 0;">${player["tsb_percent"]}%</p>
          </div>
          <div style="border-left: 1px solid #ddd; padding-left: 0.7rem;">
            <p style="margin: 0; font-weight: bold;" class="tooltip-trigger">
              FDR
              <span class="tooltip-text">Fixture Difficulty Rating</span>
            </p>
            <p style="margin: 0;">${player["fdr"]}</p>
          </div>
        </div>
      </div>
    `,
    showConfirmButton: true,
    confirmButtonText: "Close",
    width: 800,
    padding: "1.5rem",
  });
};

function TeamFormation({ selectedPlayers, setSelectedPlayers, isPickTeamMode, setIsPickTeamMode, highlightedPlayers }) {
  const [activePlayer, setActivePlayer] = useState(null);
  const [previousFormation, setPreviousFormation] = useState(null);

  const handleClearTeam = () => {
    setSelectedPlayers([]);
    setIsPickTeamMode(false);
    setPreviousFormation({ GKP: 1, DEF: 4, MID: 4, FWD: 2 });
  };

  useEffect(() => {
    if (isPickTeamMode) {
      // store the formation when switching to "Pick Team" mode
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
  }, [isPickTeamMode, selectedPlayers]);

  const handleSetTeam = () => {
    if (selectedPlayers.length === 15) {
      const formation = previousFormation || { GKP: 1, DEF: 4, MID: 4, FWD: 2 };
      const sortedPlayers = [];
      let remainingPlayers = [...selectedPlayers];
      // iterate through positions and add starters based on formation
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
      sortedPlayers.push(...remainingPlayers);
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
    setIsPickTeamMode(!isPickTeamMode);
    setActivePlayer(null);
  };

  const handlePlayerRemove = (player) => {
    const updatedPlayers = selectedPlayers.filter((p) => p.id !== player.id);
    setSelectedPlayers(updatedPlayers);
  };

  const handleSubstitution = (player) => {
    if (activePlayer && activePlayer.id === player.id) {
      setActivePlayer(null);
    } else {
      setActivePlayer(player);
    }
  };

  const handlePlayerSwap = (player1, player2) => {
    const updatedPlayers = [...selectedPlayers];
    const index1 = updatedPlayers.findIndex((p) => p.id === player1.id);
    const index2 = updatedPlayers.findIndex((p) => p.id === player2.id);

    [updatedPlayers[index1], updatedPlayers[index2]] = [
        updatedPlayers[index2],
        updatedPlayers[index1],
    ];

    setSelectedPlayers(updatedPlayers);
    setActivePlayer(null);
  };

  const isEligibleForSubstitution = (player) => {
    if (!activePlayer) return false; // if no active player then no substitutions possible
    if (activePlayer.id === player.id) return false; // same player cannot swap with itself
    // GKP can only swap with another GKP
    if (activePlayer.position === 1 || player.position === 1) {
      return activePlayer.position === 1 && player.position === 1;
    }
    const activePlayerIsStarter = starters.includes(activePlayer);
    const targetPlayerIsStarter = starters.includes(player);
    const activePlayerIsSubstitute = substitutes.includes(activePlayer);
    const currentDefendersCount = getPositionCount(2);
    // restrict substitutions when only 3 starting defenders remain
    if (currentDefendersCount === 3) {
      if (activePlayerIsStarter && activePlayer.position === 2) {
        // starting defenders can only swap with other starting defenders
        return targetPlayerIsStarter && player.position === 2;
      }
      if (activePlayerIsSubstitute) {
        // substitutes cannot swap with starting defenders
        return player.position !== 2 || !targetPlayerIsStarter;
      }
    }
    // allow starters to swap with other starters of the same position
    if (activePlayerIsStarter && targetPlayerIsStarter && activePlayer.position === player.position) {
      return true;
    }
    // allow substitutes to swap with players of different positions except GKP
    if (activePlayerIsSubstitute && player.position !== 1) {
      return true;
    }
    // default allow swapping only for the same position
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

  const getJerseyImage = (player) => {
    if (!player) return jerseyImages['Unknown'];
    if (player.position === 1) {
      return jerseyImages['Goalkeeper'] || jerseyImages['Unknown Goalkeeper'];
    }
    return jerseyImages[player.team] || jerseyImages['Unknown'];
  };

  const PlayerRow = ({ position, maxPlayers }) => {
    const players = selectedPlayers.filter((p) => p.position === position);
    return (
      <div className="player-row">
        {Array.from({ length: maxPlayers }).map((_, index) => {
          const player = players[index];
          return (
            <div
              key={index}
              className={`player-slot ${getPlayerClass(player)} ${highlightedPlayers.includes(player?.name) ? 'highlight' : ''}`}
              onClick={() => {
                if (player) {
                  if (!isPickTeamMode || (isPickTeamMode && !activePlayer)) {
                    showPlayerInfo(player);
                  } else if (isPickTeamMode && activePlayer) {
                    handlePlayerSwap(activePlayer, player);
                  }
                }
              }}
            >
              <div className="player-slot-top">
                {isPickTeamMode && player && (
                    <img
                    src={substitutionIcon}
                    alt="Sub"
                    className="sub-icon"
                    onClick={(e) => {
                        e.stopPropagation();
                        handleSubstitution(player);
                    }}
                    />
                )}
                {!isPickTeamMode && player && (
                  <img
                    src={redxIcon}
                    alt="Remove"
                    className="remove-icon"
                    onClick={(e) => {
                      e.stopPropagation();
                      handlePlayerRemove(player);
                    }}
                  />
                )}
                {player?.price && (
                  <div className="player-price">£{player.price}m</div>
                )}
              </div>
              {player?.team && (
                <img 
                    src={getJerseyImage(player)} 
                    alt={`${player?.team || "Unknown"} jersey`} 
                    className="player-jersey" 
                />
              )}
              <span className="player-name">{player?.display_name || ""}</span>
              <span className = "player-team">{player?.team}</span>
            </div>
          );
        })}
      </div>
    );
  };    

  return (
    <div className={`middle-column ${isPickTeamMode ? 'pick-team-mode' : ''}`}>
      <div className="title">
        <div className="header-container">
          {!isPickTeamMode && <svg class="invisible"></svg>}
          <h2>{isPickTeamMode ? "Your Team" : "Build Team"}</h2>
          {!isPickTeamMode && <svg class="search-icon tab" viewBox="0 0 24 24"><g><path d="M21.53 20.47l-3.66-3.66C19.195 15.24 20 13.214 20 11c0-4.97-4.03-9-9-9s-9 4.03-9 9 4.03 9 9 9c2.215 0 4.24-.804 5.808-2.13l3.66 3.66c.147.146.34.22.53.22s.385-.073.53-.22c.295-.293.295-.767.002-1.06zM3.5 11c0-4.135 3.365-7.5 7.5-7.5s7.5 3.365 7.5 7.5-3.365 7.5-7.5 7.5-7.5-3.365-7.5-7.5z"></path></g></svg>}
        </div>
      </div>
      <div className="team-formation-container">
        <div className="budget-container">
          <span className="budget">Budget: £{totalCost.toFixed(1)}m</span>
          <div className="buttons-container">
          {isPickTeamMode ? (
            <button className="edit-team-button orange-hover" onClick={handleToggleMode}>
              Edit Team
            </button>
          ) : (
            <>
              <button className="set-team-button orange-hover" onClick={handleSetTeam}>
                Set Team
              </button>
              <button className="clear-button orange-hover" onClick={handleClearTeam}>
                Clear
              </button>
            </>
          )}
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
                      className={`player-slot ${getPlayerClass(player)} ${highlightedPlayers.includes(player?.name) ? 'highlight' : ''}`}
                      onClick={() => {
                          if (player) {
                            if (!isPickTeamMode || (isPickTeamMode && !activePlayer)) {
                              showPlayerInfo(player);
                            } else if (isPickTeamMode && activePlayer) {
                              handlePlayerSwap(activePlayer, player);
                            }
                          }
                      }}
                  >
                      <div className="player-slot-top">
                          {isPickTeamMode && player && (
                              <img
                              src={substitutionIcon}
                              alt="Sub"
                              className="sub-icon"
                              onClick={(e) => {
                                  e.stopPropagation();
                                  handleSubstitution(player);
                              }}
                              />
                          )}
                          {player?.price && (
                          <div className="player-price">£{player.price}m</div>
                          )}
                      </div>
                      {player?.team && (
                          <img 
                              src={getJerseyImage(player)} 
                              alt={`${player?.team || "Unknown"} jersey`} 
                              className="player-jersey" 
                          />
                      )}
                      <span className="player-name" onClick={() => activePlayer && handlePlayerSwap(activePlayer, player)}>
                      {player?.display_name || ""}
                      </span>
                      <span className = "player-team">{player?.team}</span>
                  </div>
                  ))}
              </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TeamFormation;