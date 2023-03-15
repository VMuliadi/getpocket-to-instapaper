#!/usr/bin/python3

import json
import logging
import requests
import sys

GETPOCKET_API_VERSION = "v3"
GETPOCKET_API_ENDPOINT = "https://getpocket.com"

GETPOCKET_REDIRECT_PORT = 14045
GETPOCKET_REDIRECT_HOST = "127.0.0.1"
GETPOCKET_REDIRECT_URI = "http://{}:{}"
  .format(GETPOCKET_REDIRECT_HOST,
    GETPOCKET_REDIRECT_PORT)

class Getpocket:
  def __init__(self, consumer_key):
    self.consumer_key = consumer_key


  def get_request_token(self):
    try:
      return json.loads(requests.post(
        GETPOCKET_API_ENDPOINT + "/" + GETPOCKET_API_VERSION + "/oauth/request",
        headers={"Content-Type": "application/json", "X-Accept": "application/json"},
        json={"consumer_key": self.consumer_key, "redirect_uri": GETPOCKET_REDIRECT_URI}).text)["code"]
    except json.decoder.JSONDecodeError:
      # no need to continue if failed to get request token
      logging.error("Please check your consumer key")
      logging.error("Check request token or try again later (rate limit)")
      return ""


  def get_access_token(self, request_token):
    try:
      import threading
      from http_server import HTTP_Server, HTTPHandler
      server = HTTP_Server((GETPOCKET_REDIRECT_HOST, GETPOCKET_REDIRECT_PORT), HTTPHandler)
      thread = threading.Thread(None, server.run)
      thread.start()

      print('Please open this website on your browser and click on "Authorize" button')
      print(GETPOCKET_API_ENDPOINT + "/auth/authorize?request_token=" + request_token + "&redirect_uri=" + GETPOCKET_REDIRECT_URI)
      input("Press Enter to continue...\n")
      server.shutdown()
      thread.join()

      return json.loads(requests.post(
        GETPOCKET_API_ENDPOINT + "/" + GETPOCKET_API_VERSION + "/oauth/authorize",
        headers={"Content-Type": "application/json; charset=UTF-8", "X-Accept": "application/json"},
        json={"consumer_key": self.consumer_key, "code": request_token}).text)["access_token"]
    except json.decoder.JSONDecodeError:
      # no need to continue if failed to get access token
      logging.error("Failed to retrieve an access-token")
      logging.error("Check request token or consumer key or try again later (rate limit)")
      sys.exit(1)


  def get_articles(self, access_token):
    try:
      return requests.post(
        GETPOCKET_API_ENDPOINT + "/" + GETPOCKET_API_VERSION + "/" + "get",
        headers={"Content-Type": "application/json", "X-Accept": "application/json"},
        json={"consumer_key": self.consumer_key, "access_token": access_token}).text
    except json.decoder.JSONDecodeError:
      logging.error("Failed to retrieve the articles")
      logging.error("Check request token or consumer key or try again later (rate limit)")
      return json.dumps({})


  def delete_article(self, access_token, item_id):
    try:
      requests.get(
        GETPOCKET_API_ENDPOINT + "/" + GETPOCKET_API_VERSION + "/send",
        headers={"Content-Type": "application/json", "X-Accept": "application/json"},
        params={"consumer_key": self.consumer_key, "access_token": access_token,
          "actions": json.dumps([{"action": "delete", "item_id": item_id}])}).status_code
    except json.decoder.JSONDecodeError:
      logging.error("Failed to delete the article. Id: {}".format(item_id))
      logging.error("Check request token or consumer key or try again later (rate limit)")
