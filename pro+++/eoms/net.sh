#!/bin/bash 

if [ -n "${1}" ];
        then 
    NetDevice=${1};
else 
    NetDevice=wlp3s0;
fi 
    printf "|------ Time  ------|---- NetIn ----|--- NetOUt ----|\n" 
while true 
    do time=$(date +%F" "%T) 
        rx_before=$(ifconfig ${NetDevice}|awk -F' *|:' '{if($2=="RX"&&$3=="bytes") print $4}') 
        tx_before=$(ifconfig ${NetDevice}|awk -F' *|:' '{if($2=="RX"&&$3=="bytes") print $9}')
     sleep 1 
        rx_after=$(ifconfig ${NetDevice}|awk -F' *|:' '{if($2=="RX"&&$3=="bytes") print $4}') 
        tx_after=$(ifconfig ${NetDevice}|awk -F' *|:' '{if($2=="RX"&&$3=="bytes") print $9}') 
        rx_result=$(((rx_after-rx_before)/1024)) 
        tx_result=$(((tx_after-tx_before)/1024)) 
printf "|%19s|%10s kbps|%10s kbps|\n" "${time}" "${rx_result}" "${tx_result}"
 # sleep 1 
done


