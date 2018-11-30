class Client:
  def __init__(self, port_number):
    self.port_number = port_number
    self.folder = '/tmp/' + port_number

  def upload(self, file_location):
    pass

  def download(self, file_id):
    # first, talk to tracker and get the info
    # about which peers to get the file from

    # then connect to those peers and download all parts
    # reorder parts
    pass

  def reorder_parts():
    pass