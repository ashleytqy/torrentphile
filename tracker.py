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
    self.registration_port = SOCK_CONFIG['REGISTRATION_PORT']
    self.address = SOCK_CONFIG['TRACKER_ADDRESS']
    self.clients = {}
    self.sock = None
    # mapping the hex digest of a file to the clients that current have it
    self.file_to_client = {}

    self.connect_clients()

  # continually listen on a port for any incoming client requests to connect 
  def connect_clients(self):
    self.registration_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.registration_sock.bind((self.address, self.registration_port))
    self.registration_sock.listen(0)

    while True:
      thread = Thread(target=self.connect_client)
      thread.start()
      thread.join()

  def connect_client(self):
    registration_conn = self.registration_sock.accept()[0]
    response = registration_conn.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')
    command = response.split(' ')[0]

    if command != MESSAGES['REGISTER_CLIENT']:
      registration_conn.close()
    else:
      # client_id is also the client's port number
      # in a real application, the client_id would be its address, but since we're running
      # everything on one machine, this isn't feasible
      client_id = response.split(' ')[1]
      client_config = {
        'address': SOCK_CONFIG['CLIENT_ADDRESS'],
        'port': int(client_id),
      }
      self.clients[client_id] = client_config

      self.log('registered', client_id)
      registration_conn.send(MESSAGES['REGISTER_ACK'].encode('utf-8'))
      registration_conn.close()
      
      client_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
      client_config['sock'] = client_sock

      client_sock.bind((client_config['address'], client_config['port']))
      client_sock.listen(0)
      client_conn = client_sock.accept()[0]

      while True:
        response = client_conn.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')
        command = response.split(' ')[0]

        if command == MESSAGES['UPLOAD_FILE']:
          self.process_upload(client_id, client_conn, response)

        elif command == MESSAGES['DOWNLOAD_FILE']:
          self.process_download(client_id, client_conn, response)

        elif command == MESSAGES['DISCONNECT']:
          client_conn.close()
          break

  def process_upload(self, client_id, client_conn, response):3
    self.file_to_client[file_uuid] = [client_id]
    message = MESSAGES['UPLOAD_ACK']

    client_conn.send(message.encode('utf-8'))

  def process_download(self, client_conn, arguments):
    file_uuid = arguments
    message = MESSAGES['DOWNLOAD_ACK']
    for node in self.file_to_client[file_uuid]:
      message.append("\n" + node)

    client_conn.send(message.encode('utf-8'))

  