import flask_script

import minesweeper.app

app = minesweeper.app.create_app()
manager = flask_script.Manager(app)

manager.add_command("runserver", flask_script.Server("0.0.0.0", threaded=True))

if __name__ == '__main__':
    manager.run()
