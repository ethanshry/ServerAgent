.PHONY: setup-linux
setup-linux:
	curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
	installing nodejs
	sudo apt-get install -y nodejs
	installing pm2
	sudo npm install -y pm2 -g
	setup done

.PHONY: setup
setup:
	Make is not configured to setup for Windows or macOS
	Please install nodejs (https://nodejs.org/en/download/)
	Then install pm2 globally with "sudo npm install pm2 -g"

.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: test
test:
	Make is not configured to run any tests

.PHONY: run
run:
	python3 -m server_agent