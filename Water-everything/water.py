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

def api_get(endpoint):
            """GET from an API endpoint."""
            response = requests.get(self.api_url + endpoint, headers={
            'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
            'content-type': "application/json"})
            #self.api_response_error_collector(response)
            #self.api_response_error_printer()
            return response


def load_plants_from_web_app():
        """Download known plants from the FarmBot Web App API."""
        response = api_get('points')
        app_points = response.json()
        if response.status_code == 200:
            log('nice','info')
            plants = []
            for point in app_points:
                if point['pointer_type'] == 'Plant':
                    plants.append({
                        'x': point['x'],
                        'y': point['y'],})
            self.plants['known'] = plants
            self.sorted_coords = sorted(self.plants['known'])
            log('sorted', 'info')

if __name__ == '__main__':

    log('test','info')
    load_plants_from_web_app()
    