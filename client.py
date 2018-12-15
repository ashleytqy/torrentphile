import sys
import socket as s
import time
from threading import Thread

from config import SOCK_CONFIG, MESSAGES
from logger import Logger


class Client:
  def __init__(self, port_number, enable_logging=False):
    self.port_number = port_number
    self.id = str(port_number)
    self.log = Logger('Client ' + self.id, enable_logging).log
    self.registered = False
    self.directory = '/tmp/' + str(port_number)
    self.uploaded_files = []
    self.kill = False
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

      listen_to_peers_thread = Thread(target=self.listen_to_peers)
      listen_to_peers_thread.start()
    else:
      self.log('unregistered with response', response)
      sock.close()
      raise RuntimeError

  def listen_to_peers(self):
    peer_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    peer_sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    # we have to add 10000 to the port number because CLIENT_ADDRESS == TRACKER_ADDRESS when running on one machine
    # and the tracker is listening to (TRACKER_ADDRESS, self.port_number)
    peer_sock.bind((SOCK_CONFIG['CLIENT_ADDRESS'], self.port_number + SOCK_CONFIG['PEER_PORT_INCREMENT']))
    peer_sock.listen(10)

    while True:
      peer_conn = peer_sock.accept()[0]
      response = peer_conn.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')

      if response == MESSAGES['KILL_CLIENT']:
        self.process_kill()
      elif response in self.uploaded_files:
        self.log('received download request for', response)
        file = open(self.directory + '/' + response)
        
        chunk = file.read(SOCK_CONFIG['DATA_SIZE'])

        while chunk:
          peer_conn.send(chunk.encode('utf-8'))
          chunk = file.read(SOCK_CONFIG['DATA_SIZE'])

        file.close()
        self.log('finished sending file')
        peer_conn.send(MESSAGES['DOWNLOAD_END'].encode('utf-8'))

      peer_conn.close()

      if self.kill:
        break

  def upload(self, file_name):
    # assumption: file has to be within /tmp/:client_id/
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)

    message = self.construct_message(MESSAGES['UPLOAD_FILE'], [file_name])
    sock.send(message.encode('utf-8'))
    response = sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')

    if response == MESSAGES['UPLOAD_ACK']:
      self.uploaded_files.append(file_name)
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
      peer_address = (SOCK_CONFIG['CLIENT_ADDRESS'], peer_port + SOCK_CONFIG['PEER_PORT_INCREMENT'])
      peer_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
      peer_sock.connect(peer_address)

      file = open(self.directory + '/' + file_name, 'w')
      self.log('downloading', file_name, 'from', peer_port)
      peer_sock.send(file_name.encode('utf-8'))

      while True:
        chunk = peer_sock.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')

        if chunk == MESSAGES['DOWNLOAD_END']:
          break
        else:
          file.write(chunk)

      file.close()

      self.log('downloaded', file_name, 'from client', peer_port)
      self.upload(file_name)

  def disconnect(self):
    tracker_address = (SOCK_CONFIG['TRACKER_ADDRESS'], self.port_number)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(tracker_address)
    message = MESSAGES['DISCONNECT']
    sock.send(message.encode('utf-8'))
    sock.close()

    self.kill_self()
    self.log('disconnected')

  def construct_message(self, op, messages = []):
    # messages is an array
    messages = [str(m) for m in messages]
    return (' ').join([op] + messages)

  def process_kill(self):
    self.kill = True

  def kill_self(self):
    listen_to_peers_address = (SOCK_CONFIG['CLIENT_ADDRESS'], self.port_number + SOCK_CONFIG['PEER_PORT_INCREMENT'])
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect(listen_to_peers_address)
    message = MESSAGES['KILL_CLIENT']
    sock.send(message.encode('utf-8'))