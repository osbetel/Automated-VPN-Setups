# script to build docker image of openvpn server on PORT 443 using TCP. 
# installs requisite packages, creates docker image, volume, and initiates "run-forever" of the container.
# outputs a .ovpn certificate file you can use to connect to the VPN server.
import os, requests

# Make sure requests library is installed via pip3
os.system("apt install python3-pip")
os.system("pip3 install requests")

# Save IP for later
ip = requests.get("http://ifconfig.me").content.decode("utf-8")

# initialize docker volume for the openvpn certificate authority (stores authorized and banned keys here)
os.system("docker volume create --name ovpn443")

# Build docker container for openvpn. initialize certificate authority certs
os.system("docker build docker-openvpn-443 -t docker-openvpn-443")
os.system("docker run -v ovpn443:/etc/openvpn --log-driver=none --rm "
          "docker-openvpn-443 ovpn_genconfig -u tcp://" + ip + ":443")
os.system("docker run -v ovpn443:/etc/openvpn --log-driver=none --rm -it docker-openvpn-443 ovpn_initpki")

# boot up the openvpn server process
os.system("docker run -v ovpn443:/etc/openvpn -d -p 443:1194/tcp --cap-add=NET_ADMIN "
          "--restart=always --name docker-openvpn-443 docker-openvpn-443")

# generate a client certificate for your computer, and output to directory
os.system("docker run -v ovpn443:/etc/openvpn "
          "--log-driver=none --rm -it docker-openvpn-443 easyrsa build-client-full vpn nopass")
os.system("docker run -v ovpn443:/etc/openvpn --log-driver=none "
          "--rm docker-openvpn-443 ovpn_getclient vpn > vpn443.ovpn")
