import json
import string
from collections import defaultdict
import pandas as pd
import sqlite3 as sql

def get_match_scores(words, titles, ids):
    scores = defaultdict(int)
    print("words,t", words, titles)
    for word in words:
        for title, id in zip(titles, ids):
            if word in title:
                scores[id] += 1 
    print("scores", scores)
    return scores
                

def get_best_match(text, titles, ids):
    scores = get_match_scores(text.split(' '), titles, ids)
    scores = {k: v for k,v in sorted(scores.items(), key=lambda item:item[1])}
    ids_matched = [x for x,y in scores.items() if y > 0][:9]
    return ids_matched


def get_word_search_results(text):
  table_name = "videos_check"
  conn = sql.connect(table_name)
  videos = pd.read_sql('select * from {0}'.format(table_name), conn)
  videos.drop_duplicates(keep='first', inplace=True, subset='id')
  conn.close()

  text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).lower()
  print("After process", text)

  titles = [x.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).lower() for x in videos['title'].tolist()]
  ids = videos['id'].tolist()

  ids_matched = get_best_match(text, titles, ids)
  videos = videos[videos['id'].isin(ids_matched)]
  return json.loads(videos.to_json(orient ='records'))