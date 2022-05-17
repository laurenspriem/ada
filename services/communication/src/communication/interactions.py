from communication.models import Chat, Message


class CommunicationInteractions:
    def __init__(self, **repositories):
        self._database_repository = repositories["database_repository"]
        self._pubsub_repository = repositories["pubsub_repository"]
        self._web_repository = repositories["web_repository"]

    def get_chat(self, chat_id):
        return self._database_repository.get_chat(int(chat_id)).to_dict()

    def get_message(self, message_id):
        return self._database_repository.get_message(int(message_id)).to_dict()

    def get_chats_for_user(self, user_id):
        return [
            c.to_dict()
            for c in self._database_repository.get_chats_for_user(int(user_id))
        ]

    def create_chat(self, data):
        chat = Chat(
            participant_1_id=data["participant_1_id"],
            participant_2_id=data["participant_2_id"],
            item_id=data["item_id"],
        )

        return self._database_repository.create_chat(chat).to_dict()

    def create_text_message(self, chat_id, data):
        chat = self._database_repository.get_chat(int(chat_id))
        message = Message(text=data["text"], image=None)

        message = self._database_repository.create_message(chat, message).to_dict()

        self._pubsub_repository.push(
            self._pubsub_repository.MESSAGE_SEND_TOPIC,
            message,
        )

        return message

    def create_picture_message(self, chat_id, file):
        chat = self._database_repository.get_chat(int(chat_id))
        picture = self._web_repository.upload_picture(file)
        message = Message(image=picture["url"])

        message = self._database_repository.create_message(chat, message).to_dict()

        self._pubsub_repository.push(
            self._pubsub_repository.MESSAGE_SEND_TOPIC,
            message,
        )

        return message

    def delete_chat(self, chat_id):
        return self._database_repository.delete_chat(int(chat_id))

    def pull_item_update_topic(self):
        messages = self._pubsub_repository.pull(
            self._pubsub_repository.ITEM_UPDATE_TOPIC,
        )

        for message in messages:
            chats = self._database_repository.get_chats_for_item(
                message["id"],  # TODO(tomdewildt): update keys
            )
            for chat in chats:
                message = Message(text="System: Item updated.")

                message = self._database_repository.create_message(
                    chat,
                    message,
                ).to_dict()

                self._pubsub_repository.push(
                    self._pubsub_repository.MESSAGE_SEND_TOPIC,
                    message,
                )

    def pull_offer_accepted_topic(self):
        messages = self._pubsub_repository.pull(
            self._pubsub_repository.OFFER_ACCEPTED_TOPIC,
        )

        for message in messages:
            chats = self._database_repository.get_chats_for_item_and_user(
                message["item_id"],  # TODO(tomdewildt): update keys
                message["user_id"],  # TODO(tomdewildt): update keys
            )
            for chat in chats:
                message = Message(text="System: Offer accepted.")

                message = self._database_repository.create_message(
                    chat,
                    message,
                ).to_dict()

                self._pubsub_repository.push(
                    self._pubsub_repository.MESSAGE_SEND_TOPIC,
                    message,
                )

    def pull_user_blocked_topic(self):
        messages = self._pubsub_repository.pull(
            self._pubsub_repository.USER_BLOCKED_TOPIC,
        )

        for message in messages:
            chats = self._database_repository.get_chats_for_user(
                message["id"],  # TODO(tomdewildt): update keys
            )
            for chat in chats:
                self._database_repository.delete_chat(chat.id)
