# Input is a file of IP /24 subnetworks
# The script invokes crackmapexec for each subnet and, once it is finished, it saves both the list of IP addresses with SMB signing off and the full output of CME in files

if [ $# -eq 0 ]
  then
    echo "You need to provide the name of the file with the list of subnetworks to scan"
else

    for subnet in $(cat $1)
    do
        echo $subnet
        echo "..............................."
        short=$(echo $subnet | cut -d "/" -f 1)
        cme smb $subnet --gen-relay-list targets_${short}_24.txt | tee cme_output_${short}_24.txt
        echo "..............................."
    done
fi