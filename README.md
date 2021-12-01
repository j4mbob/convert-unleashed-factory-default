# Reflash Unleashed firmware APs back to factory default standalone APs 

Requires the following python2 modules:

pexpect<br/>
sys<br/>
argparse<br/>
logging<br/>
multiprocessing<br/>
time<br/>

install them via **pip2 install <module>**

## usage


*usage: convert-unleashed-factory-default.py [-h]filepath username password model hostname*

*filepath* is the path to a file containing the IP address of each AP to reflash in the following format:

192.168.1.2<br/>
192.168.1.3<br/>
192.168.1.4<br/>

This will look for a webserver avalible at *hostname* and by default will look for a /ruckus/ directory with the firmware files inside it and pull it via HTTP

Script supports the following models / firmware files.

    modelFirmwares = {
        '7372' : 'ZF7372_104.0.0.0.1347.bl7',
        'r300' : 'R300_104.0.0.0.1347.bl7',
        'r500' : 'R500_104.0.0.0.1347.bl7',
        'r600' : 'R600_104.0.0.0.1347.bl7',
        'h500' : 'H500_104.0.0.0.1347.bl7',
        'h510' : 'h510-114.0.0.0.6565.bl7',
        'r510' : 'R510_104.0.0.0.1347.bl7',
    }

username and pass is the AP CLI username and password (not the SZ credentials)

Script is multithreaded so will fire off a socket for each IP simultanously to speed up flashing on large deployments
