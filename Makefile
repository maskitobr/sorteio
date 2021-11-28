install: requirements.txt
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

run:
	export FLASK_APP=app
	flask run
