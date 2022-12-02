
#Tool for extracting the /24 subnetworks where an input list of IP addresses are located

import sys
import re

def extract_subnetworks(list_ip_addresses):
    subnetworks = []
    for ip in list_ip_addresses:
        by_tuples = ip.split('.')
        if len(by_tuples)!=4:
            print("MALFORMED IP!! - "+ip)
            return subnetworks
        by_tuples[3] = '0/24'
        subnet = '.'.join(by_tuples)
        if subnet not in subnetworks:
            subnetworks.append(subnet)

    return subnetworks

def read_ip_addresses(input_file):
    f = open(input_file, "r")
    ip_addresses = f.read().splitlines()

    return ip_addresses

def print_list(list_objects):
    for element in list_objects:
        print(element)

if __name__=="__main__":
    if len(sys.argv) <= 1:
        print("Extracting private IP addresses from Wireshark - by dedalus")
        print("-----------------------------------------------------------")
        print("Please provide a file exported from Wireshark: Statistics > IPv4 Statistics > All Addresses")
        print("Usage: python3 extract_subnetworks.py <ip address list file>")
    else:

        ip_addresses = read_ip_addresses(sys.argv[1])
        subnetworks = extract_subnetworks(ip_addresses)
        print_list(subnetworks)