build:
	docker build -t webscraperdocker .

run:
	docker run -it --rm -v "$(shell pwd)/output:/app/output" webscraperdocker


