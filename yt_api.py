import time
import pandas as pd
import sqlite3 as sql
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def store_data(new_videos):
  # Connect to database and get already saved video data
  table_name = "videos_check"
  conn = sql.connect(table_name)
  try:
    old_videos = pd.read_sql('select * from {0}'.format(table_name), conn)
  except Exception as e:
    print("----------SERVER: Creating new table")
    old_videos = pd.DataFrame(data=[], columns=list(new_videos.columns))
  
  # Append the new videos, de-duplication and sorting
  videos = old_videos.append(new_videos)
  videos.drop_duplicates(subset="id", keep="first", inplace=True)
  videos['datetime_obj'] = videos['publishTime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
  videos.sort_values(by='datetime_obj', ascending=False, inplace=True)

  # Save a backup of data to disk
  videos.to_csv("./data/{0}.csv".format(str(time.time())), index=False)
  videos.to_sql(table_name, conn, if_exists="append", index=False)

  conn.commit()
  conn.close()
  return 

def search_keyword(args, api_key, service, version):
  youtube_api = build(service, version, developerKey=api_key)

  # Search the youtube for related word/query
  response = youtube_api.search().list(q=args.search, part='id,snippet',
                                type='video', order='date', maxResults=args.limit,
                                publishedAfter=args.date).execute()

  videos_data = []

  # Store data and fields related to videos
  for item in response.get('items', []):
    videos_data.append({
      "id": item['id']['videoId'],
      "title": item['snippet']['title'],
      "description": item['snippet']['description'],
      "publishTime": item['snippet']['publishTime'],
      "url":  "https://www.youtube.com/watch?v=" + item['id']['videoId'],
      "thumbnail_small": item['snippet']['thumbnails']['default']['url'],
      "thumbnail_medium": item['snippet']['thumbnails']['medium']['url'],
      "thumbnail_high": item['snippet']['thumbnails']['high']['url'],
    })
  
  df_videos = pd.DataFrame(videos_data)
  return df_videos

def driver(api_keys, service, version, args):
  # Failover case for api keys
  for api_key in api_keys:
      try:
        while True:
          videos_data = search_keyword(args, api_key, service, version)
          print("----------SERVER: Successfully fetched data from YT API!!")
          store_data(videos_data)
          print("----------SERVER: Successfully saved data to DB")
          time.sleep(args.interval)
          continue
      except HttpError as e:
        print('Error %d Probable Limit/Quota exceeded: %s' % (e.resp.status, e.content))
        continue
