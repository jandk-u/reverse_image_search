import config
from crawl_image import Scraper
from feature_extraction import FeatureExtraction
from mongodb_helpers import MongoDBHelpers
from milvus_helpers import MilvusHelpers
from ultils import do_load
import time

if __name__ == '__main__':
    feature_extract = FeatureExtraction()
    milvus_cli = MilvusHelpers(host=config.MILVUS_HOST, port=config.MILVUS_PORT)
    mongodb_cli = MongoDBHelpers(host=config.MONGODB_HOST, port=config.MONGODB_PORT,
                                 db_name=config.MONGODB_DATABASE, collection_name=config.COLLECTION_NAME)

    # scaper = Scraper(
    #     image_url=[],
    #     name_folder=config.IMAGE,
    #     search_keywords="",
    #     file_lengths=config.FILE_LENGTHS,
    #     bookmarks="")
    #
    # search_key = ["cat", "dog", "bird", "elephants", "car", "plane", "pig", "anime", "girl", "view", "book"]
    # start = time.time()
    # for key in search_key:
    #     print("Crawl", key, "...")
    #     scaper.reset(search_key=key, name_folder=config.IMAGE, file_length=config.FILE_LENGTHS)
    #     scaper.download_images()
    # end = time.time()

    # print("Crawl done!", end - start, "s")
    print("Upload to milvus and Mongodb")
    image_dir = config.IMAGE + "*/*"
    lengths = do_load(image_dir=image_dir, feature_extract=feature_extract,
                      milvus_cli=milvus_cli, mongodb_cli=mongodb_cli, collection_name=config.COLLECTION_NAME)
    print(f"Upload {lengths} file")

