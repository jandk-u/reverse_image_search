# Crawl image from Pinterest
import os

import requests
import urllib
import json
import time


class Pinterest:

    IMAGE_SEARCH_URL = "https://tr.pinterest.com/resource/BaseSearchResource/get/?"

    def __init__(self, search_keywords, file_lengths=100, bookmarks=""):
        self.search_keywords = search_keywords
        self.file_lengths = file_lengths
        self.image_quality = "orig"
        self.bookmarks = bookmarks

    # image search url
    @property
    def source_url(self):
        return "/search/pins/?q=" + urllib.parse.quote(self.search_keywords)

    # search parameter "source_url"
    @property
    def search_url(self):
        return self.IMAGE_SEARCH_URL

    # search parameter "data"
    @property
    def image_data(self):
        if self.bookmarks == "":
            return '''{"options":{"isPrefetch":false,"query":"''' + self.search_keyword + '''","scope":"pins","no_fetch_context_on_resource":false},"context":{}}'''
        else:
            return '''{"options":{"page_size":25,"query":"''' + self.search_keyword + '''","scope":"pins","bookmarks":["''' + self.bookmark + '''"],"field_set_key":"unauth_react","no_fetch_context_on_resource":false},"context":{}}'''.strip()

    # set and get for search_keyword
    @property
    def search_keyword(self):
        return self.search_keywords

    @search_keyword.setter
    def search_keyword(self, search_keywords):
        self.search_keywords = search_keywords

    # set and get for file_length
    @property
    def file_length(self):
        return self.file_lengths
    
    @file_length.setter
    def file_length(self, file_length):
        self.file_lengths = file_length

    # set and get for bookmark
    @property
    def bookmark(self):
        return self.bookmarks

    @bookmark.setter
    def bookmark(self, bookmarks):
        self.bookmarks = bookmarks

        
class Scraper(Pinterest):

    def __init__(self, image_url=[], name_folder="photo/", **kwargs):
        super().__init__(**kwargs)
        self.image_urls = image_url
        self.name_folder = name_folder

    def reset(self, search_key, file_length, name_folder="static/image/"):
        self.__init__(image_url=[],
                      name_folder=name_folder,
                      search_keywords=search_key,
                      file_lengths=file_length,
                      bookmarks="")

    def get_urls(self):
        """
        Get URL of the image related to the search key
        :return: list of URL
        """
        SOURCE_URL = self.source_url
        DATA = self.image_data
        URL_CONSTANT = self.search_url

        r = requests.get(URL_CONSTANT, params={
            "source_url": SOURCE_URL, "data": DATA
        })
        json_data = json.loads(r.content)
        resource_response = json_data["resource_response"]
        data = resource_response["data"]
        results = data["results"]

        for i in results:
            try:
                self.image_urls.append(
                    i["images"][self.image_quality]["url"]
                )
            except Exception as e:
                pass
        if len(self.image_urls) < int(self.file_lengths):
            self.bookmark = resource_response["bookmark"]
            print("Creating links: ", len(self.image_urls))
            self.get_urls()
            return self.image_urls[0: self.file_lengths]
        else:
            return self.image_urls[0: self.file_lengths]

    def download_images(self):
        """
        Download image from url list
        :return: None
        """
        print(self.search_keywords)
        folder = self.name_folder + self.search_keywords.replace(" ", "-")
        numbers = 1
        results = self.get_urls()
        try:
            os.makedirs(folder)
            print("Directory ", folder, " Created ")
        except FileExistsError:
            print("Error create folder!")

        arr = os.listdir(folder+"/")
        image_paths = []
        for i in results:
            if str(i + ".jpg") not in arr or str(i + ".png") not in arr:
                try:
                    file_name = str(i.split("/")[-1])
                    download_folder = str(folder) + "/" + file_name
                    image_paths.append(download_folder)
                    print("Download", numbers, ": ", i)
                    urllib.request.urlretrieve(i, download_folder)
                    numbers = numbers + 1
                except Exception as e:
                    print(e)
        return image_paths


if __name__ == '__main__':
    scaper = Scraper(
        image_url=[],
        name_folder="status/",
        search_keywords="",
        file_lengths=200,
        bookmarks="")

    search_key = ["cat", "dog", "bird", "elephants", "car", "plane", "pig", "anime", "girl", "view", "book"]
    start = time.time()
    for key in search_key:
        print("Crawl", key, "...")
        scaper.reset(search_key=key, name_folder="static/image/", file_length=200)
        scaper.download_images()
    end = time.time()

    print("Done!", end - start, "s")
