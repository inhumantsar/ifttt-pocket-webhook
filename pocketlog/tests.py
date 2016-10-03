import pocketlog as pl
import unittest
import json
from datetime import datetime
import logging
import boto3

logger = logging.getLogger()
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

class TestPocketLog(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    boto3.client('s3').delete_object(Bucket=pl.DEFAULTS['bucket'],Key='%s/readinglist.1999.12.31.json' % pl.DEFAULTS['path'])

  def test_upload(self):
    # handler(event, context, bucket='samsite.ca', path='json/readinglist', dt=None):
    body = json.dumps({
      'title': 'psychadelic santa',
      'image_url': 'http://i.imgur.com/8XhpU.gif',
      'tags': 'tag1, tag2, tag3, tag4',
      'url': 'http://imgur.com/8XhpU',
      'excerpt': 'this is a test entry. there might be a lot of them.'
    })
    try:
      pl.handler(event={'httpMethod':'POST','body':body},context=None,dt=datetime(1999, 12, 31, 11, 59, 59))
    except Exception as e:
      self.fail('ERROR: Exception encountered: %s: %s' % (e, e.message))
