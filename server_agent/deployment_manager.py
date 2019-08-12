import toml
from server_agent import LOG
import uuid
import subprocess

GITHUB_URL = 'http://github.com'
CLONE_PATH ='~/'


class DeploymentManager():
    """
    Handle application deployments.
    The general process will be as follows-
    clone repo
    load specification
    deploy app
    """

    def __init__(self, repo_owner, repo_name):
        self.repo = repo_name
        self.owner = repo_owner
        self.name = None
        self.app_spec = {}
    
    def load(self):
        """ Load application specification"""
        # pull the toml data
    
    def clone(self):
        """ Clone the repo to a new folder. Returns uuid of the application, or false if clone failed """
        name = uuid.uuid4()

        # clone repo
        res = subprocess.run([f'git clone {GITHUB_URL}/{self.owner}/{self.repo}.git {name}'], cwd='~/')
        if res.returncode != 0:
            return False
            
        else:
            self.name = name
            return True
    
    def deploy(name):
        """ deploy the application """
