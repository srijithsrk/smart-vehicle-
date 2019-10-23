import smtplib, ssl
import serial
import RPi.GPIO as GPIO
import os, time
from decimal import *
delay = 1
GPIO.setmode(GPIO.BOARD)
E=0
F=0
def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
cd=1
try:
    while cd <= 50:
        ck=0
        fd=''
        while ck <= 50:
            rcv = port.read(10)
            
            fd=fd+rcv
            ck=ck+1
        
        if '$GPRMC' in fd:
            ps=fd.find('$GPRMC')
            dif=len(fd)-ps
            
            if dif > 50:
                data=fd[ps:(ps+50)]
                print(data)
                p=list(find(data, ","))
                lat=data[(p[2]+1):p[3]]
                lon=data[(p[4]+1):p[5]]
                
                s1=lat[2:len(lat)]
                s1=Decimal(s1)
                s1=s1/60
                s11=int(lat[0:2])
                s1=s11+s1
                
                s2=lon[3:len(lon)]
                s2=Decimal(s2)
                s2=s2/60
                s22=int(lon[0:3])
                s2=s22+s2
                E=s1
                F=s2
            
            #print("Latitude:",s1)
            #print("Longitude:",s2)
            cd=cd+1
            if cd==3:
                break;
            print(cd)
print (E)
print("  ")
print (F)
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
    sender_email = "srijith698@gmail.com"  # Enter your address
    receiver_email = "srijith125@gmail.com"  # Enter receiver address
    password = '1234567'
    message ="""\
        Subject: Hello
        
        I am here. This is my Refference ID:101 in EMERGENCY Situation you can locate me at the given location http://maps.google.com/?q=%s,%s"""%(E,F)
    
    context=ssl.create_default_context()
    server=smtplib.SMTP_SSL(smtp_server,port)
    server.login(sender_email,password)
    print('it worked!')
    server.sendmail(sender_email,receiver_email,message)
    print('Mail sent')
    server.quit()



except KeyboardInterrupt:
    print("Thank You")

