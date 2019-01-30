#!/bin/bash -e

pAntler wamv.moos >& /dev/null &
# pAntler wamv.moos
sleep 0.25

morse run wamv_sim

printf "Killing all processes ... \n"
kill -- -$$
printf "Done killing processes.   \n"
