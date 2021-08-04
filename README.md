# FamPay YT API
An E2E project built on Flask Python to fetch, save and display videos asynchronously from Youtube

## Features
1. A backend server that asynchronously fetches and saves latest video for a given search query and save it in Database SQL Lite
2. Duplications are removed and sorted in reverse chronological order
3. Can take input of multiple API Keys for fail-over cases of resource quota exceeded
4. A GET API that responds in a paginated manner to list all the videos stored
5. A Search API that can handle complex scenarios like "How to make tea", "Tea How?", "Make Tea!"
6. Paginated Dashboard to view the list of videos, also diffent dashboard for search queris and search results
7. Fully documented and commented code.

## Architecture

