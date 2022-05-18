import sqlalchemy as sa

from db import Base


class Model(Base):
    __tablename__ = "models"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    field = sa.Column(sa.String, nullable=False)
    created_on = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
    )
    updated_on = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "field": self.field,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }
