
from tqdm import tqdm
import glob2


def do_search(image_path, feature_extract, collection_name, top_k, milvus_cli, mongodb_cli):
    try:
        feature = feature_extract.extract(image_path)
        vectors = milvus_cli.search_vector(collection_name, feature, top_k)
        vids = [str(x.id) for x in vectors[0]]
        results = mongodb_cli.search(collection_name, {'_id': {'$in': vids}})
        paths = []
        for result in results:
            paths.append(result['path'])
        distances = [x.distance for x in vectors[0]]
        return paths, distances
    except Exception as e:
        print("Error with search", e)


def do_load(image_dir, feature_extract, collection_name, milvus_cli, mongodb_cli):
    vectors, names = extract_features(image_dir=image_dir, feature_extract=feature_extract)
    ids = [milvus_cli.insert(collection_name, [vector])[0] for vector in vectors]
    data = []
    for i in range(len(ids)):
        value = ({"_id": str(ids[i]), "path": names[i]})
        data.append(value)
    mongodb_cli.insert(collection_name, data)
    return len(ids)


def extract_features(image_dir, feature_extract):
    try:
        features = []
        names = []
        for file_path in tqdm(glob2.glob(image_dir)):
            try:
                feature = feature_extract.extract(file_path)
                features.append(feature)
                names.append(file_path)
            except Exception as e:
                print("\nError with extracting feature from image", e)
        return features, names
    except Exception as e:
        print("\nError with extracting feature from image", e)


def do_drop(collection_name, milvus_cli, mongodb_cli):
    try:
        if not milvus_cli.has_collection(collection_name):
            return f"\nMilvus doesn't have a collection named {collection_name}"
        status = milvus_cli.delete_collection(collection_name)
        mongodb_cli.delete_collection(collection_name)
        return status
    except Exception as e:
        print("\nError with drop collection:", e)


def do_upload(collection_name, image_path, feature_extract, milvus_cli, mongodb_cli):
    try:
        feature = feature_extract.extract(image_path)
        ids = milvus_cli.insert(collection_name, [feature])
        mongodb_cli.insert(collection_name, [{'_id': str(ids[0]), 'path': image_path}])
        return ids[0]
    except Exception as e:
        print("Error with upload:", e)
