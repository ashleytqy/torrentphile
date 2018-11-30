import sys
import os
from socket import *

class Tracker:
  def __init__(self, port_number = 8000):
    self.debug = True
    self.port_number = int(port_number)
    self.address = "127.0.0.1"
    self.active_clients = []
    self.sock = None

    self.listen()

  # continually listen on a port for any incoming client requests to connect 
  def listen(self):
    self.sock = socket(AF_INET, SOCK_DGRAM)
    self.sock.bind((self.address, self.port_number))

    while True:
      data, address = self.sock.recvfrom(1024)
      data = data.decode("utf-8")
      print("argument is " + data)
      self.sock.sendto(str.encode('hihihi'), address)

  # register incoming clients
  def register(self, client_id):
    self.active_clients.append(client_id)

  def get_clients_for_file(self, file):
    pass

