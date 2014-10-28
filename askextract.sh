#!/bin/bash
alias curl="./curl"

getnicks(){
local ask=$(curl -s -L -A "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0" http://ask.fm/)
ask=${ask##*heads\"\>}
echo $ask | awk -F'</a>' '{for(i=1;i<=13;i++){num = match($i, "=\"*\"") + 3; print substr($i, num, index($i, "\" da") - num)}}'
}

param=$1
howmuch=$((param/13))
if [[ $((param % 13)) != 0 ]]
then
  howmuch=$((howmuch+1))
fi

for i in $(seq 1 $howmuch)
do
  nicks=$(getnicks)$'\n'$nicks
done

printf "$nicks" | sort -f | uniq > uniquenicks.txt
printf "$nicks" > nicks.txt
printf "Number of got nicks: "
wc -l < nicks.txt
printf "Number of got unique nicks: "
wc -l < uniquenicks.txt