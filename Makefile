.PHONY: setup-linux
setup-linux:
	curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
	@echo installing nodejs
	sudo apt-get install -y nodejs
	@echo installing pm2
	sudo npm install -y pm2 -g
	@echo setup done

.PHONY: setup
setup:
	@echo Make is not configured to setup for Windows or macOS
	@echo Please install nodejs (https://nodejs.org/en/download/)
	@echo Then install pm2 globally with "sudo npm install pm2 -g"

.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: test
test:
	@echo Make is not configured to run any tests

.PHONY: run
run:
	python3 -m server_agent