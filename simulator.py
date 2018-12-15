import threading
from threading import Thread
import time
import os
import atexit

from client import Client
from tracker import Tracker
from random import randint

NUM_CLIENTS = 5
clients = {} # map client id to the actual client object

def run_tracker_simulation():
  tracker = Tracker(False)

def run_client_simulation(client_id):
  client = Client(client_id, True)
  clients[client_id] = client

  if not os.path.exists(client.directory):
      os.makedirs(client.directory)
      print('created directory:', client.directory)

  # this sleep is required so that the tracker has time to listen to the new port
  time.sleep(1)

  if client_id == 10000:
    # run_upload_simulation(client_id, 'test.txt')
    # run_upload_simulation(client_id, 'two.txt')
    client.upload('test1.txt')
    client.upload('test2.txt')
  
  if client_id == 10001:
    client.upload('test3.txt')
  
  time.sleep(1)

  if client_id == 10002:
    client.download('test1.txt')

  if client_id == 10003:
    client.download('test3.txt')
    
  client.disconnect()

def run_upload_simulation(client_id, file_name):
  uploader = clients[client_id]
  uploader.upload(file_name)

def run_download_simulation(client_id, file_name):
  downloader = clients[client_id]
  downloader.download(file_name)

if __name__== "__main__":
  tracker_thread = Thread(target=run_tracker_simulation)
  tracker_thread.start()

  for i in range(NUM_CLIENTS):
    client_id = 10000 + i
    client_thread = Thread(target=run_client_simulation, args=[client_id])
    client_thread.start()

  time.sleep(5)
  kill_tracker_thread = Thread(target=Tracker.kill_self())
  kill_tracker_thread.start()