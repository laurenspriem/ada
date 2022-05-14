import sqlalchemy as sa

from account.db import Base


class NotificationSettings(Base):
    __tablename__ = "notificationsettings"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    item_notifications_enabled = sa.Column(sa.Boolean, nullable=False, default=True)
    bids_notifications_enabled = sa.Column(sa.Boolean, nullable=False, default=True)
    chat_notifications_enabled = sa.Column(sa.Boolean, nullable=False, default=True)
    news_notifications_enabled = sa.Column(sa.Boolean, nullable=False, default=True)
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
            "item_notifications_enabled": self.item_notifications_enabled,
            "bids_notifications_enabled": self.bids_notifications_enabled,
            "chat_notifications_enabled": self.chat_notifications_enabled,
            "news_notifications_enabled": self.news_notifications_enabled,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }


class PaymentInfo(Base):
    __tablename__ = "paymentinfo"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    iban = sa.Column(sa.String, nullable=True)
    name = sa.Column(sa.String, nullable=True)
    bank = sa.Column(sa.String, nullable=True)
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
            "iban": self.iban,
            "name": self.name,
            "bank": self.bank,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }


class Profile(Base):
    __tablename__ = "profile"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    birthday = sa.Column(sa.String, nullable=True)
    gender = sa.Column(sa.String, nullable=True)
    height = sa.Column(sa.String, nullable=True)
    shirt_size = sa.Column(sa.String, nullable=True)
    jeans_size = sa.Column(sa.String, nullable=True)
    shoe_size = sa.Column(sa.String, nullable=True)
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
            "birthday": self.birthday,
            "gender": self.gender,
            "height": self.height,
            "shirt_size": self.shirt_size,
            "jeans_size": self.jeans_size,
            "shoe_size": self.shoe_size,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }


class ShippingInfo(Base):
    __tablename__ = "shippinginfo"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    street = sa.Column(sa.String, nullable=True)
    street_number = sa.Column(sa.String, nullable=True)
    zip_code = sa.Column(sa.String, nullable=True)
    city = sa.Column(sa.String, nullable=True)
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
            "street": self.street,
            "street_number": self.street_number,
            "zip_code": self.zip_code,
            "city": self.city,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }


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

    # Relationship to profile
    profile_id = sa.Column(sa.Integer, sa.ForeignKey("profile.id"))
    profile = sa.orm.relationship(
        Profile.__name__,
        backref=sa.orm.backref("user", uselist=False),
    )

    # Relationship to notification settings
    notificationsettings_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("notificationsettings.id"),
    )
    notificationsettings = sa.orm.relationship(
        NotificationSettings.__name__,
        backref=sa.orm.backref("user", uselist=False),
    )

    # Relationship to shipping information
    shippinginfo_id = sa.Column(sa.Integer, sa.ForeignKey("shippinginfo.id"))
    shippinginfo = sa.orm.relationship(
        ShippingInfo.__name__,
        backref=sa.orm.backref("user", uselist=False),
    )

    # Relationship to payment information
    paymentinfo_id = sa.Column(sa.Integer, sa.ForeignKey("paymentinfo.id"))
    paymentinfo = sa.orm.relationship(
        PaymentInfo.__name__,
        backref=sa.orm.backref("user", uselist=False),
    )

    def to_dict(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "is_verified": self.is_verified,
            "profile": self.profile.to_dict(),
            "notificationsettings": self.notificationsettings.to_dict(),
            "shippinginfo": self.shippinginfo.to_dict(),
            "paymentinfo": self.paymentinfo.to_dict(),
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }
