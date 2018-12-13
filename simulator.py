from threading import Thread

from client import Client
from tracker import Tracker
from random import randint

NUM_CLIENTS = 5
clients = {} # map client id to the actual client object

def run_tracker_simulation():
  print('starting tracker simulation')
  tracker = Tracker(True)

def run_client_simulation():
  print('starting client simulation')

  for i in range(NUM_CLIENTS):
    id = 10000 + i
    client = Client(id, True)
    clients[id] = client

  # simulate an upload
  # random_id = randint(10000, 10000 + NUM_CLIENTS - 1)
  # uploader = clients[random_id]
  # file_location = '/tmp/test.txt'
  # uploader.upload(file_location)

  # random_id = randint(10000, 10000 + NUM_CLIENTS - 1)
  # downloader = clients[random_id]
  # print(downloader)
  # downloader.download('f0f0f8e489652435c38caa6e53b7b749')


if __name__== "__main__":
  tracker_thread = Thread(target=run_tracker_simulation)
  client_thread = Thread(target=run_client_simulation)

  tracker_thread.start()
  client_thread.start()