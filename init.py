import argparse
from client import *
from tracker import *

def run():
  parser = argparse.ArgumentParser(description='stuff.')
  parser.add_argument('--type', help='client or tracker', choices=['client', 'tracker'])
  parser.add_argument('--port', help='port to run on')
  parser.add_argument('--file', help='path of file to upload')

  args = parser.parse_args()

  if args.type == 'client':
    client = Client(args.port)
    client.upload(args.file)
  else:
    tracker = Tracker()


if __name__== "__main__":
  run()