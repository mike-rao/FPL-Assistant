// frontend/src/App.js
import React, { useState, useEffect } from "react";
import "./styles/App.css";

function App() {
  const [playerData, setPlayerData] = useState([]);
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [filter, setFilter] = useState("Global");
  const [searchTerm, setSearchTerm] = useState("");

  const API_BASE_URL =
    process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/get_player_data`);
        const data = await response.json();
        setPlayerData(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [API_BASE_URL]);

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
    if (filter !== "Global" && filter !== position) {
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
    <div className="App">
      <h1>Fantasy Premier League Assistant</h1>

      <div className="columns">
        <div className="left-column">
          <h2>Player Selection</h2>
          <div>
            <select value={filter} onChange={handleFilterChange}>
              <option value="Global">Global</option>
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
                  selectedPlayers.find((p) => p.id === player.id)
                    ? "selected"
                    : ""
                }
              >
                {player.first_name} {player.second_name}
              </div>
            ))}
          </div>
        </div>

        <div className="middle-column">
          <h2>Team Formation</h2>
          <div className="formation">
            {/* Goalkeeper */}
            <div
              className="player-slot"
              onClick={() =>
                handlePlayerSelect(
                  selectedPlayers.find((p) =>
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === "GKP",
                  ),
                )
              }
            >
              {selectedPlayers.find(
                (p) => ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === "GKP",
              )?.first_name || ""}
            </div>

            {/* Defenders */}
            {Array.from({ length: 4 }).map((_, index) => (
              <div
                key={index}
                className="player-slot"
                onClick={() =>
                  handlePlayerSelect(
                    selectedPlayers[
                      selectedPlayers.findIndex((p) =>
                        ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] ===
                        "DEF",
                      ) + index
                    ],
                  )
                }
              >
                {selectedPlayers[
                  selectedPlayers.findIndex((p) =>
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === "DEF",
                  ) + index
                ]?.first_name || ""}
              </div>
            ))}

            {/* Midfielders */}
            {Array.from({ length: 4 }).map((_, index) => (
              <div
                key={index}
                className="player-slot"
                onClick={() =>
                  handlePlayerSelect(
                    selectedPlayers[
                      selectedPlayers.findIndex((p) =>
                        ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] ===
                        "MID",
                      ) + index
                    ],
                  )
                }
              >
                {selectedPlayers[
                  selectedPlayers.findIndex((p) =>
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === "MID",
                  ) + index
                ]?.first_name || ""}
              </div>
            ))}

            {/* Attackers */}
            {Array.from({ length: 2 }).map((_, index) => (
              <div
                key={index}
                className="player-slot"
                onClick={() =>
                  handlePlayerSelect(
                    selectedPlayers[
                      selectedPlayers.findIndex((p) =>
                        ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] ===
                        "FWD",
                      ) + index
                    ],
                  )
                }
              >
                {selectedPlayers[
                  selectedPlayers.findIndex((p) =>
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === "FWD",
                  ) + index
                ]?.first_name || ""}
              </div>
            ))}

            {/* Substitutes */}
            {Array.from({ length: 4 }).map((_, index) => (
              <div
                key={index}
                className="player-slot"
                onClick={() =>
                  handlePlayerSelect(
                    selectedPlayers[
                      selectedPlayers.findIndex((p) =>
                        ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] !==
                        "FWD",
                      ) + index
                    ],
                  )
                }
              >
                {selectedPlayers[
                  selectedPlayers.findIndex((p) =>
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] !== "FWD",
                  ) + index
                ]?.first_name || ""}
              </div>
            ))}
          </div>
        </div>

        <div className="right-column">
          <h2>Transfers</h2>
          {/* ... content for future transfer suggestions ... */}
        </div>
      </div>
    </div>
  );
}

export default App;