import re, urllib2, cookielib, urllib, sys

try:
  nicks = int(sys.argv[1])
except:
  print "First parameter (nicks number) not specified or is not a number"
  sys.exit()

global cj
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
token = urllib2.urlopen('http://ask.fm/').read()
token = token[token.find(' AUTH_TOKEN = "')+15:]
token = token[:token.find('"')]

urllib2.urlopen(urllib2.Request('http://ask.fm/session' , urllib.urlencode({'authenticity_token':token, 'login':'nowekontotestowe', 'password':'nokurwa'})))

se = set()
le = 0
while len(se) <= nicks:
  le = len(se)
  res = urllib2.urlopen('http://ask.fm/account/stream').read()
  reg = re.findall('<a href=\"\/(?:(?!\/).)*?\"', res)
  se = se|set(map(lambda s:s[s.find('/')+1:-1], reg))
  se.discard('signup')
  se.discard('languages')
  se.discard('')
  if le != len(se):
    print "Already downloaded "+str(len(se))+" nicks"

file = open('nicks.txt', 'w')
file.write("\n".join(sorted(se, key=lambda k: k.lower())))
file.close()