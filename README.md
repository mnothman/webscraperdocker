after changes: <br />
docker build -t webscraperdocker . <br />

docker run -it --rm webscraperdocker <br />

or makefile <br />
make build <br />
make run <br />




debugging:  <br /> 

restart docker container  <br />

sudo systemctl restart docker <br />

ensure user is part of docker group  <br /> 

sudo usermod -aG docker $(whoami) <br />

then restart (might need restart entire system/computer) <br />

sudo systemctl restart docker <br />

verify if user is added to group:  <br /> 

groups $(whoami)<br />

then build again  <br />

docker build -t webscraperdocker .
