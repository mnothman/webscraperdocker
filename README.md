after changes: <br />

make build <br />

handle url in cmd line now: 

docker run -it --rm -v "$(pwd)/output:/app/output" webscraperdocker https://example.com  <br />

--> will log data in scraper.log and sqlite data.db  <br /> <br />


debugging:  <br /> 

restart docker container  <br />

sudo systemctl restart docker <br />

ensure user is part of docker group  <br /> 

sudo usermod -aG docker $(whoami) <br />

then restart (might need restart entire system/computer) <br />

sudo systemctl restart docker <br />

verify if user is added to group:  <br /> 

groups $(whoami)<br />

then build again: make build <br />

