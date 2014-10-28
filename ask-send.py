import cookielib, urllib, urllib2, random, os, sys, socket, socks, time

from stem import Signal
from stem.control import Controller

#i = 0

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
oldsocket = socket.socket
socket.socket = socks.socksocket

def captcha(*args):
  #global i
  #i = i+1
  socket.socket = oldsocket
  with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    controller.signal(Signal.NEWNYM)
  socket.socket = socks.socksocket
  print 'Captcha or IP error detected - changing IP'
  time.sleep(5)
  
  #print 'Captcha :C. Press enter, when i can start sending'
  #raw_input()

def gettoken():
  global cj
  cj = cookielib.LWPCookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  urllib2.install_opener(opener)
  tokenpage = urllib2.urlopen('http://ask.fm/'+nick, timeout=10).read()
  token = tokenpage[tokenpage.find(' AUTH_TOKEN = "')+15:]
  token = token[:token.find('"')]
  
  if ((tokenpage.find('image-captcha') > -1) or (tokenpage.find('No robots allowed!') > -1)):
    captcha(tokenpage)
    token = gettoken()
  
  return token

try:
  nicks = sys.argv[1]
  try:
    msg = sys.argv[2]
  except:
    print "Second parameter (message to send/list of messages in file) not specified"
    sys.exit()
except:
  print "First parameter (nick/list of nicks in file) not specified"
  sys.exit()

if os.path.isfile(nicks):
  print "Found file "+nicks+"! Messages will now be sent to nicks taken from that file."
  nicks = map(lambda s: s.strip(), open(nicks, 'rU').readlines())
else:
  nicks = [nicks]

if os.path.isfile(msg):
  print "Found file "+msg+"! Selected mode is: random messages from file."
  msgfile = True
else:
  print "Message parameter does not point to a file. Selected mode is: one message to all (from paramater)"
  msgfile = False
  
def getmsg():
  global msgfile
  if msgfile:
    msgfile = map(lambda s: s.strip(), open(msg, 'rU').readlines())
    return msgfile[random.randint(0,len(msgfile)-1)]
  else:
    return msg

for nick in nicks:
  msg1 = getmsg()
  err = 0
  while 1:
    try:
      log = urllib2.urlopen(urllib2.Request('http://ask.fm/'+nick+'/questions/create' , urllib.urlencode({'authenticity_token':gettoken(), 'question[question_text]':msg1})), timeout=10).read()
      if (log.find('onclick="Profile.showQuestionForm();') > -1):
        print 'Message "'+msg1+'" sent to '+nick
        break
      #elif (log.find('No robots allowed!') > -1):
      #  print "Robot detected :C"
      #  captcha()
      elif (log.find('onclick="Login.showPopup(this,') > -1):
        print nick+' does not allow anonymous asking'
        break
      else:
        open('log.txt','w').write(log)
        print 'Error while sending message "'+msg1+'" to '+nick+'!'
    except Exception as e:
      print "Error while sending message \""+msg1+"\" to "+nick+"! - "+str(e)
    err = err + 1
    if err >= 10:
      break
    elif err >= 5:
      captcha()