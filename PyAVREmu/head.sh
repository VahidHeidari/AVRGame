#!/bin/bash

MX=10000

STATE_PATH=3rdParty/uzem/Release/state.txt
if [[! -f $STATE_PATH ]]
then
	STATE_PATH=3rdParty/uzem/Debug/state.txt
fi

for ((i=1; i <= $MX; ++i)) do
	clear
	echo head \`$STATE_PATH\'  -\> $i of $MX
	head -n 26 $STATE_PATH
	sleep 0.5
done
