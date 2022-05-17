import sqlalchemy as sa

from communication.db import Base


class Message(Base):
    __tablename__ = "message"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text = sa.Column(sa.String, nullable=True)
    image = sa.Column(sa.String, nullable=True)
    chat_id = sa.Column(sa.Integer, sa.ForeignKey("chat.id"))
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
            "text": self.text,
            "image": self.image,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }


class Chat(Base):
    __tablename__ = "chat"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    participant_1_id = sa.Column(sa.Integer, nullable=False)
    participant_2_id = sa.Column(sa.Integer, nullable=False)
    item_id = sa.Column(sa.Integer, nullable=False)
    created_on = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
    )
    updated_on = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )

    # Relationship to message
    messages = sa.orm.relationship(
        Message.__name__,
        backref=sa.orm.backref("chat"),
        cascade="all,delete",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "participant_1_id": self.participant_1_id,
            "participant_2_id": self.participant_2_id,
            "item_id": self.item_id,
            "messages": [m.to_dict() for m in self.messages],
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }
