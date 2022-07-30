PROJECT=apprunner-rss
REGION=ap-northeast-1
ACCOUNT=853641575541

URL=https://pqwm9pmm6x.ap-northeast-1.awsapprunner.com

login::
	aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin https://${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com

build::
	docker build -t ${PROJECT} .
	docker tag ${PROJECT}:latest ${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${PROJECT}:latest

run:: build
	docker run -p 4567:4567 --rm -v $$HOME/.aws:$$HOME/.aws --env AWS_REGION=${REGION} --env "HOME=$$HOME" ${PROJECT}:latest

shell::
	docker run -it ${PROJECT}:latest /bin/bash

push::
	docker push ${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${PROJECT}:latest

pull::
	docker pull ${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${PROJECT}:latest

start::
	(cd app; env QUEUE_URL=${QUEUE_URL} bundle exec ruby server.rb)

createstack:
	aws --region ${REGION} cloudformation create-stack --stack-name ${PROJECT} --capabilities CAPABILITY_IAM --template-body "$$(cat pipeline.yml)"

updatestack:
	aws --region ${REGION} cloudformation update-stack --stack-name ${PROJECT} --capabilities CAPABILITY_IAM --template-body "$$(cat pipeline.yml)"

validate:
	aws --region ${REGION} cloudformation validate-template --template-body "$$(cat pipeline.yml)"
