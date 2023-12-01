import multiprocessing as mp
import time
from typing import List, Optional

from pymilvus import (
    Collection,
    MilvusException,
    connections,
    index_building_progress,
    wait_for_index_building_complete,
    utility,
)

from engine.base_client.upload import BaseUploader
from engine.clients.milvus.config import (
    DISTANCE_MAPPING,
    DTYPE_DEFAULT,
    MILVUS_COLLECTION_NAME,
    MILVUS_DEFAULT_ALIAS,
    MILVUS_DEFAULT_PORT,
)

from pymilvus import Collection, utility
from pymilvus import CollectionSchema, DataType, FieldSchema, MilvusException


class MilvusUploader(BaseUploader):
    client = None
    upload_params = {}
    collection: Collection = None
    distance: str = None

    @classmethod
    def get_mp_start_method(cls):
        return "forkserver" if "forkserver" in mp.get_all_start_methods() else "spawn"

    @classmethod
    def init_client(cls, host, distance, connection_params, upload_params):
        cls.client = connections.connect(
            alias=MILVUS_DEFAULT_ALIAS,
            host=host,
            port=str(connection_params.pop("port", MILVUS_DEFAULT_PORT)),
            **connection_params
        )
        cls.collection = Collection(MILVUS_COLLECTION_NAME, using=MILVUS_DEFAULT_ALIAS)
        cls.upload_params = upload_params
        cls.distance = DISTANCE_MAPPING[distance]

    @classmethod
    def upload_batch(
        cls, ids: List[int], vectors: List[list], metadata: Optional[List[dict]]
    ):
        if metadata is not None:
            field_values = [
                [
                    payload.get(field_schema.name) or DTYPE_DEFAULT[field_schema.dtype]
                    for payload in metadata
                ]
                for field_schema in cls.collection.schema.fields
                if field_schema.name not in ["id", "vector"]
            ]
        else:
            field_values = []
        cls.collection.insert([ids, vectors] + field_values)

    @classmethod
    def post_upload(cls, distance):
        index_params = {
            "metric_type": cls.distance,
            "index_type": cls.upload_params.get("index_type", "HNSW"),
            "params": {**cls.upload_params.get("index_params", {})},
        }
        print('!!!!!!!!!', index_params)
        cls.collection.flush()
        print("start creating index")
        cls.collection.create_index(field_name="vector", index_params=index_params)
        print("finish creating index")
        for field_schema in cls.collection.schema.fields:
            if field_schema.name in ["id", "vector"]:
                continue
            print("????", field_schema)
            try:
                cls.collection.create_index(
                    field_name=field_schema.name, index_name=field_schema.name
                )
            except MilvusException as e:
                # Code 1 means there is already an index for that column
                if 1 != e.code:
                    raise e

        # for index in cls.collection.indexes:
        #     wait_for_index_building_complete(
        #         MILVUS_COLLECTION_NAME,
        #         index_name=index.index_name,
        #         using=MILVUS_DEFAULT_ALIAS,
        #     )
            
        for index in cls.collection.indexes:
            print("index", index.index_name)
            print("wait_for_index_building_complete")
            utility.wait_for_index_building_complete(
                MILVUS_COLLECTION_NAME,
                index_name=index.index_name,
                using=MILVUS_DEFAULT_ALIAS,
            )

            def wait_index():
                while True:
                    # print("wait_index")
                    progress = utility.index_building_progress(
                        MILVUS_COLLECTION_NAME,
                        index_name=index.index_name,
                        using=MILVUS_DEFAULT_ALIAS,
                    )
                    if progress.get("pending_index_rows", -1) == 0:
                        print("finish wait_index")
                        break
                    time.sleep(5)

            wait_index()
            cls.collection.compact()
            print("start wait_for_compaction_completed")
            cls.collection.wait_for_compaction_completed()
            print("finishe wait_for_compaction_completed")
            wait_index()

        print("load")
        cls.collection.load()
        return {}
