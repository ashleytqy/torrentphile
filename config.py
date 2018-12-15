SOCK_CONFIG = {
  'REGISTRATION_PORT': 8000,
  'TRACKER_ADDRESS': '127.0.0.1',
  'CLIENT_ADDRESS': '127.0.0.1',
  'DATA_SIZE': 1024,
  'PEER_PORT_INCREMENT': 10000,
}

MESSAGES = {
  'REGISTER_ACK': 'ack',
  'REGISTER_CLIENT': 'register_client',
  'UPLOAD_FILE': 'upload_file',
  'UPLOAD_ACK': 'upload_ack',
  'DOWNLOAD_FILE': 'download_file',
  'DOWNLOAD_ACK': 'download_ack',
  'NONEXISTENT_FILE': 'nonexistent_file',
  'DISCONNECT': 'disconnect',
  'KILL_TRACKER': 'kill_tracker',
  'KILL_CLIENT': 'kill_client',
  'DOWNLOAD_END': 'download_end',
}