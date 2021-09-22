SERVICE=built-budgets
DOCKER_EXEC=docker exec -it $(SERVICE)
DOCKER_PIPENV=$(DOCKER_EXEC) pipenv run
ALEMBIC=alembic

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

migrations-autogenerate:  ## autogenerate alembic migration
ifndef message
	$(error "Message required. Try message='some message'")
endif
	$(DOCKER_PIPENV) $(ALEMBIC) revision -m "$(message)" --autogenerate

migrations-migrate:  ## Apply migrations
	$(DOCKER_PIPENV) $(ALEMBIC) upgrade head
