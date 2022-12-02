# Bloom Internal
A pentesting methodology for wandering an internal network and gathering information about targets.

## Introduction

The goal of Bloom Internal is to provide a methodology for the information gathering phase in an internal pentesting, together with a set of scripts to automatize this process.

## 1. Passive Discovery with Wireshark

The starting point should be Passive Discovery of assets. We can use a tool such as *netdiscover*, but if we are in a network with not many assets it's better to just run Wireshark and get the list of all the observed IP addresses:

Statistics > IPv4 Statistics > All Addresses

We can then export these results and use the script *wireshark_private_ip.py* to process the exported file and extract the list of IP addresses:

```
python3 wireshark_private_ip.py <exported text file>
```

To extract only the private ones:

```
python3 wireshark_private_ip.py <exported text file> --private
```

## 2. Ping Sweep with nmap

Next step would be to identify a set of internal subnetworks from the IP addresses passively gathered. We can suppose that for each private IP address, the /24 network where it is located could have other valid IP addresses. The list of /24 subnetworks can be extracted using the extract_subnetworks.py script

```
python3 extract_subnetworks.py <ip address list file>
```

Once we place all the /24 network to analyze in a file, we can execute a nmap ping sweep to identify active IP address, which can be automatized with the script *nmap_subnet_sweep.sh*:

```
./nmap_subnet_sweep.sh <file with list of /24 subnetworks>
```

The script invokes a ping sweep nmap scan for each subnet and it saves the output in a txt file called *pingsweep.txt*, which is afterwards processed to output the list of responding IP addresses in a set of files, one for each subnet and called *ips_<subnet .0 address>_24.txt*.

## 3. Port Scan with nmap

Once we have a list of ping-responding IP addresses, we can actively scan their ports to get a profile of each asset. We have automatized the process with the script *nmap_discovery.sh*. This script invokes a standard nmap scan for each IP and, once it is finished, it erases the IP address from the file. Doing so, the scan can be interrumpted at any time and continued at any other moment by just invoking the same function, without repeating previously done scans. We can directly use the *ips_<subnet .0 address>_24.txt* files obtained from the previous step.

```
./nmap_discovery.sh <file with list of IP addresses>
```

The scan used is of type `nmap -sV -Pn <ip> -oA <nmap_$ip>`, but we can easily change the type of scan by modifying the script. As shown in the nmap command, the output will be stored for each analyzed IP address with the name nmap_<ip>, in all the supported output formats.

Once the scans are finished, we can easily transform the output to an Excel spreadsheet using the great tool [*nmap_converter.py*](https://github.com/mrschyte/nmap-converter):

```
./nmap-converter.py -o <full output path .xls> <full input nmap_<ip>.xml 
```

## 4. Analyzing individual ports

With those results, we can launch other scripts to massively analyze the discovered ports, in the quest of vulnerabilities. These scans could be launch at the same time that *nmap_discovery.sh*.

For example, we can look for SMB ports without signing for later launch a responder-based attack, using the script *cme_smb_signing_off.sh*. Given a list of subnetworks in a file, this script invokes crackmapexec for each subnet and, once it is finished, it saves in files both the list of IP addresses with SMB signing off (with format *targets_<subnet .0 address>_24.txt*) and the full output of CME (*cme_output_<subnet .0 address>_24.txt*).

```
./cme_smb_signing_off.sh <file with list of /24 subnetworks>
```

Other ports to analyze are those using SSL/TLS, that can be located in the resulting Excel with the open ports and massively scanned with *testssl* or *sslscan*.

For example, we can look for the SWEET32 vulnerability:

```
testssl --file ./ips_<subnet .0 address>_24.txt --sweet32 --csvfile sweet32_<subnet .0 address>_24.csv
```

Or we can check the TLS versions and details about the certificates (faster with *sslscan*):

```
sslscan --targets=<file> --no-heartbleed
```
