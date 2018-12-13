import threading
from threading import Thread
import time
import os
import atexit

from client import Client
from tracker import Tracker
from random import randint

NUM_CLIENTS = 3
clients = {} # map client id to the actual client object

def run_tracker_simulation():
  print('starting tracker simulation')
  tracker = Tracker(True)

def run_client_simulation(client_id):
  print('starting client simulation', client_id)
  client = Client(client_id, True)
  clients[client_id] = client

  if not os.path.exists(client.directory):
      os.makedirs(client.directory)
      print('created directory:', client.directory)

  # this sleep is required so that the tracker has time to listen to the new port
  time.sleep(1)

  if client_id == 10000:
    run_upload_simulation(client_id)

  if client_id == 10001:
    run_download_simulation(client_id)

  client.disconnect()

def run_upload_simulation(client_id):
  uploader = clients[client_id]
  file_name = 'test.txt'
  uploader.upload(file_name)

def run_download_simulation(client_id, file_name='test.txt'):
  downloader = clients[client_id]
  downloader.download(file_name)

def exit_handler():
  for key in clients:
    clients[key].disconnect()

atexit.register(exit_handler)

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
  exit_handler()