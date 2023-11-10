# Tic Tac Toe Game

Tic tac toe game with Django, Rest API, Docker, CircleCI and Pytest

## Details

- Software
  - Version 1.0.0
  - The application is running in a Docker container and with a sqlite database
  - Documentation is running on `http://localhost:8000/swagger/`
- Game
  - The user win a points after a win
  - The user sum a new game played after the game finishes
  - The inital user joined to the game have the `X` mark and the second one the `O`. For this version is not possible to modify.

## Instructions

- Have Docker installed
- Run `docker compose build` to create the container
- Run `docker compose up` to run the application
- Go to `http://localhost:8000/` to run the application

## Endpoints

- `swagger/`: To see the documentation with more details
- `games/`
  - `GET`: List all games and optional filter by available games (Using a query param `?status=waiting`)
  - `POST`: Create a game. User is created also, if the user sent it does not exist
- `games/<str:name>`
  - `GET`: Retrieve a game instance
  - `PUT`: Add a new user to the game. If the game is filled it starts
- `games/<str:name>/play`
  - `GET`: Get the actual game details
  - `POST`: Play the game making a movement
- `users/`
  - `POST`: Register a new User
- `users/<str:username>/`
  - `GET`: Login User and get user data with the games played

## How to play

- `users/`: Register the both users
- `games/` POST: Create the game
- `games/<str:name>` PUT: Join the second user to the game
- `games/<str:name>/play` POST: Make the movements one player and the other until the game finishes and return the final data
- `users/<str:username>/` GET: In the profile you can check your points, number of games, and list of games played

## Future improvements

- Change to an SQL database in the cloud or in a server
- Add authorization system by OAuth or by external integrations like google
- Frontend
  - Create the frontend to handle communication and show a better visualization
  - In frontend, we can update (by events) when the other player makes the movement to continue the game smoothly
- Logics
  - Add `id` for user and handle with more user data for the profile
  - Add logs of the games. For this, we need to save that in the database linked to the actual models
  - Add the possibility of selecting the mark that the user wants to be (X or O)
