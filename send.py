#!/usr/bin/env python3
import random
import socket
import sys
from time import sleep


from scapy.all import IP, TCP, Ether, get_if_hwaddr, get_if_list, sendp, sr1


def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def main():

    if len(sys.argv)<3:
        print('pass 2 arguments: <destination> "<message>"')
        exit(1)
    avgrtt = 0
    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    print("sending on interface %s to %s" % (iface, str(addr)))
    pkt = IP(dst=addr) / TCP(dport=1234, flags = "S")
    pkt.show2()
   
    try:
      for i in range(int(sys.argv[3])):
         a = sr1(pkt)
         print(a.time - pkt.sent_time)
         avgrtt += (a.time - pkt.sent_time)
         sleep(1)
      print("Average RTT = ", avgrtt/sys.argv[3])
    except KeyboardInterrupt:
        raise

if __name__ == '__main__':
    main()
