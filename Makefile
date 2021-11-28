install: requirements.txt
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

run:
	export FLASK_APP=app
	flask run
