#! /usr/bin/env python

from unroll import Unroll
from exports_append import ExportsAppend
from ssh import ssh, CRYPT_HOSTNAME

from getpass import getpass
import os
import sys

NC_PORT = 54736

def create(directory, size_mb, password):
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

    u.run(ssh('dd if=/dev/zero of=/media/volume/crypt bs=1M count={:d}'.format(size_mb)))
    u.run(
        ssh(
            "HISTFILE= echo '{:s}' | sudo cryptsetup luksFormat /media/volume/crypt"
            .format(password)))

    u.run(
        ssh(
            "HISTFILE= echo '{:s}' | sudo cryptsetup luksOpen /media/volume/crypt crypt"
            .format(password)),
        ssh('sudo cryptsetup luksClose crypt'))

    u.run(ssh('sudo mkfs.ext4 /dev/mapper/crypt'))

    u.run(
            ssh('sudo mount /dev/mapper/crypt /crypt'),
            ssh('sudo umount /crypt')
            )

    u.run(ssh('sudo chown -R nikita:nikita /crypt'))

    u.run(ssh())

    u.unroll()

def main():
    if len(sys.argv) != 3:
        print 'Usage: {0} crypt-directory size-in-mb'.format(sys.argv[0])
        return 1
    directory = os.path.abspath(sys.argv[1])
    size_mb = int(sys.argv[2])

    if os.path.exists(directory + '/crypt'):
        print 'Crypt already exists!'
        return 1

    password = getpass(prompt='Container Password: ')
    if password != getpass(prompt='Confirm Password: '):
        print 'Passwords mistmatch'
        return 1

    try:
        create(directory, size_mb, password)
    except Exception, err:
        print err
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
