import sys
import socket as s

from file_splitter import *
from config import SOCK_CONFIG, MESSAGES
from logger import Logger
import hashlib

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
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], SOCK_CONFIG['REGISTRATION_PORT'])

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)
    message = self.construct_message(MESSAGES['REGISTER_CLIENT'])
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

  def get_active_peers(self):
    # get active peers by asking the tracker
    return []

  def send_to_peer(self, peer_port, file):
    peer_address = (SOCK_CONFIG['ADDRESS'], peer_port)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(peer_address)
    sock.send(file.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')

    if response == MESSAGES['REGISTER_ACK']:
      self.log('succesfully sent file chunk')
      sock.close()
    else:
      self.log('unsuccessfully sent file chunk')
      sock.close()
      raise RuntimeError

  def upload(self, file_location):
    file = open(file_location,'rb').read()
    file_digest = hashlib.md5(file).hexdigest()

    tracker_address = (SOCK_CONFIG['ADDRESS'], SOCK_CONFIG['REGISTER_PORT'])
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)

    message = self.construct_message(MESSAGES['UPLOAD_FILE'], [file_digest])
    self.log(message)
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')

    if response == MESSAGES['UPLOAD_ACK']:
      self.log('succesfully notified tracker')
      sock.close()
    else:
      self.log('unsuccessfully notified tracker')
      sock.close()
      raise RuntimeError

  def download(self, file_id):
    peers = self.get_active_peers(file_id)
    # connect to those peers and download all parts
    # reorder parts

  def get_active_peers(self, file_id):
    tracker_address = (SOCK_CONFIG['ADDRESS'], SOCK_CONFIG['REGISTER_PORT'])
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)

    message = self.construct_message(MESSAGES['DOWNLOAD_FILE'], [file_id])
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8').splitlines()

    if response[0] == MESSAGES['DOWNLOAD_ACK']:
      active_peers = response[1]
      self.log('successfully obtained active peers from tracker:', active_peers)
      sock.close()
      return active_peers
    
    else:
      self.log('unable to obtain active peers from tracker')
      sock.close()
      raise RuntimeError

  def reorder_parts(self, parts):
    # sort parts of files by some index
    # combine parts
    pass

  def construct_message(self, op, messages = []):
    # messages is an array
    return ('\n').join([op, self.id] + messages)