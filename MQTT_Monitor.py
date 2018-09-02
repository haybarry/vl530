#Try robust MQTT

#

# Test of setup with GIT
# 20/10/17  try lists for topics.  and index list to check which topic
#
#update to use 12c display

import machine, time, utime
import network

from umqtt.robust import MQTTClient

from machine import Pin

from machine import Timer

import ubinascii
from sh1106 import SH1106_SPI, SH1106_I2C
from writer import Writer

# Fonts
#import freesans20
import myfont12
#import freeserif19
#import inconsolata16


#configure display
WIDTH = const(128)
SPI = False
Lastline = 0
NewScreen = False
if SPI:
    # Pyb   SSD
    # 3v3   Vin
    # Gnd   Gnd
    # X1    DC
    # X2    CS
    # X3    Rst
    # X6    CLK
    # X8    DATA
    HEIGHT = 64
    pdc = machine.Pin(2, machine.Pin.OUT)
    pcs = machine.Pin(15, machine.Pin.OUT)
    prst = machine.Pin(0, machine.Pin.OUT)
    #spi = machine.SPI(1)
    spi = machine.SPI(1, baudrate=5000000, polarity=1, phase=1)
    shdisp = SH1106_SPI(WIDTH, HEIGHT, spi, pdc, prst)
else:  # I2C
    # Pyb   SSD
    # 3v3   Vin
    # Gnd   Gnd
    # Y9    CLK
    # Y10   DATA
    HEIGHT = 64
    pscl = machine.Pin(4, machine.Pin.OUT)
    psda = machine.Pin(5, machine.Pin.OUT)
    i2c = machine.I2C(scl=pscl, sda=psda)
    shdisp = SH1106_I2C(WIDTH, HEIGHT, i2c, None)
DispTopic = ["","","","",""]
DispMsg = ["","","","",""]
wri2 = Writer(shdisp, myfont12, verbose=False)   #  freesans20
Writer.set_clip(True, True)

#Configure Network

CONFIG = {

    "client_id": ubinascii.hexlify(machine.unique_id()),

}



channel = [b'INSIDE/TEMP', b'INSIDE/HUMID', b'AQUAP/AIR', b'AQUAP/WATER', b'HYDRO/FLOW']



sec1 = 1000
sec60 = 60000   #12 minutes

sec101 = 10100   #10.1 seconds

Wdog_TimeOut = 720000   







def sub_wifi():

    global np
    print('connecting to network...')
    
    sta_if.active(True)
    sta_if.connect('canucks_fans_live_here', 'Impre5si0ni5t')
    while not sta_if.isconnected():
        pass

    print('network config:', sta_if.ifconfig())




def sub_MQTT():

    c.connect()

#    np.write()

#    c.subscribe(T_TOPIC)

#    c.subscribe(H_TOPIC)




    
def sub_CB(topic, msg):
#    global RedDog, Wdog_Timer
#    print(topic, msg)
    global Lastline, NewScreen
    yy = channel.index(topic)
    DispTopic[yy] = topic
    DispMsg[yy] = msg
    NewScreen = True
    print(topic)
    print(NewScreen)
   

def sub_screendraw():
    print('refresh')
    wri2.set_textpos(0, 0)
    for x in range(5):
        print(x)
        z = str(DispTopic[x],'utf-8') + ': ' + str(DispMsg[x],'utf-8') + '          \n'      
        wri2.printstring(z) 
        print(DispTopic[x])   
    shdisp.show()
   



sta_if = network.WLAN(network.STA_IF)

mac = sta_if.config('mac') # get full mac address

macascii = ubinascii.hexlify(mac)  # turn mac into ascii 

node = macascii[6:]  # node for MQTT

server = "192.168.1.180"

c = MQTTClient(node, server)

c.set_callback(sub_CB)

sub_wifi()
sub_MQTT()
for z in range(5):
    c.subscribe(channel[z])


#sub_MQTT()



#setup_pins()

reftime = utime.ticks_ms()
onesec = utime.ticks_ms()
Wdog_Timer = utime.ticks_ms()

while True:

    if not sta_if.isconnected():
        sub_wifi()
        c.disconnect()
        sub_MQTT()


#    if not c.connect():
#        sub_MQTT()
#    c.connect()

    now = utime.ticks_ms()

    if utime.ticks_diff(now, reftime) > sec60:     #  Ifcycle time greater then 60 sec

        reftime = reftime + sec60

           

    c.check_msg()

    if NewScreen == True:
        sub_screendraw()
        NewScreen = False 


 