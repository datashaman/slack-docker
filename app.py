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
        event_defn = config['events'][event['Type']]

        def match(which):
            for defn in event_defn[which]:
                (filter_type, filter_pattern) = defn.split('=')

                if filter_type == 'image' and \
                    re.search(filter_pattern,
                              event['Actor']['Attributes']['image']):
                        return True

                if filter_type == 'name' and \
                    re.search(filter_pattern,
                              event['Actor']['Attributes']['name']):
                        return True
            return False

        if 'only' in event_defn and not match('only'):
            continue

        if 'except' in event_defn and match('except'):
            continue

        params = {}
        params.update(config['defaults'])

        if event_defn['actions'][event['Action']]:
            params.update(event_defn['actions'][event['Action']])

        params['text'] = Template(params['text']).substitute(
            action=event['Action'],
            image=event['Actor']['Attributes'].get('image'),
            name=event['Actor']['Attributes']['name'],
            type=event['Type']
        )

        slack_client.api_call('chat.postMessage', **params)
