from bottle import Bottle, run, get, post, static_file, request
from server_agent.app_manager import AppManager
from pathlib import Path

# globals
PORT = 8080
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
    print(request.json)
    return

@app.get('/rt/<name>')
def sec(name):
    return f'hello {name}'

run(app, host='localhost', port=PORT)