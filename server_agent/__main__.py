from bottle import Bottle, run, get, post, static_file, request
from server_agent.app_manager import AppManager
from pathlib import Path

# globals
PORT = 9000
CONFIG_PATH = f'{Path(__file__).parent}/../data/node_env.toml'

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
    print(data['action'])
    if data['action'] == 'closed':
        # this is a pull request which was either closed or merged
        print(data['pull_request']['merged'])
        if data['pull_request']['merged'] is True:
            # pull request was merged, we're in luck
            print(data['ref'])
            print(data['repo'])
            #print(data['base'])
            if ['ref'] == 'refs/heads/deployment':
                # we pulled to the deployment branch, we want to run this code
                print(f"event is good, trying to deploy {data['repo']['full_name']}")

@app.get('/rt/<name>')
def sec(name):
    return f'hello {name}'

run(app, host='0.0.0.0', port=PORT)