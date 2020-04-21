import flask_script
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils import create_database, database_exists

import minesweeper.app
import minesweeper.config
import minesweeper.extensions
import minesweeper.models


def make_app_context():
    return {
        "app": minesweeper.app,
        "db": minesweeper.extensions.db
    }


app = minesweeper.app.create_app()
migrate = Migrate(app, minesweeper.extensions.db)
manager = flask_script.Manager(app)

manager.add_command("runserver", flask_script.Server("0.0.0.0", threaded=True))
manager.add_command("shell", flask_script.Shell(make_context=make_app_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
