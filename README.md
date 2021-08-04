# FamPay YT API
An E2E project built on Flask Python to fetch, save and display videos asynchronously from Youtube

## Video Demo
Please watch this short video for 3 Minutes, of working code showcase
https://youtu.be/SMNbI6pp7Fc

## Features
1. A backend server that asynchronously fetches and saves latest video for a given search query and save it in Database SQL Lite. Also, saves a backup on the disk.
2. Duplications are removed and sorted in reverse chronological order
3. Can take input of multiple API Keys for fail-over cases of resource quota exceeded
4. A GET API that responds in a paginated manner to list all the videos stored
5. A Search API that can handle complex scenarios like "How to make tea", "Tea How?", "Make Tea!"
6. Paginated Dashboard to view the list of videos, also diffent dashboard for search queris and search results
7. Fully documented and commented code.
8. Docker Containerized

## Architecture
![WhatsApp Image 2021-08-04 at 08 25 53](https://user-images.githubusercontent.com/29350756/128118905-288b6797-c969-476d-b5b5-075c6d798e84.jpeg)


## Futher Scope
Things I though of doing, but couldn't due to time constraints
1. Implementing Word2Vec in Search API, so that we can match even synonyms.
2. Better dashboad using Bootstrap

I enjoyed doing this project. Thanks for the team at FamPay!
Thanks & Cheer!
