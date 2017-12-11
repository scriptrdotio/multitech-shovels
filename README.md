# multitech-shovels
Set of simple python based shovels for forwarding data from local multitech broker to a remote one

Note
In order to use these scripts on the multitech gateway, you will need to install the correct dependencies
update /etc/opkg/mlinux-feed.conf to match the current mlinux version (3.1, default was 3.3 and not returns a 404)

and then execute the following

```bash
opkg update
opkg install python-pip
wget https://bootstrap.pypa.io/ez_setup.py
python ez_setup.py

#needed for shovel-aws.py
pip install AWSIoTPythonSDK 
#needed for shovel.py and shovel-aws.py
pip install paho-mqtt

```
