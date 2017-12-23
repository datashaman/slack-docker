import docker
import os
import yaml

from slackclient import SlackClient
from string import Template


with open('config.yml', 'r') as f:
    config = yaml.load(f)

docker_client = docker.from_env()
slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))

for event in docker_client.events(decode=True):
    if event['Type'] in config['events'] and \
            event['Action'] in config['events'][event['Type']]:
        params = {}
        params.update(config['defaults'])

        if config['events'][event['Type']][event['Action']]:
            params.update(config['events'][event['Type']][event['Action']])

        params['text'] = Template(params['text']).substitute(
            action=event['Action'],
            image=event['Actor']['Attributes'].get('image'),
            name=event['Actor']['Attributes']['name'],
            type=event['Type']
        )

        slack_client.api_call('chat.postMessage', **params)
