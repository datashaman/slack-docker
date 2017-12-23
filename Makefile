TAG = datashaman/docker-slack

build:
	docker build . -t $(TAG)

run:
	docker run -it --rm -e SLACK_TOKEN=${SLACK_TOKEN} -v ${PWD}/config.yml:/var/app/config.yml -v /var/run/docker.sock:/var/run/docker.sock $(TAG)
