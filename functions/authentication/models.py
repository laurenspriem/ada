# pylint: disable=import-error
from db import db


class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
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
            "username": self.name,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }
