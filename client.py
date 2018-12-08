import sys
import socket as s

from file_splitter import *
from config import SOCK_CONFIG, MESSAGES
from logger import Logger

class Client:
  def __init__(self, port_number, enable_logging=False):
    
    self.port_number = port_number
    self.id = str(port_number)
    self.log = Logger('Client ' + self.id, enable_logging).log
    self.registered = False
    # so we don't alter system files. only compatible for MacOS
    self.folder = '/~/tmp/' + str(port_number)
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
    self.register()
    

  def register(self):
    tracker_address = (SOCK_CONFIG['ADDRESS'], SOCK_CONFIG['REGISTER_PORT'])
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)
    message = 'registering ' + self.id
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')

    if response == MESSAGES['REGISTER_ACK']:
      self.log('succesfully registered')
      self.registered = True
      sock.close()
    else:
      self.log('unsuccessfully registered')
      sock.close()
      raise RuntimeError

  def connect(self, peer):
    # first establish the connection
    # peer ==> port
    peer_address = ("127.0.0.1", peer)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(peer_address)
    message = 'registering ' + self.id
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

  def reorder_parts(self, parts):
    # sort parts of files by some index
    # combine parts
    pass