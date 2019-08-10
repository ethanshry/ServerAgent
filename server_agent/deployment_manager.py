import toml
from server_agent import LOG

class DeploymentManager():
    """ Handle application deployments """

    def __init__(self, repo_owner, repo_name):
        self.repo = repo_name
        self.owner = repo_owner
        self.app_spec = {}
    
    def load(self):
        """ Attempt to load application specification from Github """
        