#!/usr/bin/python3

import json
import logging
import os

from getpocket import Getpocket
from getpass import getpass
from instapaper import Instapaper

logging.basicConfig(
  format='%(asctime)s %(levelname)s %(message)s',
  level=logging.INFO)


getpocket = Getpocket(os.environ["GETPOCKET_CONSUMER_KEY"])
request_token = getpocket.get_request_token()
access_token = getpocket.get_access_token(request_token=request_token)

instapaper_username = os.environ["INSTAPAPER_USERNAME"]
instapaper_password = getpass("Instapaper password for {}: ".format(instapaper_username))
instapaper = Instapaper(instapaper_username, instapaper_password)

delete_after_import = False
delete_after_import_input = input("Delete pocket's data after import? (y/N): ")
if delete_after_import_input.lower() == "y":
  logging.info("Pocket's article will be deleted after import")
  delete_after_import = True

if instapaper.authenticate():
  try:
    error_message = {}
    error_message[400] = "Bad request or exceeded the rate limit"
    error_message[403] = "Invalid username or password"
    error_message[500] = "The service encountered an error. Please try again later."

    articles = getpocket.get_articles(access_token=access_token)
    parsed_articles = json.loads(articles)
    number_of_articles = len(parsed_articles["list"])

    failed_to_migrate = False
    failed_migration_list = []
    for index, article_id in enumerate(parsed_articles["list"]):
      article = parsed_articles["list"][article_id]
      article_url = article["resolved_url"]
      article_title = article["given_title"]
      status_code = instapaper.add_article(url=article_url, title=article_title)
      if status_code in [400, 403, 500]:
        failed_to_migrate = True
        failed_migration_list.add(article_id)
        logging.error("Failed to migrate {}. Message: {}"
          .format(article_id, error_message[status_code]))

      if not failed_to_migrate or delete_after_import:
        getpocket.delete_article(access_token=access_token, item_id=article_id)
        logging.info("#{}/{} [DEL] {}".format(index+1, number_of_articles, article_title))

    if len(failed_migration_list) > 0:
      logging.error("{} failed to migrate :: {}"
        .format(len(failed_migration_list),
          " ".join(failed_migration_list)))
  except Exception as exc:
    logging.error(exc, exc_info=True)
    pass
