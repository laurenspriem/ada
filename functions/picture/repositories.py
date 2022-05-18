import hashlib

from models import Metadata


class NotFoundError(Exception):
    pass


class MetadataRepository:
    def __init__(self, session):
        self._session = session

    def get_metadata(self, metadata_id):
        metadata = self._session.query(Metadata).get(metadata_id)
        if not metadata:
            raise NotFoundError()

        return metadata

    def store_metadata(self, metadata):
        self._session.add(metadata)
        self._session.commit()

        return metadata


class StorageRepository:
    def __init__(self, client, bucket):
        self._bucket = client.bucket(bucket)
        self._client = client

    def store_file(self, file):
        content = file.read()
        digest = hashlib.md5(content).hexdigest()
        extension = file.filename.split(".")[-1]
        file.seek(0)

        name = f"{digest}.{extension}"

        blob = self._bucket.blob(name)
        blob.upload_from_file(file, content_type=file.mimetype)
        blob.make_public()

        return name, blob.public_url
