import threading
from threading import Thread
import time

from client import Client
from tracker import Tracker
from random import randint

NUM_CLIENTS = 5
clients = {} # map client id to the actual client object

def run_tracker_simulation():
  print('starting tracker simulation')
  tracker = Tracker(True)

def run_client_simulation(client_id):
  print('starting client simulation', client_id)
  client = Client(client_id, True)
  clients[client_id] = client
  # this sleep is required so that the tracker has time to listen to the new port
  time.sleep(1)

  # simulate an upload
  # random_id = randint(10000, 10000 + NUM_CLIENTS - 1)
  # uploader = clients[random_id]
  # file_location = '/tmp/test.txt'
  # uploader.upload(file_location)

  # random_id = randint(10000, 10000 + NUM_CLIENTS - 1)
  # downloader = clients[random_id]
  # print(downloader)
  # downloader.download('f0f0f8e489652435c38caa6e53b7b749')
  
  client.disconnect()

if __name__== "__main__":
  tracker_thread = Thread(target=run_tracker_simulation)

  tracker_thread.start()

  for i in range(NUM_CLIENTS):
    client_id = 10000 + i
    client_thread = Thread(target=run_client_simulation, args=[client_id])
    client_thread.start()

  time.sleep(10)
  kill_tracker_thread = Thread(target=Tracker.kill_self())
  kill_tracker_thread.start()