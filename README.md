# Minesweeper API
API to play the classic game Minesweeper.

## About the Challenge:
- Support mark flags, question and rollback to unknown (only if the cell was marked and is not discovered)
- API clients can track the elapsed time because the game has the datetime created in UTC timestamp (the client should make the difference with their current UTC timestamp)
- When you discover a cell without adjacent mines, the adjacents cells are revelead (recursivesly)
- You can create your board like you want. It handle error cases (For instance if you want to create a board with more mines than cells)
- You can be resume whenever you want if it is still in progress
- You can see all the games played regardless if it is finished or not (Persistence)
- The game finishes when you discover a cell with mine or the only undiscovered cells (also mark as flag) are the cells with mines (if you have marked a cell with a question mark the game doesn't finish)
### Considerations
- User/accounts wasn't implemented because it would take so much time. The implementation of this would be with user table and creating jwt tokens when the user logged in. So the user should send the JWT in each request and the backend should check if the token is valid and not expired
- Extract the game in a API library could be done making a distribute package with the `models`, `services` and `GameErros`, then it must receive the DB client from the consumers clients. It haven't been done because it would take more time to make the refactor
- A tool file was create to interact directly with the backend



## Setup
- Export ENV environment variable running the command: `export ENV=local`
- Export DATABASE_URL environment variable running the command line: `export DATABASE_URL={URI_TO_YOUR_DB}`
    > Note: Replace `{URI_TO_YOUR_DB}` by some DB Uri that you have access
- Create a new python virtual environment and init it
- Run the command: `pip install -r requirements.txt`
- Create the DB Model running the following commands:
    - `python manage.py db init`
    - `python manage.py db migrate`
    - `python manage.py db upgrade`

## Run the server
- Since your virtualenv is installed and the project setted up, you can run the Server executing the following command line:
    - `python manage.py runserver`
        - Note: Make sure that you exported the `ENV` and `DATABASE_URL` environment variables

## API
> NOTE: {{domain}} should be replaced by `https://mluksenberg-minesweeper.herokuapp.com` if you want to play online or `http://localhost:5000` if you are running the localserver and you want to play offline
Create a new Game:
- [POST] {{domain}}/api/game
    - json body: `{"mines": minesSize, "width": widthSize, "height": heightSize}`
        - NOTE: Either `minesSize`, `widthSize` and `heightSize` are INT values

Get All Games:
- [GET] {{domain}}/api/game?status={{status}}
    - `status`: [OPTIONAL] filter the games storages by status. It takes the values `IN_PROGRESS`, `WIN`, `LOST`

Get Game By ID
- [GET] {{domain}}/api/game/{{GAME_ID}}
    - `{{GAME_ID}}`: INT value
    
Delete Game By ID
- [DELETE] {{domain}}/api/game/{{GAME_ID}}

Make Action on Cell
- [PUT] {{domain}}/api/game/{{GAME_ID}}
    - json body: `{"coordinate_x": posX, "coordinate_y": posY, "action": actionCell}`
        - posX: INT value
        - posY: INT value
        - actionCell: STRING value. One of `DISCOVER`, `MARK_FLAG`, `MARK_QUESTION`, `MARK_UNKNOWN`

You can import [POSTMAN Collection](https://www.getpostman.com/collections/97d8676147ff8e4b8691) with all URL


## Sample usages:
- [POST] https://mluksenberg-minesweeper.herokuapp.com/api/game
    - body: {"mines": 5, "width": 6, "height": 10}
- [GET] https://mluksenberg-minesweeper.herokuapp.com/api/game
- [GET] https://mluksenberg-minesweeper.herokuapp.com/api/game/6
- [GET] https://mluksenberg-minesweeper.herokuapp.com/api/game?status=IN_PROGRESS
- [DELETE] https://mluksenberg-minesweeper.herokuapp.com/api/game/1
- [PUT] https://mluksenberg-minesweeper.herokuapp.com/api/game/6
    - body {"coordinate_x": 0, "coordinate_y": 1, "action": "DISCOVER"}
- [PUT] https://mluksenberg-minesweeper.herokuapp.com/api/game/6
    - body {"coordinate_x": 5, "coordinate_y": 6, "action": "MARK_FLAG"}
- [PUT] https://mluksenberg-minesweeper.herokuapp.com/api/game/6
    - body {"coordinate_x": 15, "coordinate_y": 12, "action": "MARK_QUESTION"}
- [PUT] https://mluksenberg-minesweeper.herokuapp.com/api/game/6
    - body {"coordinate_x": 15, "coordinate_y": 12, "action": "MARK_UNKNOWN"}
    
## Tool to interact with the API
There is a filename `tool.py` which can interact with the API (either local or dev) by commandline. You can see the help usage running the command: `python tool.py --help`
### Some usage examples:
```
- python tool.py -d -e dev create-game 5 6 10
- python tool.py -d -e dev show-games
- python tool.py -d -e dev show-board 6
- python tool.py -d -e dev discover-cell 4 2 2
- python tool.py -d -e dev set-flag 4 2 1
- python tool.py -d -e dev set-unknown 4 2 1
- python tool.py -d -e dev set-question 4 2 1
```