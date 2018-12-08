from threading import Thread

from client import Client
from tracker import Tracker

NUM_CLIENTS = 5

def run_tracker_simulation():
  print('starting tracker simulation')
  tracker = Tracker(True)

def run_client_simulation():
  print('starting client simulation')

  for i in range(NUM_CLIENTS):
    client = Client(10000 + i, True)

if __name__== "__main__":
  tracker_thread = Thread(target=run_tracker_simulation)
  client_thread = Thread(target=run_client_simulation)

  tracker_thread.start()
  client_thread.start()