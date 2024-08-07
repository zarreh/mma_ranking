# Makefile for managing Python project tasks

# Define the default make target
.PHONY: all
all: activate_env lint run_scrapy

# Lint Python scripts and Jupyter notebooks
.PHONY: lint
lint:
	# Lint Python files
	autoflake8 . --exclude=mme_app/ufcstat_scrapy
	black .
	isort .

# Run the Scrapy crawler
.PHONY: run_scrapy
DATE = $(shell date "+%Y-%m-%d")
run_scrapy:
	cd mma_ranking/ufcstat_scrapy && scrapy crawl events -o ../../data/all_fights_$(DATE).csv

# Clean up generated files
.PHONY: clean
clean:
	# Command to clean up linting artifacts or any other clean up you want to do

.PHONY: activate_env
activate_env:
	source ../venv/mma_ufc/Scripts/activate

.PHONY: git_push
MSG ?= "updates"
git: 
	git add .
	git commit -m "$(MSG)"
	git push

