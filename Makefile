.PHONY: all dev test clean relclean db devdb

all:
	@echo read Makefile for useful targets

dev:
	@echo "==> setting up dev virtualenv"
	@if [ ! -d venv ]; then python3 -m venv venv; fi
	@./venv/bin/pip install -r requirements.txt

run:
	@echo "==> Starting Gonk Bot"
	@./venv/bin/python ./bot/bot.py

install:
	@echo "==> Installing and restarting Gonk Bot"
	@ssh gonkprod "cd git/gonk && git pull && pm2 restart gonk-bot"

db:
	@echo"==> Updating live DB"
	@ssh gonkprod "cd git/gonk && git pull && mysql -uroot < db/schema.sql"

devdb:
	@echo"==> Updating local DB"
	@ssh gonkprod "mysql -uroot < db/schema.sql"

start:
	@echo "==> All stations, black alert"
	@ssh gonkprod "cd git/gonk && pm2 start ./run.sh --name gonk-bot"

kill:
	@echo "==> Kill him now"
	@ssh gonkprod "cd git/gonk && pm2 delete gonk-bot"

clean:
	@echo "==> cleaning working files"
	@find . -name \emacs*.core -delete
	@find . -name \*~ -delete
	@find . -name \*.pyc -delete
	@find . -name \#* -delete

relclean: clean
	@echo "==> removing dev venv"
	@rm -rf venv gonk-bot.egg-info
