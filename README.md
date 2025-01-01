# Fantasy Premier League (FPL) Assistant

## Development Overview

The Fantasy Premier League (FPL) Assistant project is a comprehensive web application designed to enhance decision-making for FPL players. The app combines frontend and backend technologies with machine learning to predict player performance, suggest optimal transfers, and assist in team management. This project leverages modern development technologies, including React for the frontend, Flask for the backend API, and a PostgreSQL database for data storage and retrieval.

## Frontend Development

The frontend of the FPL Assistant is built using React, a JavaScript library for creating dynamic and interactive user interfaces. The UI includes components that: 
- Displays all players fetched from the database, allowing users to view and select players for their team. 
- Provides a visual representation of the selected team in formation, enabling users to arrange players by position.
- Shows analytical insights about the selected team, including metrics like team score and transfer suggestions.
- Suggests potential player transfers to improve team performance based on predicted points and budget constraints.

## Backend Development

The backend is implemented using Flask, a Python microframework. It provides RESTful API endpoints to handle web scraping, machine learning predictions, and database operations. Key API functionalities include:
- Scraping Player Stats - the /scrape-and-save endpoint scrapes FPL player statistics from the official premier league website and stores them in the database
- Fetching Players - the /players endpoint retrieves player data from the database for frontend display.
- Predicting Player Points - the /predict-pts endpoint predicts the amount of points a player will score the next week using a machine learning model trained on player statistics.
- Generating Transfers - the /suggest-transfers endpoint calculates optimal transfer suggestions based on an algorithm to bring in the best net of predicted points.

## Database Integration

The PostgreSQL database serves as the backbone for storing and retrieving player data. Tables are structured to hold player attributes such as name, position, team, price, form, and predicted points. SQLAlchemy, a Python ORM, facilitates seamless database interaction, ensuring efficiency and maintainability.

## Machine Learning Integration

A machine learning model is implemented to predict weekly FPL points for players based on historical data. Features include:
- Input Variables - player form, fixture difficulty rating (FDR), points per match, total points, ICT (impact creativity and threat) index, and team selected by percentage.
- Target Variable - points scored in the upcoming gameweek.
- Algorithm - a Random Forest Regressor, chosen for its ability to handle complex relationships and feature importance.
The model is trained on historical player data scraped from the Premier League website and stored in the PostgreSQL database. Predictions are generated using the trained model during transfer calculations, helping users optimize their team lineup.


This development approach combines robust technology stacks with thoughtful design and user-centric features to create a powerful assistant for FPL players.