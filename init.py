import argparse

def run():
  parser = argparse.ArgumentParser(description='stuff.')
  parser.add_argument('--type', help='client or server')
  parser.add_argument('--port', help='port to run on')

  args = parser.parse_args()

if __name__== "__main__":
  run()