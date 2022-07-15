install:
	pip3 install -r requirements.txt 

start:
	uvicorn main:app --reload