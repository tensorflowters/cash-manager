
#!/bin/bash

docker login --username $DOCKER_HUB_USER --password $DOCKER_HUB_PASS
sudo curl -L https://raw.githubusercontent.com/docker/compose-cli/main/scripts/install/install_linux.sh | sudo sh
sudo docker-compose -f docker-compose.yml build
sudo docker-compose -f docker-compose.yml push
sudo docker context create ecs deploy-phoenix --from-env
sudo docker context use deploy-phoenix
sudo docker compose -f docker-compose.dev.yml up
echo "test"
echo "test"
