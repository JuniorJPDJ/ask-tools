#!/bin/bash
alias curl="./curl"
token=$(curl -s -L -A "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0" -c cookies.txt -b cookies.txt "http://ask.fm/$1")
token=${token##*AUTH_TOKEN\ =\ \"}
token=${token%%\";*}
curl -s -L -A "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0" -c cookies.txt -b cookies.txt --data-urlencode "authenticity_token=$token" --data-urlencode "question[question_text]=$2" -o /dev/null "http://ask.fm/$1/questions/create"
rm cookies.txt