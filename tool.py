from pip._vendor import requests


def draw_board():
    response = requests.get("http://localhost:5000/api/game/4").json()
    cells = response.get("board")
    sorted(cells, key="coordinate_y")
    for cell in cells:
        print(" * ")


if __name__ == '__main__':
    draw_board()