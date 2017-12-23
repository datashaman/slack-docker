# slack-docker

A simple integration of docker events and slack messaging.

## Installation

Set environment variables:

* SLACK_TOKEN 
* DOCKER_HOST - Optional. See docker CLI documentation.

```
mkvirtualenv -p /usr/bin/python3 -r requirements.txt
cp config.yml.example config.yml
vim config.yml
python app.py
```
