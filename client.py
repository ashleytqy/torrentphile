import sys
import socket as s
import time

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
      self.log('registered')
      self.registered = True
      sock.close()

      
    else:
      self.log('unregistered with response', response)
      sock.close()
      raise RuntimeError

  def listen_to_peers(self):

  def upload(self, file_name):
    # assumption: file has to be within /tmp/:client_id/
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)

    message = self.construct_message(MESSAGES['UPLOAD_FILE'], [file_name])
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')

    if response == MESSAGES['UPLOAD_ACK']:
      self.log('uploaded', file_name, 'to tracker')
    else:
      self.log('failed to upload to tracker')
      raise RuntimeError

  def download(self, file_name):
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)

    message = self.construct_message(MESSAGES['DOWNLOAD_FILE'], [file_name])
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')
    
    if response == MESSAGES['NONEXISTENT_FILE']:
      self.log('failed to download non-existent', file_name)
    else:
      peer_port = int(response)
      self.log('downloaded', file_name, 'from client', peer_port)

  def get_active_peers(self, file_id):
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)

    message = self.construct_message(MESSAGES['DOWNLOAD_FILE'], [file_id])
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8').split(' ')

    if response[0] == MESSAGES['DOWNLOAD_ACK']:
      active_peers = response[1]
      self.log('obtained active peers from tracker:', active_peers)
      sock.close()
      return active_peers
    
    elif response[0] == MESSAGES['NONEXISTENT_FILE']:
      self.log('file does not exist')
      sock.close()
      return []
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
      self.log('sent file chunk')
      sock.close()
    else:
      self.log('unsent file chunk')
      sock.close()
      raise RuntimeError

  def disconnect(self):
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)
    message = MESSAGES['DISCONNECT']
    sock.send(message.encode('utf-8'))
    sock.close()

    self.log('disconnected')

  # call this method after client has downloaded all chunks
  # and stored all the chunks in its folder
  # the saved file path would be the file_name_[epoch time]
  def reorder_and_combine_chunks(self, file_name):
    # get all files in the right directory
    # after a client downloads, all the chunks will live in /tmp/:port/:name/1..100
    # path = self.directory + '/' + file_name
    path, file_ext = os.path.splitext(file_name)
    self.log('path is', path)
    file_parts = [f for f in listdir(path) if isfile(join(path, f))]

    new_file_path = file_name + '_' + str(int(time.time()))
    with open(self.directory + '/' + new_file_path, 'w' ) as result:
      for f in file_parts:
          for line in open(path + '/' + f, 'r' ):
              result.write(line)

    return new_file_path

  def construct_message(self, op, messages = []):
    # messages is an array
    messages = [str(m) for m in messages]
    return (' ').join([op] + messages)