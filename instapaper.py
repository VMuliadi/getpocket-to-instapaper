#!/usr/bin/python3

import json
import requests
from requests.auth import HTTPBasicAuth

INSTAPAPER_API_ENDPOINT = "https://www.instapaper.com/api"

class Instapaper:
  def __init__(self, username, password):
    self.username = username
    self.password = password

  def authenticate(self):
    try:
      return requests.post(
        INSTAPAPER_API_ENDPOINT + "/authenticate",
        auth=HTTPBasicAuth(self.username, self.password)
        ).status_code == 200
    except json.decoder.JSONDecodeError:
      # no need to continue if failed to authenticate user
      logging.error("Failed to authenticate user")
      logging.error("Check username and password or try again later (rate limit)")
      sys.exit(1)

  def add_article(self, url, title):
    return requests.post(
      INSTAPAPER_API_ENDPOINT + "/add",
      auth=HTTPBasicAuth(self.username, self.password),
      data={"title": title, "url": url}).status_code

  def delete_article(self, url, title):
    pass
