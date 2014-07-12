from tempfile import NamedTemporaryFile
import os

class ExportsAppend(object):
    def __init__(self, u, directory):
        super(ExportsAppend, self).__init__()

        self.u = u
        self.directory = directory

    def run(self):
        with NamedTemporaryFile(mode='w') as patched:
            with open('/etc/exports', 'r') as original:
                for line in original:
                    if line.startswith(self.directory):
                        return
                    patched.write(line)
            patched.write(
                    '{} -mapall={}:{} -network 1.1.1.0 -mask 255.255.255.0\n'
                    .format(self.directory, os.getuid(), os.getgid()))
            patched.flush()
            self.u.run(['sudo', 'cp', patched.name, '/etc/exports'])

    def unroll(self):
        with NamedTemporaryFile(mode='w') as unpatched:
            with open('/etc/exports', 'r') as patched:
                for line in patched:
                    if not line.startswith(self.directory):
                        unpatched.write(line)
            unpatched.flush()
            self.u.run(['sudo', 'cp', unpatched.name, '/etc/exports'])
