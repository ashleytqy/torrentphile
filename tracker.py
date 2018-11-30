class Tracker:
  def __init__(self, port_number = 8000):
    self.port_number = port_number
    self.active_clients = []

  # continually listen on a port for any incoming client requests to connect 
  def listen(self):
    pass
  
  # register incoming clients
  def register(self, client_id):
    self.active_clients.append(client_id)

  def get_clients_for_file(self, file):
    pass

