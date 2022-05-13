.PHONY: init run/app build/app deploy/app deploy/func stack/list stack/create stack/update stack/delete
.DEFAULT_GOAL := help

NAMESPACE := ada-team-2
NAME := fintet

CLOUD_PROJECT := jads-adaassignment
CLOUD_REGION := europe-west3
CLOUD_ACCOUNT := jads-adaassignment-application@jads-adaassignment.iam.gserviceaccount.com


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

run/app: ## Run app
	docker-compose -p $(subst -,_,$(NAME)) -f docker-compose.yml up

build/app: ## Build app
	docker-compose -p $(subst -,_,$(NAME)) -f docker-compose.yml build

##

deploy/app: ## Deploy app
	@echo "Error: Not Implemented"

deploy/func: ## Deploy function
	gcloud functions deploy ${CLOUD_PROJECT}-$(subst _,-,$(target)) --region ${CLOUD_REGION} --service-account ${CLOUD_ACCOUNT} --entry-point $(target) --source ./functions/$(source) --runtime python39 --trigger-http --allow-unauthenticated

##

stack/list: ## List stacks
	gcloud deployment-manager deployments list

stack/create: ## Create stack
	gcloud deployment-manager deployments create $(name) --config $(file)

stack/update: ## Update stack
	gcloud deployment-manager deployments update $(name) --config $(file)

stack/delete: ## Delete stack
	gcloud deployment-manager deployments delete $(name)
