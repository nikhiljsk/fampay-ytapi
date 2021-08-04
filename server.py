import argparse
import threading
import configparser
import yt_api, list_api, query_api
from flask import Flask, render_template, request
from flask_paginate import get_page_args, Pagination

app = Flask(__name__)
app.template_folder = 'dashboard_templates/'


def get_current_videos(offset=0, number_of_videos=9, videos=[]):
    return videos[offset: offset + number_of_videos]


@app.route('/')
def homepage():
    total, videos = list_api.get_videos()
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    current_page_videos = get_current_videos(offset=offset, number_of_videos=per_page, videos=videos)
    pagination_obj = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('dashboard_list.html',
                           videos=current_page_videos,
                           page=page,
                           per_page=per_page,
                           pagination=pagination_obj,
                           )


@app.route('/search')
def search_bar():
    return render_template('search_bar.html')


@app.route('/search', methods=['POST'])
def search_api():
    text = request.form['text']
    results = query_api.get_word_search_results(text)
    return render_template('search_results.html',
                            videos=results)


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

  app.run(debug=True, port=8080)
