DC = docker-compose
STORAGES_FILE = docker_compose/mongodb.yaml
MONGODB_EXPRESS_FILE = docker_compose/mongodb_express.yaml
APP_FILE = docker_compose/app.yaml
EXEC = docker exec -it
LOGS = docker logs
ENV_FILE = --env-file .env
APP_CONTAINER = app
INTO_BASH = /bin/bash


.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MONGODB_EXPRESS_FILE}  ${ENV_FILE} up -d

.PHONY: mongo
mongo:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${MONGODB_EXPRESS_FILE} down

.PHONY: appbash
appbash:
	${EXEC} ${APP_CONTAINER} ${INTO_BASH}

.PHONY: runtest
runtest:
	${EXEC} ${APP_CONTAINER} pytest
