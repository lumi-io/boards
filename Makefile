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
	docker build -t whyphi_server .
	docker tag whyphi_server:latest 280776660572.dkr.ecr.us-east-2.amazonaws.com/whyphi_server:latest
	docker push 280776660572.dkr.ecr.us-east-2.amazonaws.com/whyphi_server:latest


test:
	docker build -t test .
	docker run -d --name=test -p 1234:1234 ehjggknsjk
