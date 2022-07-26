
#Tool for processing the output in Wireshark > Statistics > IPv4 Statistics > All Addresses

import sys
import re

def extract_all_ip_addresses(input_file):
    f = open(input_file, "r")
    pattern =re.compile('''((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)''')

    extracted_patterns = [pattern.search(x.strip()) for x in f.readlines()]

    ip_addresses = []

    for search_result in extracted_patterns:
        if search_result:
            ip_addresses.append(search_result.group(0))

    return ip_addresses

def select_private_ip_addresses(list_ip_addresses):
    pattern = re.compile('''(^127\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)''')
    private_ip_addresses = []
    for ip in list_ip_addresses:
        result = pattern.search(ip)
        if result:
            private_ip_addresses.append(ip)

    return private_ip_addresses

def print_list(list_objects):
    for element in list_objects:
        print(element)

if __name__=="__main__":
    if len(sys.argv) <= 1 or (len(sys.argv)>2 and sys.argv[2]!="--private"):
        print("Extracting private IP addresses from Wireshark - by dedalus")
        print("-----------------------------------------------------------")
        print("Please provide a file exported from Wireshark: Statistics > IPv4 Statistics > All Addresses")
        print("Usage: python3 wireshark_private_ip.py <exported text file>")
        print("Only private IP addresses:")
        print("python3 wireshark_private_ip.py <exported text file> --private")
    else:

        ip_addresses = extract_all_ip_addresses(sys.argv[1])
        if (len(sys.argv)>2 and sys.argv[2]=="--private"):
            ip_addresses = select_private_ip_addresses(ip_addresses)
        print_list(ip_addresses)