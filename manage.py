import flask_script
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
manager = flask_script.Manager(app)

manager.add_command("runserver", flask_script.Server("0.0.0.0", threaded=True))
manager.add_command("shell", flask_script.Shell(make_context=make_app_context))


@manager.command
def create_db():
    if not database_exists(minesweeper.config.Config.SQLALCHEMY_DATABASE_URI):
        create_database(minesweeper.config.Config.SQLALCHEMY_DATABASE_URI)
        with app.app_context():
            minesweeper.extensions.db.create_all()


if __name__ == '__main__':
    manager.run()
