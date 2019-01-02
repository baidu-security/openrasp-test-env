#!/usr/bin/env python

import socket
import sys

def getAddr(hostname):
    result = socket.getaddrinfo(hostname, None)
    return result[0][4][0]

if __name__ == "__main__":
    print getAddr("apache-php7.2")