# Input is a file of IP /24 subnetworks
# The script invokes a ping sweep nmap scan for each subnet and, once it is finished, it saves the list of IP addresses in a txt file.

if [ $# -eq 0 ]
  then
    echo "You need to provide the name of the file with the list of subnetworks to scan"
else

    for subnet in $(cat $1)
    do
        #Removing the possible trailing whitespaces
        trimmed=`echo $subnet | tr -d " \t\n\r"`
        echo $trimmed
        echo "..............................."
        nmap -sn -v $trimmed -oG pingsweep.txt
        short=$(echo $trimmed | cut -d "/" -f 1)
        echo $short
        grep Up pingsweep.txt | cut -d " " -f 2 > ips_${short}_24.txt
        echo "..............................."
    done
fi
