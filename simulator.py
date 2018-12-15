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

def initialise_client(client_id):
  client = Client(client_id, True)
  clients[client_id] = client

  if not os.path.exists(client.directory):
      os.makedirs(client.directory)
      print('created directory:', client.directory)

  if client_id == 10000:
    print('created test file in ' + client.directory + "/test1.txt")
    with open(client.directory + "/test1.txt", "w") as file:
      file.write("hello")

    print('created test file in ' + client.directory + "/test3.txt")
    with open(client.directory + "/test3.txt", "w") as file:
      file.write("world")

  # this sleep is required so that the tracker has time to listen to the new port
  time.sleep(1)

def run_client_simulation():
  clients[10000].upload('test1.txt')
  clients[10000].upload('test3.txt')

  clients[10001].download('test2.txt')

  clients[10002].download('test1.txt')

  clients[10003].download('test3.txt')

  clients[10004].download('test1.txt')
  clients[10004].download('test3.txt')

if __name__== "__main__":
  tracker_thread = Thread(target=run_tracker_simulation)
  tracker_thread.start()

  for i in range(NUM_CLIENTS):
    client_id = 10000 + i
    client_thread = Thread(target=initialise_client, args=[client_id])
    client_thread.start()

  time.sleep(1)

  run_client_simulation()

  for i in range(NUM_CLIENTS):
    client = clients[10000 + i]
    client.disconnect()

  time.sleep(5)
  kill_tracker_thread = Thread(target=Tracker.kill_self())
  kill_tracker_thread.start()