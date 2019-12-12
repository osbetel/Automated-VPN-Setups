### Automated VPN setup w/ Docker ###
This project contains scripts and dockerfiles to create VPN server docker images.
To run, only the following files / folders are needed:
docker-ikev2
docker-openvpn
docker-openvpn-443
configure-ikev2.py
configure-openvpn.py
configure-openvpn-443.py
---
Requirements:
Must have docker and python3 installed, as well as the ```requests``` pacakge for python3.
The scripts will check and install via pip if the package is not already instaled.
---
Running:
1) Place the required folders / files above into a linux-based server (must install docker! ```apt install docker```). I usually use an Amazon EC2 or a DigitalOcean droplet.
2) run all the python scripts and follow their prompts to input passphrases for certificate generation, etc.
3) you can use ```docker containers ls``` to list the running containers after executing the configuration scripts.
4) the scripts will output .ovpn files and / or .mobileconfig files. Fetch using sftp and install to your device of choice.
5) If you used an Amazon EC2 or a Digital Ocean Droplet, you should be able to connect using the .ovpn/.mobileconfig files, otherwise if using a self-hosted device you must open ports 1194 and 443 (openvpn), 500 and 4500 (ikev2).  
