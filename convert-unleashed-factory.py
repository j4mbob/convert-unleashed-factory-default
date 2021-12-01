#!/usr/bin/env python2
import pexpect
import sys
import argparse
import logging
import multiprocessing
import time

def parseArguments():

    parser = argparse.ArgumentParser(description='Ruckus AP Unleashed - Factory default Firmware Rollback')
    parser.add_argument('filepath', help='filepath')
    parser.add_argument('username',help='admin username on AP')
    parser.add_argument('password',help='admin password on AP')
    parser.add_argument('model',help='AP model')
    parser.add_argument('hostname', help='hostname of webserver')

    return parser.parse_args()
            

def spanwProcess(ruckus):

    logging.info("Process %s: starting", ruckus.ip)

    try:

        rukus.child = pexpect.spawn('ssh -o StrictHostKeyChecking=no ' + ruckus.ip)
        rukus.child.logfile = sys.stdout
        rukus.child.timeout = 45
        rukus.child.expect ('Please login:')
        rukus.child.sendline (ruckus.username)
        rukus.child.expect ('password : ')
        rukus.child.sendline (ruckus.password + "\r")
        rukus.child.expect ('rkscli: ')
        rukus.child.sendline ('fw set proto http\r')
        rukus.child.expect ('OK')
        rukus.child.sendline ('fw set control ruckus/' +  ruckus.firmware + "\r")
        rukus.child.expect ('OK')
        rukus.child.sendline ('fw set host ' + ruckus.hostname + '\r')
        rukus.child.expect ('OK')
        rukus.child.sendline ('fw update\r')
        rukus.child.expect(": Completed", timeout=300)
        rukus.child.sendline('set factory\r')
        rukus.child.expect ('OK')
        rukus.child.sendline('reboot\r')
        rukus.child.expect ('OK')

    except:

        logging.error("Process %s: an error occurred", ruckus.ip)

    logging.info("Process %s: finishing", ruckus.ip)

class Ruckus:

    modelFirmwares = {
        '7372' : 'ZF7372_104.0.0.0.1347.bl7',
        'r300' : 'R300_104.0.0.0.1347.bl7',
        'r500' : 'R500_104.0.0.0.1347.bl7',
        'r600' : 'R600_104.0.0.0.1347.bl7',
        'h500' : 'H500_104.0.0.0.1347.bl7',
        'h510' : 'h510-114.0.0.0.6565.bl7',
        'r510' : 'R510_104.0.0.0.1347.bl7',
    }

    def __init__(self, ip, username, password, model, hostname):

        self.model = model
        self.firmware = self.modelFirmwares.get(self.model)
        self.ip = ip
        self.username = username
        self.password = password
        self.hostname = hostname

if __name__ == '__main__':

    format = "%(asctime)s: %(message)s"

    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    args = parseArguments()

    logging.info("Main: parsing jobs")

    jobs = []

    with open(args.filepath) as file:
        for ip in file:
            ruckus = Ruckus(ip, args.username, args.password, args.model, args.hostname)
            process = multiprocessing.Process(target=spanwProcess, args=(ruckus,))
            jobs.append(process)

    logging.info("Main: starting %d jobs", len(jobs))

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    logging.info("Main: finishing %d jobs", len(jobs))
