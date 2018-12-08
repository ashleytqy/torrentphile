import sys
from socket import *

from file_splitter import *

class Client:
  def __init__(self, port_number):
    self.port_number = port_number
    self.folder = '/tmp/' + port_number
    self.file_splitter = FileSplitter()

    # shoud we have only 1 socket for this client, or 1 socket per peer?

    # list of peers it is connected to
    # peers need to know what pieces of the content each peer in its peer set has
    self.peer_set = []

    # leecher state: it is still downloading the file while uploading pieces it has to other leechers
    # seed state: it has the complete file and is uploading to leechers
    self.state = None

    # when we initialise a client, we automatically inform the tracker
    # i.e. we initialise a connection to the tracker server
    self.notify_tracker()

  def notify_tracker(self, port = 8000):
    tracker_address = ("127.0.0.1", 8000)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(tracker_address)
    message = 'hello from client!'
    sock.send(message.encode("utf-8"))
    print("sent: " + message + "\n")
    # if recieved an ack, return True, else False / throw an error?
    # leave it to init.py to catch the error
    # sock.close()

  def connect(self, peer):
    # first establish the connection
    # peer ==> port
    peer_address = ("127.0.0.1", peer)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(peer_address)
    message = 'hello from client!'
    sock.send(message.encode("utf-8"))
    print("sent: " + message + "\n")

    # if connection is successful, add peer to peer set
    self.peer_set.append(peer)

  def upload(self, file_location):
    files = self.file_splitter.split(file_location)
    # split file into equal parts
    # get all active peers
    # distribute file parts to specific peers

  def download(self, file_id):
    # first, talk to tracker and get the info
    # about which peers to get the file from

    # then connect to those peers and download all parts
    # reorder parts
    pass

  def reorder_parts(parts):
    # sort parts of files by some index
    # combine parts
    pass