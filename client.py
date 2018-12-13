import sys
import socket as s

from file_splitter import *
from config import SOCK_CONFIG, MESSAGES
from logger import Logger
import hashlib
from os import listdir
from os.path import isfile, join

class Client:
  def __init__(self, port_number, enable_logging=False):
    
    self.port_number = port_number
    self.id = str(port_number)
    self.log = Logger('Client ' + self.id, enable_logging).log
    self.registered = False

    self.directory = '/tmp/' + str(port_number)
    self.file_splitter = FileSplitter()

    # when we initialise a client, we automatically inform the tracker
    # i.e. we initialise a connection to the tracker server
    self.register()

  def register(self):
    registration_address = (SOCK_CONFIG['TRACKER_ADDRESS'], SOCK_CONFIG['REGISTRATION_PORT'])
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(registration_address)
    message = MESSAGES['REGISTER_CLIENT'] + ' ' + self.id
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')

    if response == MESSAGES['REGISTER_ACK']:
      self.log('succesfully registered')
      self.registered = True
      sock.close()
    else:
      self.log('unsuccessfully registered with response', response)
      sock.close()
      raise RuntimeError

  # tmp/client1/test.txt will be split into tmp/client1/test/1.txt..10.txt
  def upload(self, file_location):
    # assumption: file has to be within /tmp/:client_id/
    full_path = self.directory + '/' + file_location
    file_name, file_ext = os.path.splitext(file_location)
    file_chunks = self.file_splitter.split(self.directory, 'test.txt')

    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)

    message = self.construct_message(MESSAGES['UPLOAD_FILE'], [file_location])
    # sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8').split(' ')

    if response == MESSAGES['UPLOAD_ACK']:
      self.log('succesfully notified tracker')
      sock.close()
    else:
      self.log('unsuccessfully notified tracker')
      sock.close()
      raise RuntimeError

  def download(self, file_id):
    peers = self.get_active_peers(file_id)
    self.log('active peers', peers)
    # connect to those peers and download all parts
    for peer in peers:
      self.send_to_peer(peer, file_id)

    # reorder parts


  def get_active_peers(self, file_id):
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)

    message = self.construct_message(MESSAGES['DOWNLOAD_FILE'], [file_id])
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8').split(' ')

    if response[0] == MESSAGES['DOWNLOAD_ACK']:
      active_peers = response[1]
      self.log('successfully obtained active peers from tracker:', active_peers)
      sock.close()
      return active_peers
    
    else:
      self.log('unable to obtain active peers from tracker')
      sock.close()
      raise RuntimeError

  def send_to_peer(self, peer_port, file):
    peer_address = (SOCK_CONFIG['CLIENT_ADDRESS'], peer_port)
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

  def disconnect(self):
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)
    message = MESSAGES['DISCONNECT']
    sock.send(message.encode('utf-8'))


  # call this method after client has successfully downloaded all chunks
  # and stored all the chunks in its folder
  # pass in the name of the file you want to save it in
  def reorder_and_combine_chunks(self, file_name, new_file_path):
    # get all files in the right directory
    # after a client downloads, all the chunks will live in /tmp/:port/:name/1..100
    # path = self.directory + '/' + file_name
    path, file_ext = os.path.splitext(file_name)
    self.log('path is', path)
    file_parts = [f for f in listdir(path) if isfile(join(path, f))]

    with open(self.directory + '/' + new_file_path, 'w' ) as result:
      for f in file_parts:
          for line in open(path + '/' + f, 'r' ):
              result.write(line)

    return new_file_path

  def construct_message(self, op, messages = []):
    # messages is an array
    return (' ').join([op, self.id] + messages)