import sys
import os
from socket import *

DATA_SIZE = 1024

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
    self.sock = socket(AF_INET, SOCK_STREAM)
    self.sock.bind((self.address, self.port_number))
    self.sock.listen(0)
    print('hlo')

    while True:
      sender_socket, sender_addr = self.sock.accept()
      data, address = sender_socket.recv(DATA_SIZE).decode("utf-8")
      print("argument is " + data)
      self.sock.sendto(str.encode('ack.'), address)

  # register incoming clients
  def register(self, client_id):
    self.active_clients.append(client_id)

  def get_clients_for_file(self, file):
    pass

