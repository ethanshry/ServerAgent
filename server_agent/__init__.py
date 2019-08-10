import logging

LOG = logging.getLogger('server_agent')
LOG.addHandler(logging.StreamHandler())
LOG.propigate = False
# TODO: figure out why this isn't logging with the LEVEL:file:message format
LOG.setLevel(logging.DEBUG)