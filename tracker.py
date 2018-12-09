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
    response = conn.recv(SOCK_CONFIG['DATA_SIZE']).decode('utf-8')
    client_id = response.split(' ')[1]
    self.clients.append(client_id)
    self.log('registered', client_id)
    conn.send(MESSAGES['REGISTER_ACK'].encode('utf-8'))
    conn.close()

  def get_clients_for_file(self, file):
    pass

