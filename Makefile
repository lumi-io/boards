start-container:
	docker stop testing_container || true && docker rm testing_container || true
	docker build -t testing_container tests
	docker run -d --name=testing_container -p 5000:5000 testing_container

test-container: start-container
	pipenv run pytest

dev-container:
	docker stop dev_container || true && docker rm dev_container || true
	docker build -t dev_container .
	docker run -d --name=dev_container -p 56733:80 dev_container


deploy-container:
	docker build \
	-t whyphi_server \
	--build-arg MONGODB_DB={{ secrets.MONGODB_DB }} \
	--build-arg MONGODB_HOST={{ secrets.MONGODB_HOST }} \
	--build-arg MONGODB_PORT={{ secrets.MONGODB_PORT }} \
	--build-arg MONGODB_USERNAME={{ secrets.MONGODB_USERNAME }} \
	--build-arg MONGODB_PASSWORD={{ secrets.MONGODB_PASSWORD }} \
	--no-cache .
	docker tag whyphi_server:latest 280776660572.dkr.ecr.us-east-2.amazonaws.com/whyphi_server:latest
	docker push 280776660572.dkr.ecr.us-east-2.amazonaws.com/whyphi_server:latest