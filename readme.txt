This is a super-dirty setup to do Linux-compatible disk encryption on OSX,
called Centipede. It's meant to do what TrueCrypt did in it's good days.

The container resides on the host and exported via NFS to the Linux VM. The
Linux VM opens the container with dm-crypt and exports the results back to the
host via NFS.
