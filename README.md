# ServerAgent

Multi-process deployment manager

## Setting up on a server

```bash
# we will assume ubuntu 18.04 as our operating env
# update OS
sudo apt-get update && apt-get upgrade
# install pip3
sudo apt install python3-pip

# setup package
make setup-linux
make install
pm2 start server_agent


```

## node_env.toml

The node_env.toml file is a confiiguration file designed to contain information about all the applications currently running on the agent.

Format is as follows:

```toml
[APP_NAME]
deployment_type = "S3|PORT"
dest = "wuracing.com"
commit = "e87gr6"

[APP_NAME]
deployment_type = "S3|PORT"
dest = 9020
commit = "9fhr8w"
```

We will be adding to this format as the project develops

## Application specification

ServerAgent expects all deployed applications to have an `agent_config.toml` in their project root directory
Its format is as follows:

```toml
[info]
name = "app_name"
version = "x.x.x"
description = ""

[deployment]
type = "S3|PORT"
dest = "BUCKET_NAME"|PORT_NO

# specify array of commands which should be executed prior to deployment
# this could include package installs, webpack bundling, tests, etc.
# should any of these scripts return non-zero, the deployment will fail
scripts = []

# if deployment is to S3, specify the path from the project's root to the folder which should be copied to S3
artifact_folder = ""
```