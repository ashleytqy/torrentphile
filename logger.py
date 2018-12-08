class Logger:
  def __init__(self, client, is_enabled):
    self.client = client
    self.is_enabled = is_enabled

  def log(self, *messages):
    if self.is_enabled:
      print(self.client + ':', ' '.join([str(message) for message in messages]))