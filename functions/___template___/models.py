# pylint: disable=import-error
from db import db


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field = db.Column(db.String, nullable=False)
    created_on = db.Column(
        db.DateTime,
        server_default=db.func.now(),
    )
    updated_on = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "field": self.field,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }
