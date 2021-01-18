.PHONY: all dev test clean relclean

all:
	@echo read Makefile for useful targets

dev:
	@echo "==> setting up dev virtualenv"
	@if [ ! -d venv ]; then python3 -m venv venv; fi
	@./venv/bin/pip install -e .

run:
	@echo "==> Starting Squirrel Bot"
	@./venv/bin/bot

clean:
	@echo "==> cleaning working files"
	@find . -name \emacs*.core -delete
	@find . -name \*~ -delete
	@find . -name \*.pyc -delete
	@find . -name \#* -delete

relclean: clean
	@echo "==> removing dev venv"
	@rm -rf venv squirrel-sweeper-bot.egg-info