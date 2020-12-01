import os, requests, time


os.system("wget https://raw.githubusercontent.com/Nyr/openvpn-install/master/openvpn-install.sh -O openvpn-ubuntu-install.sh")
os.system("chmod -v +x openvpn-ubuntu-install.sh"
os.system("bash openvpn-ubuntu-install.sh")

# need to pass in arguments 
