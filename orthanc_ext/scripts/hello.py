import logging

def hello_world(info, _client):
  version = info.get('Version')
  logging.warning(f'Hello World! Inside the function. Version is: "{version}"',)