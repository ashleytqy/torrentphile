import sys
import os
import socket as s
from threading import Thread

from config import SOCK_CONFIG, MESSAGES
from logger import Logger

class Tracker:
  def __init__(self, enable_logging=False):
    self.log = Logger('Tracker', enable_logging).log
    self.debug = True
    self.port_number = SOCK_CONFIG['REGISTER_PORT']
    self.address = SOCK_CONFIG['ADDRESS']
    self.clients = []
    self.sock = None
    # mapping the hex digest of a file to the clients that current have it
    self.file_to_client = {}

    self.process_registrations()

  # continually listen on a port for any incoming client requests to connect 
  def process_registrations(self):
    self.sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.sock.bind((self.address, self.port_number))
    self.sock.listen(0)

    while True:
      self.log('creating registration thread')
      thread = Thread(target=self.process_registration)
      thread.start()
      thread.join()
      self.log('clients', self.clients)

  def process_registration(self):
    conn = self.sock.accept()[0]
    response = conn.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8').splitlines()
    
    action = response[0]
    client_id = response[1]
    message = ''

    if action == MESSAGES['REGISTER_CLIENT']:
      self.clients.append(client_id)
      self.log('registered', client_id)
      message = MESSAGES['REGISTER_ACK']

    elif action == MESSAGES['UPLOAD_FILE']:
      file_uuid = response[2]
      self.file_to_client[file_uuid] = [client_id]
      self.log(self.file_to_client)
      message = MESSAGES['UPLOAD_ACK']

    elif action == MESSAGES['DOWNLOAD_FILE']:
      pass

    conn.send(message.encode('utf-8'))
    conn.close()