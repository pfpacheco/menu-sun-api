-include .env
export


start/env:
	docker run \
	--name menu-sun-api-db \
	-e MYSQL_ROOT_PASSWORD=${DB_PASSWORD} \
	-e MYSQL_DATABASE=${DB_NAME} \
	-e MYSQL_USER=${DB_USER} \
	-p 3306:3306 \
	-d mysql:5.6

clean/decrypt-ssl-key:
	rm -f config/bastion_rsa

decrypt-ssl-key: clean/decrypt-ssl-key
	openssl aes-256-cbc -K ${encrypted_e356face9b97_key} -iv ${encrypted_e356face9b97_iv} -in config/bastion_rsa.enc -out config/bastion_rsa -d
	chmod 400 config/bastion_rsa

deploy/tunnel: decrypt-ssl-key
	ssh -4 -L $(TUNNEL_PORT):${DB_HOST}:${DB_PORT} ${BASTION_USER}@${BASTION_IP} -fN -o StrictHostKeyChecking=no -i config/bastion_rsa

deploy/build:
	$(PYTHON_BIN)/pip3 install -r requirements.txt --upgrade --force-reinstall -t menu_sun_api/vendored

deploy: deploy/build
	serverless deploy --stage ${STAGE}

db/migrate:
	${PYTHON_BIN}/alembic \
		-x DB_USER=${DB_USER} \
		-x DB_PASSWORD=${DB_PASSWORD} \
		-x DB_HOST=${DB_HOST} \
		-x DB_PORT=${DB_PORT} \
		-x DB_NAME=${DB_NAME} \
		upgrade heads


db/migration:
	${PYTHON_BIN}/alembic \
		-x DB_USER=${DB_USER} \
		-x DB_PASSWORD=${DB_PASSWORD} \
		-x DB_HOST=${DB_HOST} \
		-x DB_PORT=${DB_PORT} \
		-x DB_NAME=${DB_NAME} \
		revision --autogenerate -m ${name}

local/clean:
	docker-compose stop && docker-compose rm -vf

local/up: local/clean
	docker-compose up -d
	sleep 20

local/install-packages:
	${PYTHON_BIN}/pip3 install flask
	${PYTHON_BIN}/pip3 install flask-graphQL

local/setup: local/up local/install-packages db/migrate


# Install dependent libraries
#
#   make build/dependencies/install
#
build/dependencies/install:
	$(PYTHON_BIN)/pip3 install -r build_requirements.txt
	$(PYTHON_BIN)/pip3 install -r requirements.txt
# Run safety check on lib dependencies
#
#   make build/dependencies/lib/safety-check
#
build/dependencies/lib/safety-check:
	$(PYTHON_BIN)/safety check -r requirements.txt
# Run pep8 code style validations
#
#   make build/code-style
#
build/code-style:
	$(PYTHON_BIN)/pycodestyle --statistics --ignore=E501,E402 --count menu_sun_api/ menu_public_api/ promax/ test/ --exclude=vendored
# Build project
#
#   make build
#
build: build/dependencies/install build/dependencies/lib/safety-check build/code-style deploy/build
# Building githooks
#
#   make build/githooks
#
build/githooks:
	githooks
# Upload coverage report
#
#   make test/coverage/upload current_branch==master
#
test/coverage/upload:
ifeq ($(stage),prod)
	$(PYTHON_BIN)/codecov -t $(CODECOV_TOKEN) -b $(CURRENT_BRANCH)
else
	@echo $(CURRENT_BRANCH)
endif
# Run project tests
#
#   make test
#
test: build local/up db/migrate test/run
	make local/clean

# Run tests with its coverage report
#
#   make test/run
#
test/run:
	$(PYTHON_BIN)/py.test test -v -x --cov-fail-under=80


CURRENT_BRANCH = $(shell git rev-parse --abbrev-ref HEAD)
PYTHON_BIN ?= .venv/bin



