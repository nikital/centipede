Before running the setup scripts on the hosts, prepare the following things:

- Install Ubuntu server in VirtualBox, name it "crypt". Make the username
  identical to the username on the Mac. Make sure to enable OpenSSH during
  setup. The recommended hostname is "nikita-crypt".
- In VirtualBox, prepare a Host-only adapter in subnet 1.1.1.1/24. The host
  should get 1.1.1.1.
