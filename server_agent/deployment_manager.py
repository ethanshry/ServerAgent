import toml
from server_agent import LOG
import subprocess
import os

GITHUB_URL = 'https://github.com'
ROOT ='/home/ubuntu'


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
        self.app_spec = None
        self.type = None
        self.destination = None
        self.commit = None
    
    def load(self):
        """ Load application specification"""
        # pull the toml data
        try:
            self.app_spec = toml.load(f'{ROOT}/{self.owner}/{self.repo}/agent_config.toml')
        except FileNotFoundError:
            LOG.error(f'could not find agent_config in repo')
            return False
        
        self.type = self.app_spec['deployment']['type']

        self.destination = self.app_spec['deployment']['dest']

        self.commit = subprocess.run(['git rev-parse HEAD'], stdout=subprocess.PIPE, shell=True, cwd=f'{ROOT}/{self.owner}/{self.repo}').stdout

        print(f'{self.type} - {self.destination} - {self.commit}')

        subprocess.run(f"pm2 stop {self.app_spec['info']['name']}", shell=True, cwd=f"{ROOT}/{self.owner}/{self.repo}")

        return True
    
    def clone(self):
        """ Clone the repo to a new folder. Returns uuid of the application, or false if clone failed """
        if not os.path.exists(f'{ROOT}/{self.owner}'):
            os.makedirs(f'{ROOT}/{self.owner}')
        # clone repo
        res = subprocess.run([f'rm -rf {ROOT}/{self.owner}/{self.repo} && git clone {GITHUB_URL}/{self.owner}/{self.repo}.git'], shell=True, cwd=f'{ROOT}/{self.owner}')

        return res.returncode is 0
    
    def deploy(self):
        """ deploy the application """
        print(self.type.upper())
        if self.type.upper() == 'S3':
            return self._deploy_s3()
        elif self.type.upper() == 'PORT':
            return self._deploy_port()
        else:
            LOG.error('deployment type not supported')
            return False
    
    def _deploy_s3(self):
        """ deploy application files to an s3 bucket """
        return

    def _deploy_port(self):
        """ deploy to a port via pm2 """
        # run user-configured scripts prior to deployment
        res = subprocess.run(self.app_spec['deployment']['scripts'], shell=True, cwd=f'{ROOT}/{self.owner}/{self.repo}')

        if res.returncode is not 0:
            LOG.error('user deployment scripts failed')
            return False
    
        res = subprocess.run(f"pm2 start {self.app_spec['info']['name']} --interpreter=python3 --no-autorestart --interpreter-args='-m {self.app_spec['info']['name']}'", shell=True, cwd=f"{ROOT}/{self.owner}/{self.repo}")

        return res.returncode is 0