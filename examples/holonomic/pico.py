from romer_minirobot.urtps import uRTPS
from romer_minirobot.modules.pico import Holonomic, Button
from machine import Pin

SSID = "mechalab_intra"
PASSWORD = "mechastudent"

# SSID = "Printer_AP"
# PASSWORD = "K0van1231"

# Multicast group details
MULTICAST_GROUP = '224.0.0.252'# '224.1.1.1'
MULTICAST_TOPIC_PORT = 5007



urtps = uRTPS(SSID, PASSWORD, MULTICAST_GROUP, MULTICAST_TOPIC_PORT)
urtps.add_subscribing_topics(Holonomic())

urtps.add_publishing_topics(Button(12, Pin.PULL_UP, True, 0.1, 'isButtonPressed'))

urtps._start_async_main()