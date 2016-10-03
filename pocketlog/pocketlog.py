from __future__ import print_function

import boto3
import json
from datetime import datetime
import pytz
import StringIO
import botocore
import logging
import dateutil.parser as dup

logger = logging.getLogger()
s3 = boto3.client('s3')
DEFAULTS=json.loads(open('config.json','r').read())

# Receive JSON payloads from Pocket via IFTTT, record them to S3 by date.

# { "title": "{{Title}}",
# "image_url": "{{ImageUrl}}",
# "tags": "{{Tags}}",
# "url": "{{Url}}",
# "datetime": "{{AddedAt}}",
# "excerpt": "{{Excerpt}}", }


def update_log(bucket, path, payload, dt=None):
  '''fetch and update today's reading log'''
  logger.debug('update_log: starting with bucket=%s, path=%s, payload=%s, dt=%s' % (bucket, path, payload, dt))
  key = '%s/%s' % (path, format_filename(dt))
  logger.debug('update_log: s3 obj key: %s' % key)
  log = get_log(bucket, key)
  logger.debug('update_log: log acquired: %s' % log)
  if log and payload not in log:
    log.append(payload)
  else:
    log = [payload]
  logger.debug('update_log: log updated: %s' % log)
  write_log(bucket, key, json.dumps(log))
  logger.debug('update_log: log written to s3')
  return(bucket+'/'+key)

def format_filename(dt=None):
  dt = datetime.now(pytz.timezone('US/Pacific')) if not dt else dt
  return 'readinglist.%s.json' % dt.strftime('%Y-%m-%d')

def format_slug(dt=None):
  dt = datetime.now(pytz.timezone('US/Pacific')) if not dt else dt
  return 'reading-list_%s' % dt.strftime('%Y-%m-%d')

def get_log(bucket, key):
  '''fetch a reading log from s3'''
  try:
    return json.loads(s3.get_object(Bucket=bucket, Key=key)['Body'].read())
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchKey':
      return None
    else:
      raise(e)

def write_log(bucket, key, contents):
  '''write a reading log to s3'''
  s3.put_object(Bucket=bucket, Key=key, Body=StringIO.StringIO(contents).read())

def handler(event, context, bucket=DEFAULTS['bucket'], path=DEFAULTS['path'], dt=DEFAULTS['dt'], apikey=DEFAULTS['apikey']):
  '''Receive JSON payloads from Pocket via IFTTT, record them by date.'''

  operations = {
    'POST': lambda x: update_log(bucket, path, x, dt),
    'GET': lambda x: get_log(bucket, path, dup.parse(x['dt']) if not dt else dt)
  }

  operation = event['httpMethod']
  if operation in operations:
    logger.info(event)
    if operation == 'GET' and 'queryStringParameters' in event.keys():
      payload = event['queryStringParameters']
    else:
      payload = json.loads(event['body']) if type(event['body']) is not dict else event['body']

    if 'apikey' not in payload.keys() or payload['apikey'] != apikey:
      return respond(ValueError('NOPE. Gimme an API key.'))
      
    return respond(None, operations[operation](payload))
  else:
    return respond(ValueError('Unsupported method "{}"'.format(operation)))

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
