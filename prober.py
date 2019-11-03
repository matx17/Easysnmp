#!/usr/bin/python
from easysnmp import Session
import easysnmp
import sys
import time
authlist = sys.argv
auth = str(authlist[1]).split(":")
freq = float(authlist[2])
t = 1/freq
s = authlist[3]
count=0
sysup = ['1.3.6.1.2.1.1.3.0']
oidslist = authlist[4:len(authlist)]
oids = sysup + oidslist
oldest=[]
out1=[]
t4=0

while (count!= int(s)):
  t1=time.time()
  try:
      session = Session(hostname=auth[0], remote_port = auth[1], community=auth[2], version=2)
      latest = session.get(oids)
      t2=time.time()
  except easysnmp.exceptions.EasySNMPTimeoutError:
      #print "timeout"
      continue

  if len(latest)==len(oldest):
   latesttime=float(latest[0].value)/100
   oldesttime=float(oldest[0].value)/100
   if freq > 1:
     tdifference = latesttime-oldesttime
   if freq <= 1:
     tdifference1 = t1-t4
     if tdifference1!=0:
      tdifference = int(tdifference1)
     else:
      tdifference = int(t)
   for i in range(1,len(oids)):
      if latest[i].value!="NOSUCHINSTANCE" and oldest[i].value!="NOSUCHINSTANCE":
         a=int(latest[i].value)
         b=int(oldest[i].value)
         if a>=b:
           out=(a-b)/tdifference
           out1.append(out)
         if a<b and latest[i].snmp_type=="COUNTER64":
           out=((2**64+a)-b)/tdifference
           out1.append(out)
         if a<b and latest[i].snmp_type=="COUNTER32":
           out=((2**32+a)-b)/tdifference
           out1.append(out)
      else:
        print t1, "|"

   if len(out1)!=0:
      sar = [str(get) for get in out1]
      print int(t1) ,'|', ("|" . join(sar))
      count=count+1
  oldest = latest[:]
  t4=t1
  del out1[:]
  t3=time.time()
  if t-t3+t1>0:
    time.sleep(t-t3+t1)
  else:
    time.sleep(0.0)
