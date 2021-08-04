import json
import pandas as pd
import sqlite3 as sql


def get_videos():
  # Get videos from existing database
  table_name = 'videos_check'
  conn = sql.connect(table_name)
  videos = pd.read_sql('select * from {0}'.format(table_name), conn)
  videos.drop_duplicates(keep='first', inplace=True, subset='id')
  return len(videos), json.loads(videos.to_json(orient ='records'))