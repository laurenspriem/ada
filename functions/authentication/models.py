import sqlalchemy as sa

from db import Base


class User(Base):
    __tablename__ = "user"

    username = sa.Column(sa.String, primary_key=True)
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    is_verified = sa.Column(sa.Boolean, nullable=False)
    created_on = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
    )
    updated_on = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )

    profile_id = sa.Column(sa.Integer, nullable=False)
    notificationsettings_id = sa.Column(sa.Integer, nullable=False)
    shippinginfo_id = sa.Column(sa.Integer, nullable=False)
    paymentinfo_id = sa.Column(sa.Integer, nullable=False)

    def to_dict(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "is_verified": self.is_verified,
            "profile": self.profile_id,
            "notificationsettings": self.notificationsettings_id,
            "shippinginfo": self.shippinginfo_id,
            "paymentinfo": self.paymentinfo_id,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }
