#!/usr/bin/env python3

from scapy.all import DNS, DNSQR, IP, RandShort, UDP, send

send(IP(src="172.16.235.5", dst="172.16.235.1")/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname="gmail.com", qtype="MX")))
