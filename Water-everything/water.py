#!/usr/bin/env python
"""
"""
import os
import json
import base64
import requests
import numpy as np
from time import sleep
from sequence_writer import Sequence

#API_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1bmtub3duIiwic3ViIjoxNywiaWF0IjoxNTE3OTA1MTExLCJqdGkiOiI4NDdmNGVjMC03ZmZjLTQ4MzItODJmMy1hZjUwYThlMDMwYmYiLCJpc3MiOiIvL215LmZhcm1ib3QuaW86NDQzIiwiZXhwIjoxNTIxMzYxMTExLCJtcXR0IjoiYnJpc2stYmVhci5ybXEuY2xvdWRhbXFwLmNvbSIsImJvdCI6ImRldmljZV8xNyIsInZob3N0IjoidmJ6Y3hzcXIiLCJtcXR0X3dzIjoid3NzOi8vYnJpc2stYmVhci5ybXEuY2xvdWRhbXFwLmNvbTo0NDMvd3MvbXF0dCIsIm9zX3VwZGF0ZV9zZXJ2ZXIiOiJodHRwczovL2FwaS5naXRodWIuY29tL3JlcG9zL2Zhcm1ib3QvZmFybWJvdF9vcy9yZWxlYXNlcy9sYXRlc3QiLCJpbnRlcmltX2VtYWlsIjoiaGVoZTEyMzRAaG90bWFpbC5kZSIsImZ3X3VwZGF0ZV9zZXJ2ZXIiOiJERVBSRUNBVEVEIiwiYmV0YV9vc191cGRhdGVfc2VydmVyIjoiaHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9GYXJtQm90L2Zhcm1ib3Rfb3MvcmVsZWFzZXMvOTUxMDc2NSJ9.mHUQLkKLOsw4UXMwpq7Yl-45NRFeuP0mIw3o-c1aSYTY7hjLPydsam9kOGULf04hhsJEOdBdUtjOGcXpftbKtnZ1pSNbftRNfUKK8Vth7r94jd1l4-SCF7Oz7P4OxDCBAFOQqu3CM3Rr-kXKm_Mkw_qI2XYto8GATtLSyAby6ZU1ci-WHikfYJpSMZj7LZGDfiqPNbqV6OphmllktZUeE88ji3Qxn7dhNsTYaYKC3d-d_rlRB0J7cP-YEwUqpcU1qcWvHh_yT5AaUjtTYjOqjenbzqK9qvKew9p2CqWqMKuSUrxcsSaHQJBia1iKEdVnCQVNtsOJ39m-wQNc8Ie-Qg'


def api_url():
                major_version = int(os.getenv('FARMBOT_OS_VERSION', '0.0.0')[0])
                base_url = os.environ['FARMWARE_URL']
                return base_url + 'api/v1/' if major_version > 5 else base_url


class Water_everything():
    def init(self):
        #          """Set initial attributes."""
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

    def api_url(self):
                major_version = int(os.getenv('FARMBOT_OS_VERSION', '0.0.0')[0])
                base_url = os.environ['FARMWARE_URL']
                return base_url + 'api/v1/' if major_version > 5 else base_url


    def post(self, wrapped_data):
                """Send the Celery Script command."""
                self.headers = {
                    'Authorization': 'bearer {}'.format(FARMWARE_TOKEN),
                    'content-type': "application/json"}
                payload = json.dumps(wrapped_data)
                requests.post(api_url() + 'celery_script',
                              data=payload, headers=self.headers)

    def log(self, message, message_type):
                'Send a message to the log.'
                log_message = '[Water-Everything] ' + str(message)
                wrapped_message = json.dumps(
                    {"kind": "send_message",
                        "args": {"message": log_message, "message_type": message_type}})
                self.post(wrapped_message)



    def api_get(self, endpoint):
            """GET from an API endpoint."""
            response = requests.get(api_url() + endpoint, headers={
                    'Authorization': 'bearer {}'.format(FARMWARE_TOKEN),
                    'content-type': "application/json"})
            #self.api_response_error_collector(response)
            #self.api_response_error_printer()
            return response

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
                    self.log('No watering sequence found. I will create one.','info')
                    a.create_sequence()
                    self.search_sequence_counter +=1                                                                              
                if self.found_sequence == 1:
                    [int(i) for i in self.water_sequence]
                    self.seq_id_as_int = int(i)
                    if self.sequence_done == False:
                        self.log('Found the watering sequence.','info')
                        a.loop_plant_points()



    
    def loop_plant_points(self): 
           # count = 0                               #Counter to limit the points for tests.      
            for plant in self.sorted_coords:
                    #if count < 3:
                       print ("moving to points")
                       data = {"kind": "move_absolute", "args": {'x': plant['x'], 'y': plant['y'], 'z': 0, 'speed': 800}}
                       moving_coords = json.dumps(data)
                       r = requests.post(api_url() + 'celery_script', data=moving_coords, headers= self.headers)
                       #CeleryPy.move_absolute(
                       # location=[plant['x'],plant['y'] ,0],
                       # offset=[0, 0, 0],
                       # speed=800)
                       #CeleryPy.execute_sequence(sequence_id= self.seq_id_as_int)
                       seq_number = {"kind": "execute", "args": {"sequence_id": self.seq_id_as_int}}
                       print(self.seq_id_as_int)
                       self.sequence_done = True
                      # count +=1
        
    def count_downloaded_plants(self):
            plant_count = len(self.plants['known'])
            self.log( '{} plants were detected.' .format(plant_count),'info')

    
    def create_sequence(self):

            def upload(sequence):
                r = requests.post(api_url() + 'sequences', data=json.dumps(sequence), headers=self.headers)
                print(r, r.json())
                self.response = r

            if self.search_sequence_counter <3:
             with Sequence("FW_Water_everything", "green", upload) as s:
                s.write_pin(number = 9,value = 1,mode = 0)
                s.wait(milliseconds=2500)
                s.write_pin(number = 9,value = 0,mode = 0)
            if self.response.status_code == 422:
               self.log('Cant create sequence because this name already exists. Check for upper- and lowercases.','info')
            if self.response.status_code == 200:
                self.log('Created a sequence named FW_Water_everything.','info')
                CeleryPy.sync()
                a.load_sequences_from_app()
            else:
                print("There was an Error creating the sequence.")                
                        


if __name__ == "__main__":
    a = Water_everything()

    a.init()
    a.load_plants_from_web_app()
    a.count_downloaded_plants()
    a.load_sequences_from_app()