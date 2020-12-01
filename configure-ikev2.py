import os, requests, socket, random

# Make sure requests library is installed via pip3
os.system("apt install python3-pip")
os.system("pip3 install requests")

# Save public server IP for later
ip = requests.get("http://ifconfig.me").content.decode("utf-8")
name = socket.gethostname() + " – " + ip
exclude = "%032x" % random.getrandbits(128)

# find the name in the generate-mobileconfig file and edit it before the dockerfile is built.
# : ${PROFILE_NAME="IKEv2 VPN Profile"}
genConfig = open("docker-ikev2/bin/generate-mobileconfig", "r")
lines = []
for line in genConfig:
    lines.append(line)
for i in range(len(lines)):
    if lines[i].__contains__(": ${VPN_NAME"):
        lines[i] = ": ${VPN_NAME=\"" + name + "\"}\n"
genConfig.close()

genConfig = open("docker-ikev2/bin/generate-mobileconfig", "w")
genConfig.writelines(lines)
genConfig.close()

# Build and run docker container for ikev2
os.system("docker build docker-ikev2 -t docker-ikev2")
os.system(f"""docker run --cap-add=NET_ADMIN -d --name docker-ikev2 --restart=always -p 500:500/udp -p 4500:4500/udp -e "HOST={ip}" -e "HOSTNAME={name}" -e "EXCLUDE_SSID={exclude}" docker-ikev2""")
# unfortunately ikev2 protocol runs on ports 500 and 4500. Port 500 for data, port 4500
# as the IPSec control path (ikev2 wraps key exchange inside an IPSec tunnel)

# Generating the mobileconfig file and output to directory
os.system("docker exec -it docker-ikev2 generate-mobileconfig > ikev2.mobileconfig")
