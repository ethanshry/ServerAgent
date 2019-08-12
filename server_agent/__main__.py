from bottle import Bottle, run, get, post, static_file, request
from server_agent.app_manager import AppManager
from pathlib import Path
import requests as req
import base64

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
        print(data['pull_request']['merged'])
        if data['pull_request']['merged'] is True:
            # pull request was merged, we're in luck
            if data['pull_request']['base']['ref'] == 'deployment':
                # we pulled to the deployment branch, we want to run this code
                print(f"event is good, trying to deploy {data['repository']['full_name']}")

                # check for agent_config.toml in root
                url = f"{FILE_API_BASE}/repos/{data['repository']['full_name']}/contents/agent_config.toml"
                res = req.get(url).json()
                if 'message' in res.keys():
                    # file not found
                    print('repo does not have a valid agent_config.toml')
                else:
                    config_file_data = base64.b64decode(res['content'])
                    print(config_file_data)


@app.get('/rt/<name>')
def sec(name):
    return f'hello {name}'

run(app, host='0.0.0.0', port=PORT)