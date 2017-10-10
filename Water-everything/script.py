#!/usr/bin/env python
"""
"""
import os
import json
import base64
import requests
import numpy as np
import CeleryPy
import ENV
from time import sleep
from CeleryPy import log
from sequence_writer import Sequence






class Water_everything(object):

    def __init__(self):
        """Set initial attributes."""
        self.plants = {'known': [], 'save': [],
                       'remove': [], 'safe_remove': []}
        self.water_sequence = {'seq_id': []}
        self.seq = {'all_sequences' : []}
        self.sorted_coords = {'sorted':[]}
        self.found_sequence=0
        self.search_sequence_counter=0
        self.sequence_done=False
        self.seq_id_as_int = 0

        
        self.sequences = []
        self.water_sequence = []

        # API requests setup
        try:
            api_token = os.environ['API_TOKEN']
        except KeyError:
 #           api_token = 'x.eyJpc3MiOiAiLy9zdGFnaW5nLmZhcm1ib3QuaW86NDQzIn0.x'
             api_token = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJoZWhlMTIzNEBob3RtYWlsLmRlIiwiaWF0IjoxNTA3Mzc2NTY2LCJqdGkiOiI2ODQ1M2NiZC1kMTJkLTQxOTktYTdjNC1iNTY2ZDU1YzJmMDEiLCJpc3MiOiIvL215LmZhcm1ib3QuaW86NDQzIiwiZXhwIjoxNTEwODMyNTY2LCJtcXR0IjoibXF0dC5mYXJtYm90LmlvIiwib3NfdXBkYXRlX3NlcnZlciI6Imh0dHBzOi8vYXBpLmdpdGh1Yi5jb20vcmVwb3MvZmFybWJvdC9mYXJtYm90X29zL3JlbGVhc2VzL2xhdGVzdCIsImZ3X3VwZGF0ZV9zZXJ2ZXIiOiJodHRwczovL2FwaS5naXRodWIuY29tL3JlcG9zL0Zhcm1Cb3QvZmFybWJvdC1hcmR1aW5vLWZpcm13YXJlL3JlbGVhc2VzL2xhdGVzdCIsImJvdCI6ImRldmljZV8xNyJ9.zp9OTN54jIzx18efKaliu0EuPl0AnzX7igd0rxaON1pdEqzrbwg-zGRv-1DI2AmQhjpb_472pV86yA2QOiqahmzum8z259Y4IVB1HsVXwhIBzOuCDzXuD_hFToRxoqtbTU4ySDaCudH8nuODin9B0SjzJgqEay_R1P8qXgrhpZKIrzRuzrfgWZDLbeD7Vmqm-SDNg0vKe0dvYNTrHVF6Yc0rO807U9TKM0uBN5IiPlwUKf3UHHCV-C0-t0fcFFqKaVo0Q6SFZcqWucwcqu3uOtgkqM-h8uIDk1eQytUTvKK0MTZ56Kh91VTXQMy3_9MlViH866r70o72w5OzNqljTA'
        try:
            encoded_payload = api_token.split('.')[1]
            encoded_payload += '=' * (4 - len(encoded_payload) % 4)
            json_payload = base64.b64decode(encoded_payload).decode('utf-8')
            server = json.loads(json_payload)['iss']
        except:  # noqa pylint:disable=W0702
            server = '//my.farmbot.io'
        self.api_url = 'http{}:{}/api/'.format(
            's' if 'localhost' not in server else '', server)
        self.headers = {'Authorization': 'Bearer {}'.format(api_token),
                        'content-type': "application/json"}
        self.errors = {}

    def api_get(self, endpoint):
        """GET from an API endpoint."""
        response = requests.get(self.api_url + endpoint, headers=self.headers)
        self.api_response_error_collector(response)
        self.api_response_error_printer()
        return response

    def api_response_error_collector(self, response):
        """Catch and log errors from API requests."""
        self.errors = {}  # reset
        if response.status_code != 200:
            try:
                self.errors[str(response.status_code)] += 1
            except KeyError:
                self.errors[str(response.status_code)] = 1

    def api_response_error_printer(self):
        """Print API response error output."""
        error_string = ''
        for key, value in self.errors.items():
            error_string += '{} {} errors '.format(value, key)
        print(error_string)


 
    def load_plants_from_web_app(self):
        """Download known plants from the FarmBot Web App API."""
        response = self.api_get('points')
        app_points = response.json()
        if response.status_code == 200:
            plants = []
            for point in app_points:
                if point['pointer_type'] == 'Plant':
                    plants.append({
                        'x': point['x'],
                        'y': point['y'],})
            self.plants['known'] = plants
            self.sorted_coords = sorted(self.plants['known'])
            
          

    def load_sequences_from_app(self):
        response = self.api_get('sequences')
        app_sequences = response.json()
        if response.status_code == 200:
            self.sequences = []
            self.water_sequence = []
            for seq in app_sequences:
                if seq['name'] == 'FW_Water_everything':
                  self.water_sequence.append(seq['id'])
                  self.found_sequence=1
        a.check_if_sequence_found()

                  
                 

    def check_if_sequence_found(self):
        if self.found_sequence == 0:    
                self.water_sequence[:] = []
                log("No watering sequence found. I will create one.",message_type ='info', title = 'Water-everything')
                a.create_sequence()
                self.search_sequence_counter +=1                                                                              
        if self.found_sequence == 1:
                [int(i) for i in self.water_sequence]
                self.seq_id_as_int = int(i)
                if self.sequence_done == False:
                    log("Found the watering sequence.",message_type ='info', title = 'Water-everything')
                    a.loop_plant_points()


                
               

           
    def loop_plant_points(self): 
        count = 0                               #Counter to limit the points for tests.      
        for plant in self.sorted_coords:
                if count < 3:
                   print ("moving to points")
                   CeleryPy.move_absolute(
                    location=[plant['x'],plant['y'] ,0],
                    offset=[0, 0, 0],
                    speed=800)
                   CeleryPy.execute_sequence(sequence_id= self.seq_id_as_int)
                   print(self.seq_id_as_int)
                   self.sequence_done = True
                   count +=1

  
          
    def count_downloaded_plants(self):
        plant_count = len(self.plants['known'])
        log( "{} plants were detected." .format(plant_count)
            ,message_type= 'info',title= 'Water-everything')

   

    def create_sequence(self):

        def upload(sequence):
            r = requests.post(self.api_url + 'sequences', data=json.dumps(sequence), headers=self.headers)
            print(r, r.json())
            self.response = r

        if self.search_sequence_counter <3:
         with Sequence("FW_Water_everything", "green", upload) as s:
            s.write_pin(number = 9,value = 1,mode = 0)
            s.wait(milliseconds=2500)
            s.write_pin(number = 9,value = 0,mode = 0)
        if self.response.status_code == 422:
            log("Cant create sequence because this name already exists. Check for upper- and lowercases.",message_type ='info', title = 'Water-everything')
        if self.response.status_code == 200:
            log("Created a sequence named FW_Water_everything.",message_type ='info', title = 'Water-everything')
            CeleryPy.sync()
            a.load_sequences_from_app()
        else:
            print("There was an Error creating the sequence.")
        




if __name__ == "__main__":
    a = Water_everything()

    a.load_plants_from_web_app()
    a.count_downloaded_plants()
    a.load_sequences_from_app()

