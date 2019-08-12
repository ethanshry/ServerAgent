import toml
from server_agent import LOG

class AppManager():
    """ Manager for the agent's collection of applications """

    def __init__(self, config_path):
        self.filepath = config_path
        try:
            self._data = toml.load(config_path)
        except FileNotFoundError:
            LOG.error(f'could not find file with path {config_path}')
            raise SystemExit
    
    def deregister_app(self, name):
        """
        Remove app to node_env.toml.
        This is to see if the port we want to reserve is safe to use or not.
        Returns True or False based on whether we were able to deregister or not.
        """
        if name == 'SELF':
            LOG.info(f'server_agent cannot deregister itself')
            return False
        try:
            app = self._data.pop(name)
            LOG.info(f"deregistering app with name: {name} at location {app['dest']}")
            with open(self.filepath, 'w') as f:
                toml.dump(self._data, f)
                LOG.info(f'successfully deregistered app')
            return True

        except KeyError:
            LOG.warning(f'attempted to pop app {name} but no app registered')
            return False

    def register_app(self, name, deploy_type, dest, commit):
        """
        Add app to node_env.toml.
        This is to see if the port we want to reserve is safe to use or not.
        Returns True or False based on whether we were able to register or not.
        """

        LOG.info(f'registering app with name: {name} of type {deploy_type} at dest {dest}')
        if name in self._data:
            if self._data[name]['commit'] == commit:
                LOG.info(f'application is already on this commit: {commit}')
                return False
            self._data[name] = {
                'type': deploy_type,
                'dest': dest,
                'commit': commit
            }
            return True
        elif dest in map(lambda x: self._data[x]['dest'], self._data):
            LOG.info(f'cannot register application: Another app exists at target destination')
            return False
        else:
            self._data[name] = {
                'type': deploy_type,
                'dest': dest,
                'commit': commit
            }
        with open(self.filepath, 'w') as f:
            toml.dump(self._data, f)
            LOG.info(f'successfully registered app')
        
        return True
        