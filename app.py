import os
from datetime import datetime
from flask import Flask
from flask import request, render_template
from PIL import Image

import config
from ultils import do_upload, do_search, do_load
from feature_extraction import FeatureExtraction
from mongodb_helpers import MongoDBHelpers
from milvus_helpers import MilvusHelpers
from crawl_image import Scraper

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['image'] = config.IMAGE

app.config['MONGODB_HOST'] = config.MONGODB_HOST
app.config['MONGODB_PORT'] = config.MONGODB_PORT
app.config['MONGODB_DATABASE'] = config.MONGODB_DATABASE

app.config['MILVUS_HOST'] = config.MILVUS_HOST
app.config['MILVUS_PORT'] = config.MILVUS_PORT

app.config['COLLECTION_NAME'] = config.COLLECTION_NAME
app.config['TOP_K'] = config.TOP_K

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


feature_extract = FeatureExtraction()
mongodb_cli = MongoDBHelpers(host=app.config['MONGODB_HOST'],
                             port=app.config['MONGODB_PORT'],
                             db_name=app.config['MONGODB_DATABASE'],
                             collection_name=app.config['COLLECTION_NAME'])
milvus_cli = MilvusHelpers(host=app.config['MILVUS_HOST'],
                           port=app.config['MILVUS_PORT'])
scraper = Scraper(image_url=[], name_folder=config.UPLOAD_FOLDER, search_keywords="",file_lengths=200, bookmarks="")


def allowed_file(file_name):
    return "." in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template(
        'index.html'
    )


@app.route("/crawl", methods=["POST"])
def crawl():
    if request.method == 'POST':
        search_key = request.form.get('q')
        scraper.reset(search_key=search_key, file_length=5, name_folder="static/image/")
        image_paths = scraper.download_images()
        paths, distances = do_search(image_path=image_paths[3],
                                     feature_extract=feature_extract,
                                     collection_name=app.config['COLLECTION_NAME'],
                                     top_k=app.config["TOP_K"],
                                     milvus_cli=milvus_cli,
                                     mongodb_cli=mongodb_cli)
        scores = zip(paths, distances)
        for image_path in image_paths:
            x = do_upload(collection_name=app.config['COLLECTION_NAME'],
                          image_path=image_path,
                          feature_extract=feature_extract,
                          milvus_cli=milvus_cli,
                          mongodb_cli=mongodb_cli)
        return render_template('index.html', query_path=image_paths[3], scores=scores)


@app.route("/upload", methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file_name=file.filename):
            # Save image
            image = Image.open(file.stream)
            upload_image_path = app.config['UPLOAD_FOLDER'] + \
                                datetime.now().isoformat().replace(":", "").replace("-", "") + "_" + file.filename
            image.save(upload_image_path)

            # Run search
            paths, distancts = do_search(image_path=upload_image_path,
                                         feature_extract=feature_extract,
                                         collection_name=app.config['COLLECTION_NAME'],
                                         top_k=app.config["TOP_K"],
                                         milvus_cli=milvus_cli,
                                         mongodb_cli=mongodb_cli)
            scores = zip(paths, distancts)

            # Load image
            x = do_upload(collection_name=app.config['COLLECTION_NAME'],
                          image_path=upload_image_path,
                          feature_extract=feature_extract,
                          milvus_cli=milvus_cli,
                          mongodb_cli=mongodb_cli)

            return render_template('index.html', query_path=upload_image_path, scores=scores)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
