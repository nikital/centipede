CRYPT_HOSTNAME = 'nikita-crypt.local'

def ssh(command=None, host=CRYPT_HOSTNAME):
    if command:
        return ['ssh', host, command]
    else:
        return ['ssh', host]
