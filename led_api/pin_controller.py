import logging
import socket
import pigpio

from led_api.util import hex_2_rgb, Glob
log = logging.getLogger(__name__)

global pi

def start_pigpio():
    global pi
    if Glob.config['pins_enabled']:
        pi=pigpio.pi()

#start stream mode on UDP port and change color in realtime
#TODO Error Handling
def stream_thread():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", Glob.config['udp_port']))
    log.info ("Stream mode waiting on port:"+ str(Glob.config['udp_port']))
    while 1:
        str_color, addr = s.recvfrom(1024)
        if (str_color == 'exit'):
            return 1
        log.debug("parsing string: " + str(str_color))
    set_color_by_hex(str_color)
    return 1

#set gpio values according to rgb-color-hex
def set_color_by_hex(colorhex):
    r,g,b = hex_2_rgb(colorhex)
    return set_color(r,g,b)

#set gpio values according to rgb-color 
def set_color(red,green,blue):
    global pi
    msg= 'r={0}, g={1}, b={2}'.format(red,green,blue)
    if Glob.config['pins_enabled']:
        pi.set_PWM_dutycycle(pin_red,red)
        pi.set_PWM_dutycycle(pin_green,green)
        pi.set_PWM_dutycycle(pin_blue,blue)
    else:
        print(msg)
    return msg
