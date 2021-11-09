import json
import pynamodb
import requests


def handler(event, contexts):
    print('event: {}'.format(json.dumps(event)))

    return {}
