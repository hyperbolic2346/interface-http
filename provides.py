from charmhelpers.core import hookenv
from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class HttpProvides(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def joined(self):
        set_flag(self.expand_name('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.available'))

    def configure(self, port, private_address=None, hostname=None):
        if not hostname:
            hostname = hookenv.unit_get('private-address')
        if not private_address:
            private_address = hookenv.unit_get('private-address')
        for relation in self.relations:
            relation.to_publish.update({
                'hostname': hostname,
                'private-address': private_address,
                'port': port,
            })
