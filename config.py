
import os
import json
from dotenv import load_dotenv

load_dotenv()
class DefaultConfig(object):
    url_prefix = os.getenv('URL_PREFIX')