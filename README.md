# ifttt-pocket-webhook

Accepts incoming calls from Pocket via IFTTT and keeps a daily log of them in
JSON on S3. Built for AWS Lambda.

## Usage

The cloudformation template will deploy the role required *only*. It assumes that
there's already a bucket in the account we can use.

Deployment was handled with lambda-uploader. It's in the docker image. It demands
a lambda.json file, which requires an account number in the role ARN. Be sure to
put that in.

config.json in the pocketlog directory sets the bucket and storage path. It also
holds an "API key". This is checked in the handler for equiv and nothing else. I
put this in because IFTTT's Maker channel doesn't let you muck with headers, which
is where API Gateway would expected to find the API key.

## Warning

Since the API key check is in Lambda, not external to it, spammers could hammer
API Gateway and drive up costs. There's no profit in it so it seems unlikely
but still.
