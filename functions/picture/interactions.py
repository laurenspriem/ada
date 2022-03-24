# pylint: disable=import-error
from models import Metadata


class PictureInteractions:
    def __init__(self, metadata_repository, storage_repository):
        self._metadata_repository = metadata_repository
        self._storage_repository = storage_repository

    def upload(self, file):
        name, url = self._storage_repository.store_file(file)
        metadata = Metadata(name=name, url=url)

        return self._metadata_repository.store_metadata(metadata).to_dict()

    def download(self, metadata_id):
        return self._metadata_repository.get_metadata(metadata_id).to_dict()
