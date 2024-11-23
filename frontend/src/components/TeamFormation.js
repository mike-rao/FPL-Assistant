import React from "react";
import "../styles/TeamFormation.css";

function TeamFormation({ selectedPlayers, setSelectedPlayers }) {
  const handlePlayerSelect = (player) => {
    if (selectedPlayers.find((p) => p.id === player.id)) {
      setSelectedPlayers(selectedPlayers.filter((p) => p.id !== player.id));
    }
  };

  return (
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
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === "DEF",
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
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === "MID",
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
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] === "FWD",
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
                    ["GKP", "DEF", "MID", "FWD"][p.element_type - 1] !== "FWD",
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
  );
}

export default TeamFormation;