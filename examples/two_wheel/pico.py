from romer_minirobot.urtps import uRTPS
from romer_minirobot.modules.pico import TwoWheel, Button
from machine import Pin

SSID = "mechalab_intra"
PASSWORD = "mechastudent"

# SSID = "Printer_AP"
# PASSWORD = "K0van1231"

# Multicast group details
MULTICAST_GROUP = '224.0.0.252'# '224.1.1.1'
MULTICAST_TOPIC_PORT = 5007

if __name__ == "__main__":
    
    urtps = uRTPS(SSID, PASSWORD, MULTICAST_GROUP, MULTICAST_TOPIC_PORT)
    
    urtps.add_subscribing_topics(TwoWheel())
    urtps.add_publishing_topics(Button(12, Pin.PULL_UP, True, 0.1, 'button1'))
    
    urtps.start()