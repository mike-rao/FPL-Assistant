import React, { useState } from "react";
import "../styles/Analytics.css";

function Analytics({ selectedPlayers, isPickTeamMode }) {
  const [freeTransfers, setFreeTransfers] = useState(0);
  const [transferBudget, setTransferBudget] = useState(0);

  const handleFreeTransferChange = (event) => {
    const newTransfers = parseFloat(event.target.value) || 0;
    setFreeTransfers(Math.max(0, Math.min(5,newTransfers)));
  };

  const handleFreeTransferIncrement = (increment) => {
    setFreeTransfers(Math.max(0, Math.min(5, freeTransfers + increment)));
  };

  const handleBudgetChange = (event) => {
    const newBudget = parseFloat(event.target.value) || 0;
    setTransferBudget(Math.max(0, newBudget));
  };

  const handleBudgetIncrement = (increment) => {
    setTransferBudget(Math.max(0, parseFloat((transferBudget + increment).toFixed(1))));
  };

  const isGetTransfersEnabled = freeTransfers > 0 && transferBudget >= 0;

  const calculateTeamScore = () => {
    // Calculate the total score of selectedPlayers (replace with your logic)
    return selectedPlayers.reduce((sum, player) => sum + player.score, 0); 
  };

  const AnalyticsDisplay = ({}) => {
    return (
      <div>
        <div className="team-score">
          <div className="header">Team Score: {calculateTeamScore()}</div>
        </div>

        <div className="transfer-suggestions">
          <div className="header2">Transfer Suggestions</div>
          <div className="info-container">
            <button className="increment-btn" onClick={() => handleFreeTransferIncrement(-1)}>-</button>
            <span className="transfer-input-container">
              <input
                className="transfer-input"
                type="number"
                value={freeTransfers}
                onChange={handleFreeTransferChange}
              />
            </span>
            <button className="increment-btn" onClick={() => handleFreeTransferIncrement(1)}>+</button>
            <span className="transfer-info" > Free Transfers</span>
          </div>
          <div className="info-container2">
            <button className="increment-btn" onClick={() => handleBudgetIncrement(-0.1)}>-</button>
            <span className="transfer-info2"> £ </span>
            <input
              className="budget-input"
              type="number"
              step="0.1"
              value={transferBudget}
              onChange={handleBudgetChange}
            />
            <span className="transfer-info2"> m </span>
            <button className="increment-btn" onClick={() => handleBudgetIncrement(0.1)}>+</button>
            <span className="transfer-info"> Budget Available</span>
          </div>
          <button className="get-transfers-btn" disabled={!isGetTransfersEnabled}>Get Transfers</button>
        </div>

        <div className="team">
          <div className="header2">Team</div>
          <div className="analytics-player-list">
            {selectedPlayers.map((player) => (
            <div
              key={player.id}
              className={
                selectedPlayers.find((p) => p.id === player.id) ? "selected" : ""
              }
            >
              {player.display_name} 
              <span className="player-team-display"> | {["GKP", "DEF", "MID", "FWD"][player.position - 1]} | {player.team}</span> 
            </div>
          ))}
          </div>
        </div>
      </div>
    );
  }

  const isFullTeam = isPickTeamMode && selectedPlayers.length == 15;

  return (
    <div className="right-column">
      <h2>Analytics</h2>
      {isFullTeam ? (
        <AnalyticsDisplay/>
      ) : (
        <p className="set-team-msg">'Set Team' to view analytics</p>
      )}
    </div>
  );
}

export default Analytics;