.PHONY: init run/dev run/prod build/dev build/prod stack/list stack/create stack/update stack/delete
.DEFAULT_GOAL := help

NAMESPACE := ada-team-2
NAME := fintet

help: ## Show this help
	@echo "${NAMESPACE}/${NAME}"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | \
	fgrep -v fgrep | sed -e 's/## */##/' | column -t -s##

##

init: ## Initialize the environment
	for f in functions/*/*.txt; do \
		pip install -r "$$f"; \
	done
	for f in services/*/*.txt; do \
		pip install -r "$$f"; \
	done

##

run/dev: ## Run development app
	docker-compose -p $(subst -,_,$(NAME))_dev -f docker-compose.dev.yml up

run/prod: ## Run production app
	docker-compose -p $(subst -,_,$(NAME))_prod -f docker-compose.prod.yml up

##

run/func: ## Run function
	functions-framework --target $(target) --source functions/$(file)/main.py --host 127.0.0.1 --port 9090 --debug

##

build/dev: ## Build development app
	docker-compose -p $(subst -,_,$(NAME))_dev -f docker-compose.dev.yml build

build/prod: ## Build production app
	docker-compose -p $(subst -,_,$(NAME))_prod -f docker-compose.prod.yml build

##

stack/list: ## List stacks
	gcloud deployment-manager deployments list

stack/create: ## Create stack
	gcloud deployment-manager deployments create $(name) --config $(file)

stack/update: ## Update stack
	gcloud deployment-manager deployments update $(name) --config $(file)

stack/delete: ## Delete stack
	gcloud deployment-manager deployments delete $(name)
