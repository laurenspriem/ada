import flask

from flask import Blueprint

from account.interactions import AccountInteractions


resources = Blueprint("api", __name__, url_prefix="/api")


def account_interactions():
    return AccountInteractions(**flask.current_app.repositories)


@resources.route("/users", methods=["POST"])
def create_user():
    return account_interactions().create(flask.request.json)


@resources.route("/users/<d_username>", methods=["GET"])
def get_user(d_username):
    return account_interactions().get(d_username).to_dict()


@resources.route("/users/<d_username>", methods=["PUT"])
def update_user(d_username):
    return account_interactions().update(d_username, flask.request.json).to_dict()


@resources.route("/users/<d_username>", methods=["DELETE"])
def delete_user(d_username):
    account_interactions().delete(d_username)

    return "", 204


# Update a user profile
@resources.route("/users/<d_username>/profile", methods=["PUT"])
def update_profile(d_username):
    return (
        account_interactions().update_profile(d_username, flask.request.json).to_dict()
    )


# Update a user shipping information
@resources.route("/users/<d_username>/shippinginfo", methods=["PUT"])
def update_shippinginfo(d_username):
    return (
        account_interactions()
        .update_shippinginfo(d_username, flask.request.json)
        .to_dict()
    )


# Update a user notification settings
@resources.route("/users/<d_username>/notificationsettings", methods=["PUT"])
def update_notificationsettings(d_username):
    return (
        account_interactions()
        .update_notificationsettings(d_username, flask.request.json)
        .to_dict()
    )


# Update a user payment info
@resources.route("/users/<d_username>/paymentinfo", methods=["PUT"])
def update_paymentinfo(d_username):
    return (
        account_interactions()
        .update_paymentinfo(d_username, flask.request.json)
        .to_dict()
    )
