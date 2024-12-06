import os
import firebase_admin
from firebase_admin import credentials as firebase_crendentials, firestore
from loguru import logger
import json
from tqdm import tqdm
from slugify import slugify

from scrapers.constants.FilmAffinity import SLUG

CREDENTIALS_PATH = os.path.join(".", "firebase", "filmdatabase-firebase-adminsdk-do-not-publish.json")
WRITE_BATCH_SIZE = 10

COLLECTION = "all_films"

class Firestore:

    def __init__(self, collection: str = COLLECTION):
        self.client = self.__get_client()
        self.collection = collection

    def __get_client(self):
        credentials = firebase_crendentials.Certificate(cert=CREDENTIALS_PATH)
        try:
            firebase_admin.initialize_app(credential=credentials)
        except ValueError:
            pass
        client = firestore.client()

        return client

    def insert_batch(self, data: dict):
        collection = self.client.collection(self.collection)

        # Start a batch
        batch = self.client.batch()
        operations = 0

        for film_id, info in tqdm(data.items(), desc="Adding data to the database"):
            # key to slug
            slug = info[SLUG]
            document = collection.document(slug)

            # Add the set operation to the batch
            batch.set(document, info)
            operations += 1

            # Commit the batch every 50 operations
            if operations >= WRITE_BATCH_SIZE:
                batch.commit()
                # Start a new batch
                batch = self.client.batch()
                operations = 0

        # Commit any remaining operations
        if operations > 0:
            batch.commit()