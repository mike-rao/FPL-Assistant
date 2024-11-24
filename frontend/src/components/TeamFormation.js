import React from "react";
import "../styles/TeamFormation.css";

function TeamFormation({ selectedPlayers, setSelectedPlayers }) {
  const getPositionCount = (position, includeSubs = false) => {
    const players = includeSubs ? selectedPlayers : selectedPlayers.slice(0, 11);
    return players.filter((p) => p.element_type === position).length;
  };

  const handleClearTeam = () => {
    setSelectedPlayers([]);
  };
  
  const starters = selectedPlayers.slice(0, 11);
  const substitutes = selectedPlayers.slice(11).sort((a, b) => {
    // Sort substitutes, goalkeepers first
    if (a.element_type === 1 && b.element_type !== 1) return -1;
    if (a.element_type !== 1 && b.element_type === 1) return 1;
    return 0;
  });

  const totalCost = selectedPlayers.reduce((sum, player) => sum + player.now_cost, 0);

  return (
    <div className="middle-column">
      <div className="header">
        <div className="title">
          <h2>Team Formation</h2>
        </div>
        <div className="budget-container">
          <span className="budget">Budget: £{totalCost.toFixed(1)}m</span> 
          <button className="clear-button" onClick={handleClearTeam}>Clear</button>
        </div>
      </div>
      <div className="formation">
        {/* Goalkeeper */}
        <div className="player-row">
          {Array.from({ length: getPositionCount(1) }).map((_, index) => (
            <div key={index} className="player-slot">
              {starters.filter((p) => p.element_type === 1)[index]
                ?.second_name || ""}
            </div>
          ))}
        </div>

        {/* Defenders */}
        <div className="player-row">
          {Array.from({ length: getPositionCount(2) }).map((_, index) => (
            <div key={index} className="player-slot">
              {starters.filter((p) => p.element_type === 2)[index]
                ?.second_name || ""}
            </div>
          ))}
        </div>

        {/* Midfielders */}
        <div className="player-row">
          {Array.from({ length: getPositionCount(3) }).map((_, index) => (
            <div key={index} className="player-slot">
              {starters.filter((p) => p.element_type === 3)[index]
                ?.second_name || ""}
            </div>
          ))}
        </div>

        {/* Forwards */}
        <div className="player-row">
          {Array.from({ length: getPositionCount(4) }).map((_, index) => (
            <div key={index} className="player-slot">
              {starters.filter((p) => p.element_type === 4)[index]
                ?.second_name || ""}
            </div>
          ))}
        </div>

        {/* Substitutes */}
        <div className="player-row">
          {substitutes.map((player, index) => (
            <div key={index} className="player-slot">
              {player.second_name}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default TeamFormation;