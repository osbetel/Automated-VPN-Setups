import os, requests, time

# Make sure requests library is installed via pip3
os.system("apt install python3-pip")
os.system("pip3 install requests")
os.system("OVPN_DATA=\"ovpn-data-1\"")


# Save IP for later
ip = requests.get("http://ifconfig.me").content.decode("utf-8")

# initialize docker volume for the openvpn certificate authority (stores authorized and banned keys here)
os.system("docker volume create --name ovpn-data-1")
# os.system("docker build docker-openvpn -t docker-openvpn")

# Build docker container for openvpn. initialize certificate authority certs
os.system("docker run -v ovpn-data-1:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_genconfig -u udp://" + ip)
os.system("docker run -v ovpn-data-1:/etc/openvpn --log-driver=none --rm -it kylemanna/openvpn ovpn_initpki")
# time.sleep(5)
# boot up the openvpn server process
os.system("docker run -v ovpn-data-1:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN --restart=always --name docker-openvpn kylemanna/openvpn")

# generate a client certificate for your computer, and output to directory
os.system("docker run -v ovpn-data-1:/etc/openvpn --log-driver=none --rm -it kylemanna/openvpn easyrsa build-client-full vpn nopass")

os.system("docker run -v ovpn-data-1:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_getclient vpn > vpn.ovpn")
