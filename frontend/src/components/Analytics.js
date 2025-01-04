import React, { useState, useEffect } from "react";
import "../styles/Analytics.css";
import jerseyImages from '../helpers/jerseyImages';
import {showPlayerInfo} from "./TeamFormation";

function Analytics({ selectedPlayers, setSelectedPlayers, isPickTeamMode }) {
  const [freeTransfers, setFreeTransfers] = useState(0);
  const [transferBudget, setTransferBudget] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [gotTransfers, setGotTransfers] = useState(false);
  const [isFirstPage, setIsFirstPage] = useState(true);
  const [playersWithXpts, setplayersWithXpts] = useState([]);
  const [transfers, setTransfers] = useState([]);

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

  useEffect(() => {
    const fetchXpts = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/predict-pts`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ players: selectedPlayers }),
        });
        const data = await response.json();
        setplayersWithXpts(data);
      } catch (error) {
        console.error("Error fetching predicted player pts:", error);
      }
    };

    if (selectedPlayers.length > 0) {
      fetchXpts();
    }
  }, [selectedPlayers, API_BASE_URL]);

  const getTransfers = async () => {
    setIsLoading(true);
    setGotTransfers(true);
    setTransfers([]);
    try {
      const response = await fetch(`${API_BASE_URL}/suggest-transfers`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          current_team: selectedPlayers,
          free_transfers: freeTransfers,
          transfer_budget: transferBudget,
        }),
      });
      if (!response.ok) {
        throw new Error("Failed to fetch transfer suggestions.");
      }
      const data = await response.json();
      setTransfers(data);
    } catch (error) {
      console.error("Error fetching transfer suggestions:", error);
    } finally {
      setIsLoading(false);
    }
  };

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

  const handlePageBtnClick = () => {
    setIsFirstPage(!isFirstPage);
  }

  const handleTransferAccept = (player_in, player_out) => {
    setSelectedPlayers((prevPlayers) =>
      prevPlayers.map((player) =>
        player.name === player_out.name ? player_in : player
      )
    );
    setplayersWithXpts((prevPlayers) =>
      prevPlayers.map((player) =>
        player.name === player_out.name ? player_in : player
      )
    );
    setTransfers((prevSuggestions) =>
      prevSuggestions.filter(
        (suggestion) =>
          suggestion.transfer_in.name !== player_in.name ||
          suggestion.transfer_out.name !== player_out.name
      )
    );
  }

  const getJerseyImage = (player) => {
    if (!player) return jerseyImages['Unknown'];
    if (player.position === 1 || player.position === "Goalkeeper") {
      return jerseyImages['Goalkeeper'] || jerseyImages['Unknown Goalkeeper'];
    }
    return jerseyImages[player.team] || jerseyImages['Unknown'];
  };

  const isGetTransfersEnabled = freeTransfers > 0 && transferBudget >= 0;

  const calculateTeamXpts = () => {
    return (playersWithXpts.slice(0,11).reduce((sum, player) => sum + (player.xpts || 0), 0) * 10/11).toFixed(2);
  };

  const isFullTeam = isPickTeamMode && selectedPlayers.length === 15;

  if (!isFullTeam && gotTransfers) {
    setGotTransfers(false);
    setIsFirstPage(true);
  }
  if (!isFullTeam && freeTransfers > 0) {
    setFreeTransfers(0);
  }
  if (!isFullTeam && transferBudget > 0) {
    setTransferBudget(0);
  }

  const Transfer = ({ players, index }) => {
    return (
      <div className="transfer">
        <div className="transfer-name">{index}. {players.transfer_in.display_name}</div>
        <div className="transfer-body">
          <div className="transfer-container">
            <div className="player-slot transfer-out" onClick={() => {showPlayerInfo(players.transfer_out);}}>
              <div className="player-slot-top">
                <div className="player-price">£{players.transfer_out.price}m</div>
              </div>
              <img 
                src={getJerseyImage(players.transfer_out)} 
                alt={`${players?.transfer_out.team || "Unknown"} jersey`} 
                className="player-jersey" 
              />
              <span className="player-name">{players.transfer_out.display_name}</span>
              <span className = "player-team">{players.transfer_out.team}</span>
            </div>
            <div className="transfer-score">x{players.transfer_out.predicted_points.toFixed(2)}</div>
          </div>
          <div className="switch-icon">
            <div>{"→"}</div>
          </div>
          <div className="transfer-container">
            <div className="player-slot transfer-in" onClick={() => {showPlayerInfo(players.transfer_in);}}>
              <div className="player-slot-top">
                <div className="player-price">£{players.transfer_in.price}m</div>
              </div>
              <img 
                src={getJerseyImage(players.transfer_in)} 
                alt={`${players?.transfer_in.team || "Unknown"} jersey`} 
                className="player-jersey" 
              />
              <span className="player-name">{players.transfer_in.display_name}</span>
              <span className = "player-team">{players.transfer_in.team}</span>
            </div>
            <div className="transfer-score">x{players.transfer_in.predicted_points.toFixed(2)}</div>
          </div>
        </div>
        <div className="accept-btn-container">
          <button className="accept-btn orange-hover" onClick={() => handleTransferAccept(players.transfer_in, players.transfer_out)}>Accept</button>
        </div>
      </div>
    );
  }

  const AnalyticsDisplay = ({}) => {
    return (
      <div>
        <div className="team-score">
          <div className="header">Expected Team Points: x{calculateTeamXpts()}</div>
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
            <button className="get-transfers-btn orange-hover" disabled={!isGetTransfersEnabled} onClick={getTransfers}>
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
                  {transfers.map((transfer, index) => (
                    <Transfer players={transfer} index={index+1}/>
                  ))}
                </div>
                <div className="page-btn-container">
                  <button className="page-button back-btn" disabled={isFirstPage} onClick={handlePageBtnClick}><span>&lt;</span></button>
                  <button className="page-button forward-btn" disabled={!isFirstPage} onClick={handlePageBtnClick}><span>&gt;</span></button>
                </div>
              </div>
            }
          </div>
        }

        {(!gotTransfers || !isFirstPage) && 
          <div className="team">
            <div className="header2">Expected Points</div>
            <div className={`analytics-player-list ${isFirstPage ? "" : "page-two-team"} `} >
              {playersWithXpts.map((player, index) => (
                <div key={player.id} onClick={() => {showPlayerInfo(player);}}>
                  <div>
                    {index + 1}. {player.display_name}
                    <span className="player-team-display">
                      {" "}
                      | {["GKP", "DEF", "MID", "FWD"][player.position - 1]}
                    </span>
                  </div>
                  <span className="player-xpts">x{player.xpts.toFixed(2)}</span>
                </div>
              ))}
            </div>
            {!isFirstPage &&
              <div className="page-btn-container">
                <button className="page-button back-btn" disabled={isFirstPage} onClick={handlePageBtnClick}><span>&lt;</span></button>
                <button className="page-button forward-btn" disabled={!isFirstPage} onClick={handlePageBtnClick}><span>&gt;</span></button>
              </div>
            }
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