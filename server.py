import argparse
import threading
import configparser
import yt_api, list_api, query_api
from flask import Flask, render_template, request
from flask_paginate import get_page_args, Pagination

app = Flask(__name__)
app.template_folder = 'dashboard_templates/'

# Get video based on Page - Pagination
def get_current_videos(offset=0, number_of_videos=9, videos=[]):
    """
    Function to get the videos to display per page
    
    :param offset: Offset value
    :param number_of_videos: Number of videos per page
    :param videos: Data of all vides

    <return list>
    """

    return videos[offset: offset + number_of_videos]


@app.route('/')
def homepage():
    """
    Function to get the videos to display in homepage

    <return template>
    """
    total, videos = list_api.get_videos()

    # Get current page from UI
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    
    # Get list of pages to display
    current_page_videos = get_current_videos(offset=offset, number_of_videos=per_page, videos=videos)
    pagination_obj = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    # Render the HTML
    return render_template('dashboard_list.html',
                           videos=current_page_videos,
                           page=page,
                           per_page=per_page,
                           pagination=pagination_obj,
                           )


@app.route('/search')
def search_bar():
    """
    Function to display the search bar

    <return template>
    """
    return render_template('search_bar.html')


@app.route('/search', methods=['POST'])
def search_api():
    """
    Function to get the search results based on search_bar function
    
    :param text: POST Data - Words to search for

    <return template>
    """
    text = request.form['text']

    # Get the Match/Search results
    results = query_api.get_word_search_results(text)

    return render_template('search_results.html',
                            videos=results)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--search', help='Search term', default='Cooking')
  parser.add_argument('--limit', help='Number of result to be limited to', default=10)
  parser.add_argument('--date', help="Videos published after:", default='2021-01-01T00:12:10Z')
  parser.add_argument('--interval', help="Refresh the DB for every n seconds:", default=100)
  args = parser.parse_args()

  # Read the config
  configParser = configparser.RawConfigParser()   
  configParser.read('./.env')

  # Read multiple api keys to support fail over case of Quota exceeded
  api_keys = configParser.get('config', 'api_key').split(',')
  service, version = configParser.get('config', 'service'), configParser.get('config', 'version')

  # Async
  threads = threading.Thread(target=yt_api.driver, args=(api_keys, service, version, args))
  threads.start()
  print("----------SERVER: YT API Fetch Call Started - Will be executed every 10 secs:", threads.is_alive())

  # Run the server
  app.run(debug=True, port=8080)
