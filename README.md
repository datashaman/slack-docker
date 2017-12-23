# slack-docker

A simple integration of docker events and slack messaging.

## Configure

Set the following variables in the environment:

* SLACK_TOKEN 
* DOCKER_HOST - Optional. See docker CLI documentation.

Create a config file from the example:

```
mkvirtualenv -p /usr/bin/python3 -r requirements.txt
cp config.yml.example config.yml
vim config.yml
```

## Serve

```
python app.py
```
