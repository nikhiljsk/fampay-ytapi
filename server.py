import yt_api
import argparse
import threading
import configparser

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--search', help='Search term', default='Cooking')
  parser.add_argument('--limit', help='Number of result to be limited to', default=10)
  parser.add_argument('--date', help="Videos published after:", default='2021-01-01T00:12:10Z')
  args = parser.parse_args()

  configParser = configparser.RawConfigParser()   
  configParser.read('./.env')

  api_keys = configParser.get('config', 'api_key').split(',')
  service, version = configParser.get('config', 'service'), configParser.get('config', 'version')

  threads = threading.Thread(target=yt_api.driver, args=(api_keys, service, version, args))
  threads.start()
  print("----------SERVER: YT API Fetch Call Started - Will be executed every 10 secs:", threads.is_alive())
#   yt_api.driver(api_keys, service, version, args)
  