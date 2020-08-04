import os, requests

# Make sure requests library is installed via pip3
os.system("apt install python3-pip")
os.system("pip3 install requests")

# Save IP for later
ip = requests.get("http://ifconfig.me").content.decode("utf-8")

# initialize docker volume for the openvpn certificate authority (stores authorized and banned keys here)
os.system("docker volume create --name ovpn")

# Build docker container for openvpn. initialize certificate authority certs
os.system("docker build docker-openvpn -t docker-openvpn")
os.system("docker run -v ovpn:/etc/openvpn --log-driver=none --rm docker-openvpn ovpn_genconfig -u udp://" + ip)
os.system("docker run -v ovpn:/etc/openvpn --log-driver=none --rm -it docker-openvpn ovpn_initpki")

# boot up the openvpn server process
os.system("docker run -v ovpn:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN "
          "--restart=always --name docker-openvpn docker-openvpn")

# generate a client certificate for your computer, and output to directory
os.system("docker run -v ovpn:/etc/openvpn "
          "--log-driver=none --rm -it docker-openvpn easyrsa build-client-full vpn nopass")
os.system("docker run -v ovpn:/etc/openvpn --log-driver=none "
          "--rm docker-openvpn ovpn_getclient vpn > vpn.ovpn")
