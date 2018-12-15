import threading
from threading import Thread
import time
import os

from client import Client
from tracker import Tracker
from random import randint

NUM_CLIENTS = 5
clients = {} # map client id to the actual client object

def run_tracker_simulation():
  Tracker(False)

def run_client_simulation(client_id):
  client = Client(client_id, True)
  clients[client_id] = client

  if not os.path.exists(client.directory):
      os.makedirs(client.directory)
      print('created directory:', client.directory)

  # this sleep is required so that the tracker has time to listen to the new port
  time.sleep(1)

  if client_id == 10000:
    client.upload('test1.txt')
    client.upload('test3.txt')

  if client_id == 10001:
    client.download('test2.txt')

  if client_id == 10002:
    client.download('test1.txt')

  if client_id == 10003:
    client.download('test3.txt')

  if client_id == 10004:
    client.download('test1.txt')

  time.sleep(1)

  client.disconnect()

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