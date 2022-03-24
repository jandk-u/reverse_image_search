# Milvus
from pymilvus import connections, FieldSchema,CollectionSchema, DataType, Collection, utility


class MilvusHelpers:
    def __init__(self, host, port):
        try:
            self.collection = None
            connections.connect(host=host, port=port)
        except Exception as e:
            print('Failed to connect Milvus:', e)

    def has_collection(self, collection_name):
        try:
            return utility.has_collection(collection_name)
        except Exception as e:
            print("Failed to load data to Milvus:", e)

    def set_collection(self, collection_name):
        try:
            if self.has_collection(collection_name):
                self.collection = Collection(name=collection_name)
            else:
                raise Exception("There is no collection named:", collection_name)
        except Exception as e:
            print("Failed to load data to Milvus:", e)

    def create_collection(self, collection_name):
        try:
            if not self.has_collection(collection_name):
                id_ = FieldSchema(name="id", dtype=DataType.INT64, description="int64", is_primary=True, auto_id=True)
                embedding = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, description="float_vector",
                                        dim=4096, is_primary=False)
                schema = CollectionSchema(fields=[id_, embedding], description="collection description")
                self.collection = Collection(name=collection_name, schema=schema)
            else:
                self.set_collection(collection_name)
            return "OK"
        except Exception as e:
            print("Failed to load data to Milvus:", e)

    def insert(self, collection_name, vectors):
        try:
            self.create_collection(collection_name)
            self.set_collection(collection_name)
            mr = self.collection.insert(vectors)
            ids = mr.primary_keys
            self.collection.load()
            return ids
        except Exception as e:
            print("Failed to load data to Milvus:", e)

    def create_index(self, collection_name):
        try:
            self.set_collection(collection_name)
            default_index = {"index_type":"IVF_SQ8", "metric_type":"L2", "params":{"nlist":16384}}
            status = self.collection.create_index(field_name="embedding", index_params=default_index)
            if not status.code:
                return status
            else:
                raise Exception(status.message)
        except Exception as e:
            print("Failed to create index:", e)

    def delete_collection(self, collection_name):
        try:
            self.set_collection(collection_name)
            self.collection.drop()
            return "OK"
        except Exception as e:
            print("Failed to drop collection", e)

    def search_vector(self, collection_name, vector, top_k):
        try:
            self.set_collection(collection_name)
            search_params = {"metric_type": "IP", "params":{"nprobe":16}}
            res = self.collection.search(vector, anns_field="embedding", param=search_params, limit=top_k)
            return res
        except Exception as e:
            print("Failed to search vectors in Mivuls:", e)

    def count(self, collection_name):
        try:
            self.set_collection(collection_name)
            num = self.collection.num_entities
            return num
        except Exception as e:
            print("Failed to count vectors in Milvus:", e)
