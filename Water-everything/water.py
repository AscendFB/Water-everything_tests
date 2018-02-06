#!/usr/bin/env python
"""Plant Grid Farmware"""

import os
import json
import base64
import numpy as np
import requests

def log(message, message_type):
    'Send a message to the log.'
    log_message = '[plant-grid] ' + str(message)
    headers = {
        'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
        'content-type': "application/json"}
    payload = json.dumps(
        {"kind": "send_message",
            "args": {"message": log_message, "message_type": message_type}})
    requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
                    data=payload, headers=headers)

if __name__ == '__main__':

    log('test','info')