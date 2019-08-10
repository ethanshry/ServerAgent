import toml
from server_agent import LOG

class AppManager():
    """ Manager for the agent's collection of applications """

    def __init__(self, config_path):
        self.filepath = config_path
        try:
            self._data = toml.load(config_path)
        except FileNotFoundError:
            LOG.error(f'count not find file with path {config_path}')
            raise SystemExit
    
    def deregister_app(self, port):
        """
        Remove app to node_env.toml.
        This is to see if the port we want to reserve is safe to use or not.
        Returns True or False based on whether we were able to deregister or not.
        """
        try:
            app = self._data.pop(port)
            LOG.info(f"deregistering app with name: {app['name']} at port {port}")
            with open(self.filepath, 'w') as f:
                toml.dump(self._data, f)
                LOG.info(f'successfully deregistered app')
            return True

        except KeyError:
            LOG.warning(f'attempted to pop app at port {port} but no app registered')
            return False

    def register_app(self, name, port):
        """
        Add app to node_env.toml.
        This is to see if the port we want to reserve is safe to use or not.
        Returns True or False based on whether we were able to register or not.
        """
        port = str(port)

        LOG.info(f'registering app with name: {name} at port {port}')
        if port in self._data:
            LOG.info(f'cannot register application with name {name} at port {port}: Another app already exists')
            return False
        else:
            self._data[port] = {
                'name': name
            }
        with open(self.filepath, 'w') as f:
            toml.dump(self._data, f)
            LOG.info(f'successfully registered app')
        
        return True
        