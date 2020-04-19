import flask_marshmallow
import flask_sqlalchemy

import minesweeper.models.base

db = flask_sqlalchemy.SQLAlchemy(model_class=minesweeper.models.base.BaseModel)
marshmallow = flask_marshmallow.Marshmallow()
