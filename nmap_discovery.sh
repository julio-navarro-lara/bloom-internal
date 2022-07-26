# Input is a file of IP addresses
# The script invokes a nmap scan for each IP and, once it is finished, it erases the IP address from the file. Doing so, the scan can be interrumpted at any time and continued at any other moment by just invoking the same function, without repeating previously done scans.

if [ $# -eq 0 ]
  then
    echo "You need to provide the name of the file with the list of IP addresses to test"
else

    counter=$(wc -l $1 | cut -f 1 -d " " )
    echo $counter

    for i in $(seq 1 $(($counter)))
    do
        ip=$(head -n 1 $1 | tr -d -c [:graph:])
        echo $ip
        echo "..............................."
        nmap -sV -Pn -oA nmap_$ip $ip
        echo "..............................."
        tail -n +2 $1 > tmp.txt
        mv tmp.txt $1
    done
fi
