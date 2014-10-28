import urllib2, re, sys

try:
  nick = sys.argv[1]
except:
  print "First parameter (nick) not specified"
  sys.exit()
try:
  file = sys.argv[2]
except:
  file = "nicks.txt"
nicks = []

res = urllib2.urlopen("http://ask.fm/"+nick+"/gifts").read()
linksregex = re.compile("<a href=\".*?\" class=\"link-blue\" dir=\"ltr\">")
links = linksregex.findall(res)
for link in links:
  #print link[10:-30]
  nicks.append(link[10:-30])

try:
  pages = re.findall('class=\"link-page\">.*?<\/a><a href=\"\/'+nick+'\/gifts\?page=2\" class=\"link-page-arrow_right\">', res)[0]
  pages = pages[:pages.rfind("</a>")]
  pages = int(pages[pages.rfind(">")+1:])
except:
  pages = 1

i = 1

sys.stderr.write("User "+nick+" has "+str(pages)+" pages of gifts\n")
sys.stderr.write("Processing page 1 finished\n")

while i < pages:
  i = i+1
  page = urllib2.urlopen("http://ask.fm/"+nick+"/gifts?page="+str(i)).read()
  links = linksregex.findall(page)
  for link in links:
    nicks.append(link[10:-30])
  sys.stderr.write("Processing page "+str(i)+" finished\n")

print "Extracted nicks: " + str(len(nicks))
nicks = sorted(set(nicks), key=lambda k: k.lower())
print "Unique nicks: " + str(len(nicks))
print "Saving unique nicks to file '"+file+"'"
file = open(file, 'w')
file.write("\n".join(nicks))
file.close()