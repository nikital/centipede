#! /usr/bin/env python

from unroll import Unroll
from exports_append import ExportsAppend
from ssh import ssh

import os
import sys

def umount(directory):
    u = Unroll()

    u.run('sudo umount /Volumes/crypt')

    u.run(ssh("""\
sync\
&& sudo service nfs-kernel-server stop\
&& sudo umount /crypt\
&& sudo cryptsetup luksClose crypt\
&& sudo umount /media/volume"""))

    exports_append = ExportsAppend(u, directory)
    u.run(exports_append.unroll)

    u.run('VBoxManage controlvm crypt poweroff')
    u.run('VBoxManage snapshot crypt restore crypt', critical=False)

def main():
    if len(sys.argv) != 2:
        print 'Usage: {0} crypt-directory'.format(sys.argv[0])
        return 1
    directory = os.path.abspath(sys.argv[1])

    try:
        umount(directory)
    except Exception, err:
        print err
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
