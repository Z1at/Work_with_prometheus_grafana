env:
	cp .env.example .env

up:
	docker-compose up -d

req:
	pip install -r requirements.txt