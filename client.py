class Client:
  def __init__(self, port_number):
    self.port_number = port_number
    self.folder = '/tmp/' + port_number

    # list of peers it is connected to
    # peers need to know what pieces of the content each peer in its peer set has
    self.peer_set = []

    # leecher state: it is still downloading the file while uploading pieces it has to other leechers
    # seed state: it has the complete file and is uploading to leechers
    self.state = None

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