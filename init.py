import argparse
from client import *
from tracker import *

def run():
  parser = argparse.ArgumentParser(description='stuff.')
  parser.add_argument('--type', help='client or tracker', choices=['client', 'tracker'])
  parser.add_argument('--port', help='port to run on')

  args = parser.parse_args()

  if args.type == 'client':
    client = Client(args.port)
  else:
    tracker = Tracker(args.port)


if __name__== "__main__":
  run()