import docker
import os
import re
import yaml

from slackclient import SlackClient
from string import Template


with open('config.yml', 'r') as f:
    config = yaml.load(f)

docker_client = docker.from_env()
slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))

for event in docker_client.events(decode=True):
    if event['Type'] in config['events'] and \
            event['Action'] in config['events'][event['Type']]['actions']:
        skip = False

        if 'except' in config['events'][event['Type']]:
            for defn in config['events'][event['Type']]['except']:
                (filter_type, filter_pattern) = defn.split('=')

                if filter_type == 'name':
                    if re.search(filter_pattern,
                                 event['Actor']['Attributes']['name']):
                        skip = True
                        continue

        if not skip:
            params = {}
            params.update(config['defaults'])

            if config['events'][event['Type']]['actions'][event['Action']]:
                params.update(config['events'][event['Type']]['actions'][event['Action']])

            params['text'] = Template(params['text']).substitute(
                action=event['Action'],
                image=event['Actor']['Attributes'].get('image'),
                name=event['Actor']['Attributes']['name'],
                type=event['Type']
            )

            slack_client.api_call('chat.postMessage', **params)
