import flask

from flask import Blueprint, jsonify

from communication.interactions import CommunicationInteractions


resources = Blueprint("api", __name__, url_prefix="/api")


def communication_interactions():
    return CommunicationInteractions(**flask.current_app.repositories)


@resources.route("/chats/<chat_id>", methods=["GET"])
def get_chat(chat_id):
    return communication_interactions().get_chat(chat_id)


@resources.route("/chats/user/<user_id>", methods=["GET"])
def get_chats_for_user(user_id):
    return jsonify(communication_interactions().get_chats_for_user(user_id))


@resources.route("/chats/", methods=["POST"])
def create_chat():
    return communication_interactions().create_chat(flask.request.json)


@resources.route("/chats/<chat_id>", methods=["POST"])
def create_message(chat_id):
    if flask.request.content_type and flask.request.content_type.startswith(
        "application/json"
    ):
        return communication_interactions().create_text_message(
            chat_id,
            flask.request.json,
        )

    if flask.request.content_type and flask.request.content_type.startswith(
        "multipart/form-data"
    ):
        return communication_interactions().create_picture_message(
            chat_id,
            flask.request.files.get("file"),
        )

    return {"message": "Invalid content type"}, 400


@resources.route("/chats/<chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    communication_interactions().delete_chat(chat_id)

    return "", 204
