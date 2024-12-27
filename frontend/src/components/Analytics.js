import React, { useState } from "react";
import "../styles/Analytics.css";
import jerseyImages from '../helpers/jerseyImages';

function Analytics({ selectedPlayers, isPickTeamMode }) {
  const [freeTransfers, setFreeTransfers] = useState(0);
  const [transferBudget, setTransferBudget] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [gotTransfers, setGotTransfers] = useState(false);
  const [isFirstPage, setIsFirstPage] = useState(true);

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

  const handleGetTransfersClick = () => {
    setGotTransfers(true);
    setIsLoading(true);
    // Simulate a delay (e.g., making an API call)
    setTimeout(() => {
      setIsLoading(false); // Hide "Loading..." after 2 seconds
    }, 2000);
  };

  const handlePageBtnClick = () => {
    setIsFirstPage(!isFirstPage);
  }

  const getJerseyImage = (player) => {
    if (!player) return jerseyImages['Unknown'];
    if (player.position === 1) {
      return jerseyImages['Goalkeeper'] || jerseyImages['Unknown Goalkeeper'];
    }
    return jerseyImages[player.team] || jerseyImages['Unknown'];
  };

  const isGetTransfersEnabled = freeTransfers > 0 && transferBudget >= 0;

  const calculateTeamScore = () => {
    // Calculate the total score of selectedPlayers (replace with your logic)
    return selectedPlayers.reduce((sum, player) => sum + player.score, 0); 
  };

  const isFullTeam = isPickTeamMode && selectedPlayers.length === 15;

  if (!isFullTeam && gotTransfers) {
    setGotTransfers(false);
    setIsFirstPage(true);
  }

  const Transfer = ({}) => {
    return (
      <div className="transfer">
        <div className="transfer-name">1. Unknown</div>
        <div className="transfer-body">
          <div className="transfer-container">
            <div className="player-slot transfer-out">
              <div className="player-slot-top">
                <div className="player-price">£ ? m</div>
              </div>
              <img 
                src={getJerseyImage()} 
                alt="Unknown jersey" 
                className="player-jersey" 
              />
              <span className="player-name">Unknown</span>
              <span className = "player-team">Unknown</span>
            </div>
            <div className="transfer-score">50%</div>
          </div>
          <div className="switch-icon">
            <div>{"-->"}</div>
          </div>
          <div className="transfer-container">
            <div className="player-slot transfer-in">
              <div className="player-slot-top">
                <div className="player-price">£ ? m</div>
              </div>
              <img 
                src={getJerseyImage()} 
                alt="Unknown jersey" 
                className="player-jersey" 
              />
              <span className="player-name">Unknown</span>
              <span className = "player-team">Unknown</span>
            </div>
            <div className="transfer-score">100%</div>
          </div>
        </div>
      </div>
    );
  }

  const AnalyticsDisplay = ({}) => {
    return (
      <div>
        <div className="team-score">
          <div className="header">Team Score: {calculateTeamScore()}</div>
        </div>

        {isFirstPage && 
          <div className="transfer-suggestions">
            <div className="header2">Transfer Suggestions</div>
            <div className="info-container">
              <button className="increment-btn orange-hover" onClick={() => handleFreeTransferIncrement(-1)}>-</button>
              <span className="transfer-input-container">
                <input
                  className="transfer-input"
                  type="number"
                  value={freeTransfers}
                  onChange={handleFreeTransferChange}
                />
              </span>
              <button className="increment-btn orange-hover" onClick={() => handleFreeTransferIncrement(1)}>+</button>
              <span className="transfer-info" > Free Transfers</span>
            </div>
            <div className="info-container2">
              <button className="increment-btn orange-hover" onClick={() => handleBudgetIncrement(-0.1)}>-</button>
              <span className="transfer-info2"> £ </span>
              <input
                className="budget-input"
                type="number"
                step="0.1"
                value={transferBudget}
                onChange={handleBudgetChange}
              />
              <span className="transfer-info2"> m </span>
              <button className="increment-btn orange-hover" onClick={() => handleBudgetIncrement(0.1)}>+</button>
              <span className="transfer-info"> Budget Available</span>
            </div>
            <button className="get-transfers-btn orange-hover" disabled={!isGetTransfersEnabled} onClick={handleGetTransfersClick}>
              Get Transfers
            </button>
            {isLoading && 
              <div className="loading-container">
                <div className="loader__btn">
                  <div className="loader"></div>
                  Loading...
                </div>
              </div>
            }
            {gotTransfers && !isLoading &&
              <div className="transfers">
                <div className="transfer-list">
                  <Transfer/>
                  <Transfer/>
                  <Transfer/>
                  <Transfer/>
                  <Transfer/>
                </div>
                <div className="page-btn-container">
                  <button className="page-button back-btn" disabled={isFirstPage} onClick={handlePageBtnClick}><span>&lt;</span></button>
                  <button className="page-button forward-btn" disabled={!isFirstPage} onClick={handlePageBtnClick}><span>&gt;</span></button>
                </div>
              </div>
            }
          </div>
        }

        {!gotTransfers || !isFirstPage && 
          <div className="team">
            <div className="header2">Player Ratings</div>
            <div className={`analytics-player-list ${isFirstPage ? "" : "page-two-team"} `} >
              {selectedPlayers.map((player) => (
                <div>
                  <div
                    key={player.id}
                    className={
                      selectedPlayers.find((p) => p.id === player.id) ? "selected" : ""
                    }
                  >
                    {player.display_name} 
                    <span className="player-team-display"> | {["GKP", "DEF", "MID", "FWD"][player.position - 1]} | {player.team}</span> 
                  </div>
                </div>
              ))}
            </div>
            <div className="page-btn-container">
              <button className="page-button back-btn" disabled={isFirstPage} onClick={handlePageBtnClick}><span>&lt;</span></button>
              <button className="page-button forward-btn" disabled={!isFirstPage} onClick={handlePageBtnClick}><span>&gt;</span></button>
            </div>
          </div>
        }
      </div>
    );
  }

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