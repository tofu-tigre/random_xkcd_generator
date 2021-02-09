# XKCD Image Retriever
import requests
import re
from bs4 import BeautifulSoup
import webbrowser

XKCD_RANDOM_URL = "https://c.xkcd.com/random/comic/"

def get_soup_info(comic_soup):
    info = {}
    try:
        # TODO: Fix TypeError issue where "comic_soup.find("meta", property = "og:url")" returns None.
        info["url"] = comic_soup.find("meta", property = "og:url")["content"]
        info["issue"] = [int(element) for element in re.findall(r'\d+', info["url"])][0]
        info["title"] = comic_soup.find("meta", property = "og:title")["content"]
        info["image_url"] = "https:" + comic_soup.find(id="comic").img["src"]
        info["image_text"] = comic_soup.find(id="comic").img["title"]
        return info
    except TypeError:
        return None


def get_random_comic():
    try:
        # Soupify web content
        random_xkcd = requests.get(XKCD_RANDOM_URL)
        soup = BeautifulSoup(random_xkcd.content, "html.parser")

        # Get random comic info
        return get_soup_info(soup)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to", XKCD_RANDOM_URL)

#print(get_random_comic())
webbrowser.open(get_random_comic()["image_url"], new=1)