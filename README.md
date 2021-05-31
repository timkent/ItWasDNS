# Understanding and attacking DNS

## Four VMs
1. 172.16.235.4 demo-dns-attacker
2. 172.16.235.5 demo-dns-victim
3. 172.16.235.6 demo-dns-server
4. Firefox VM

## Amplification attack
1. Run `tcpdump -n port 53` on victim
2. Run `sudo ./dns_udp_src_spoof.py` on attacker

## Cache poisoning
Made possible by increasing latency to real authoritative server, and using a fixed source address.
1. Run `sudo ./serve_good` on server
2. Run `sudo ./serve_resolver` on victim
3. Run `sudo ./dns_cache_poison.py` on victim
4. Show results with `dig @localhost good.pwned.tk` on victim

## Rebind
1. Run `sudo ./dns_rebind.py` on attacker
2. Run `python3 -m http.server 5000` on victim
3. Copy `resolv.conf` to `/etc` on Firefox VM (or otherwise point DNS to `172.16.235.5`)
4. Browse to `http://bad.pwned.tk:5000` on Firefox VM
