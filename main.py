import logging

from twisted.web._newclient import ResponseNeverReceived

try:
    pass
except ResponseNeverReceived:
    logging.log(logging.ERROR, '图书馆炸了😣')

# 0000219890
