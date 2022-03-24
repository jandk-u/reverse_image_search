from feature_extraction import FeatureExtraction
from milvus_helpers import MilvusHelpers
from mongodb_helpers import MongoDBHelpers
import ultils


if __name__ == '__main__':
    feature_extract = FeatureExtraction()
    milvus_cli = MilvusHelpers(host="127.0.0.1", port=19530)
    mongodb_cli = MongoDBHelpers(host="127.0.0.1", port=27017, db_name="image_search", collection_name="image_search")
    status = ultils.do_drop("image_search", mongodb_cli=mongodb_cli, milvus_cli=milvus_cli)
    # print(status)
    # test insert vector in milvus
    # status = milvus_cli.create_collection("image_search")
    # print(status)
    # ids = ultils.do_load(collection_name="image_search", feature_extract=feature_extract, image_dir=r"./photo/*/*", mongo_cli=mongodb_cli, milvus_cli=milvus_cli)
    # ids = ['431968464806086795', '431968464806086808', '431968464806086821', '431968464806086834', '431968464806086847']
    # search = mongodb_cli.find("image_search")
    # print(search)
    # for item in search:
    #     print(item)
    #
    # print("Record in milvus", milvus_cli.count("image_search"))




