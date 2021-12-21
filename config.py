
import os
import json
from dotenv import load_dotenv

load_dotenv()
class DefaultConfig(object):
    url_prefix = os.getenv('URL_PREFIX')
    S3_KEY = os.getenv('S3_KEY')
    S3_SECRET = os.getenv('S3_SECRET')
    S3_ENDPOINT = os.getenv('S3_ENDPOINT')
    S3_BUCKET = os.getenv('S3_BUCKET')
    S3_URL = os.getenv('S3_URL')
