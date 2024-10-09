#!/bin/bash
ping -q -c 1 $1 > dump_network_output.txt 2>&1
if grep -q "1 packets received" dump_network_output.txt
then
    echo OK
else
    echo "Host is not reachable"
fi
