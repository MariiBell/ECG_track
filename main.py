import machine
import time
import socket
import network
from machine import ADC, Pin, Timer




SDNn = Pin(5, machine.Pin.OUT) 
SDNn.value(0) # выключили ЭКГ, чтобы было больше тока для подключения к Вифи

adc = ADC(Pin(4))        # create an ADC object acting on a pin
LOn = ADC(Pin(2))        # create an ADC object acting on a pin
LOp = ADC(Pin(3))        # create an ADC object acting on a pin

# enable station interface and connect to WiFi access point
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('iPhoneMasha', '12345678')

while (True):

    while not nic.isconnected():
        pass
    print('WLAN connection succeeded!')
    SDNn.value(1) # включили ЭКГ после подключения к ВиФи
    break

# server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# # Enable broadcasting mode
# server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# # Set a timeout so the socket does not block
# # indefinitely when trying to receive data.

# server.connect(('255.255.255.255', 5006))

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind(('0.0.0.0', 5006))

print('Socket created')


message = b"it's me"

        
# PN_SOOOOOOS

while (True):
    server.sendto(message, ("255.255.255.255", 5006))
    print("message sent")
    time.sleep(1)      
    data, adr = server.recvfrom(1024)
    if data == message:
        right_adr = adr
        print('Adress polychen')
        break

while True:

    # data, adr = server.recvfrom(1024)
    # if adr == right_adr:
       # get_adc - название функции, где прописываем АЦП
    print(data)
    # if data == b'1':
    def get_adc(_):
        if ((LOn.read_u16()<65000) & (LOp.read_u16()<65000)): #проверка, что электроды не отвалились
            val = adc.read_u16()
            time1 = time.time_ns()
            val = str(val)+ ' ' +str(time1)
            server.sendto(val.encode() , adr)
        else:
            time1 = time.time_ns()
            val = str(65500)+ ' ' +str(time1)
            server.sendto(val.encode() , adr)
            

    print("ADC mode entering...")
    tim0 = Timer(0)
    tim0.init(freq=250, mode=Timer.PERIODIC, callback=get_adc) # прерывание по таймингу
    while 1:
        pass
