from bottle import Bottle, run, get, post, static_file, request
from server_agent.app_manager import AppManager
from server_agent.deployment_manager import DeploymentManager
from server_agent import LOG
from pathlib import Path
import requests as req
import base64
import subprocess

# globals
PORT = 9000
CONFIG_PATH = f'{Path(__file__).parent}/../data/node_env.toml'

FILE_API_BASE = 'https://api.github.com/repos/'

manager = AppManager(CONFIG_PATH)

app = Bottle()

@app.get('/env')
def main():
    return static_file(CONFIG_PATH, root='/')

@app.get('/log')
def log():
    return '/log is under construction'

@app.post('/github-event')
def github_event():
    data = request.json
    if data['action'] == 'closed':
        # this is a pull request which was either closed or merged
        if data['pull_request']['merged'] is True:
            # pull request was merged, we're in luck
            if data['pull_request']['base']['ref'] == 'deployment':
                # we pulled to the deployment branch, we want to run this code
                LOG.info(f"event is good, trying to deploy {data['repository']['full_name']}")

                # check for agent_config.toml in root
                url = f"{FILE_API_BASE}{data['repository']['full_name']}/contents/agent_config.toml"
                res = req.get(url).json()
                if 'message' in res.keys():
                    # file not found
                    LOG.error('repo does not have a valid agent_config.toml')
                else:
                    # app is deployable
                    deployment = DeploymentManager(*(data['repository']['full_name'].split('/')))

                    if not deployment.clone():
                        LOG.error('unable to clone project')
                        return
                    if not deployment.load():
                        LOG.error('error loading config data')
                        return

                    if not manager.register_app(deployment.repo, deployment.type, deployment.destination, deployment.commit):
                        LOG.error('failed to register app')
                        return

                    deployment.deploy()

                    LOG.info('application succesfully deployed')
                    return


@app.get('/status')
def status():
    result = subprocess.run(['pm2 status'], capture_output=True, cwd='.')
    print(result) # TODO rm
    return result.stdout

run(app, host='0.0.0.0', port=PORT)