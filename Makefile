up_dev:
	sudo docker-compose -f docker-compose.yaml up
down_dev:
	sudo docker-compose -f docker-compose.yaml down
up_test:
	sudo docker-compose -f docker-compose.fortest.yaml up
down_test:
	sudo docker-compose -f docker-compose.fortest.yaml down
prune:
	sudo docker system prune -af --volumes
