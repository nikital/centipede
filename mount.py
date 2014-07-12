#! /usr/bin/env python

from unroll import Unroll
from exports_append import ExportsAppend
from ssh import ssh, CRYPT_HOSTNAME

from getpass import getpass
import os
import sys

NC_PORT = 54736

g_volume_password = ''

def get_volume_password():
    global g_volume_password
    g_volume_password = getpass(prompt='Container Password: ')
    if not g_volume_password:
        raise ValueError('Password is empty')

def mount(directory):
    u = Unroll()

    exports_append = ExportsAppend(u, directory)
    u.run(exports_append.run, exports_append.unroll)
    u.run('sudo nfsd restart')

    u.run(
            'VBoxManage snapshot crypt restore crypt',
            'VBoxManage snapshot crypt restore crypt'
            )

    u.run(
            'VBoxManage startvm crypt',
            'VBoxManage controlvm crypt poweroff'
            )

    u.run(['nc', '-l', str(NC_PORT)])

    u.run(
            ssh('sudo mount "1.1.1.1:{:s}" /media/volume'.format(directory)),
            ssh('sudo umount /media/volume')
            )

    u.run(get_volume_password)
    u.run(
        ssh(
            "HISTFILE= echo '{:s}' | sudo cryptsetup luksOpen /media/volume/crypt crypt"
            .format(g_volume_password)),
        ssh('sudo cryptsetup luksClose crypt'))

    u.run(
            ssh('sudo mount /dev/mapper/crypt /crypt'),
            ssh('sudo umount /crypt')
            )

    u.run(
            'mkdir -p /Volumes/crypt',
            'rmdir /Volumes/crypt'
            )

    u.run(
            'sudo mount_nfs {:s}:/crypt /Volumes/crypt'.format(CRYPT_HOSTNAME),
            'umount /Volumes/crypt'
            )

    u.run('open /Volumes/crypt', critical=False)

def main():
    if len(sys.argv) != 2:
        print 'Usage: {0} crypt-directory'.format(sys.argv[0])
        return 1
    directory = os.path.abspath(sys.argv[1])

    try:
        mount(directory)
    except Exception, err:
        print err
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
