<h1 align="center">Challenge 040 - Dig Dug </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/a3934bea-1862-4fdf-ad4f-7e8601dfa73b" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 10.10.2025  </p>

We will have the opportunity to play around with a DNS server. We are supposed to dig into it to find some interesting records, but as it seems, we only get a response when a request is sent to a specific kind of domain: *givemetheflag.com*.

Apparently we will have to use some common DNS enumeration tools installed on the AttackBox to get the DNS server to respond with the flag.

Checking out the address, didn't lead to anything. I thought adding the already mentioned domain name to the etc/hosts/ file would maybe lead to something.

```
127.0.0.1	localhost
127.0.0.1       vnc.tryhackme.tech
127.0.1.1	tryhackme.lan	tryhackme

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

10.10.240.191 givemetheflag.com
```

But I was wrong, which surprised me a little bit. We might have a firewall or there is not even running a web service at that IP address. 

Just to make sure what happens, I used nmap to see the output

```
root@ip-10-10-124-217:~# nmap -p- -sV 10.10.240.191
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-10 20:05 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for givemetheflag.com (10.10.240.191)
Host is up (0.00019s latency).
Not shown: 65534 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
MAC Address: 02:14:1E:16:3F:31 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 3.81 seconds
```

Not much that we can work with as of now. It explains why we couldn't see a website though.

## dig

After I had no luck with browsing I just researched what *dig* exactly is, as it was heavily emphasized. Turns out it's a command-line tool used for DNS lookup. It allows us to query DNS servers to retrieve information about a domain, such as its IP address or other DNS records. Now knowing about this information we might as well make use of it.

```
root@ip-10-10-124-217:~# dig 10.10.240.191

; <<>> DiG 9.18.28-0ubuntu0.20.04.1-Ubuntu <<>> 10.10.240.191
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 11921
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;10.10.240.191.			IN	A

;; ANSWER SECTION:
10.10.240.191.		0	IN	A	10.10.240.191

;; Query time: 3 msec
;; SERVER: ::1#53(::1) (UDP)
;; WHEN: Fri Oct 10 19:58:57 BST 2025
;; MSG SIZE  rcvd: 58
```

The answer section didn't reveal that much, as I used the tool completely wrong. I basically asked for the IP-address of an IP-address. My bad.

When the tool is used the correct way, we have the possibility to see specific kind of records like Mail exchange (MX) *dig givemetheflag MX*. Mail servers are visible that way.

```
root@ip-10-10-124-217:~# dig givemetheflag.com MX

; <<>> DiG 9.18.28-0ubuntu0.20.04.1-Ubuntu <<>> givemetheflag.com MX
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15363
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;givemetheflag.com.		IN	MX

;; ANSWER SECTION:
givemetheflag.com.	3600	IN	MX	0 .

;; Query time: 31 msec
;; SERVER: ::1#53(::1) (UDP)
;; WHEN: Fri Oct 10 20:44:22 BST 2025
;; MSG SIZE  rcvd: 61
```

Not here though. MX would reveal where to deliver email for a domain. A normal record would look something like this

```
example.com.  3600  IN  MX  10  mail.example.com.
```

but in the example of before the dot in the answer section makes clear that there is no server.

Text records can be seen as well (TXT) *dig givemetheflag TXT*. When a service is set up, and we want to validate that we own a domain for example, we have to write a text record.

```
root@ip-10-10-124-217:~# dig givemetheflag.com TXT

; <<>> DiG 9.18.28-0ubuntu0.20.04.1-Ubuntu <<>> givemetheflag.com TXT
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42679
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;givemetheflag.com.		IN	TXT

;; ANSWER SECTION:
givemetheflag.com.	3600	IN	TXT	"v=spf1 -all"

;; Query time: 31 msec
;; SERVER: ::1#53(::1) (UDP)
;; WHEN: Fri Oct 10 20:45:54 BST 2025
;; MSG SIZE  rcvd: 70
```

In this example though we only get one result, which is the Sender Policy Framework (SPF). It tells mail servers, which hosts are allowed to send emails for the domain. In this case the *-all* makes clear that no server is allowed to do that. We can't do much with this information, except maybe that we can ignore mail from this domain as it's probably fake. 

Lastly we can also use a specific DNS server for our lookups. When we write *dig @10.10.240.191 givemetheflag.com* we query the DNS server at the specified IP address for information about the domain *givemetheflag.com*. Through that we can check local DNS issues, DNS caching or look up response times.

```
root@ip-10-10-124-217:~# dig @10.10.240.191 givemetheflag.com

; <<>> DiG 9.18.28-0ubuntu0.20.04.1-Ubuntu <<>> @10.10.240.191 givemetheflag.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 46818
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;givemetheflag.com.		IN	A

;; ANSWER SECTION:
givemetheflag.com.	0	IN	TXT	"flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}"

;; Query time: 0 msec
;; SERVER: 10.10.240.191#53(10.10.240.191) (UDP)
;; WHEN: Fri Oct 10 20:28:45 BST 2025
;; MSG SIZE  rcvd: 86
```

Which revealed the flag to us. As we can see dig is a very useful tool if we want to get an overview over different DNS servers and their domains. There was another command called *nslookup* with which we can get similar results.

## nslookup

The command is almost the same, only with domain name and IP-address switched.

```
root@ip-10-10-124-217:~# nslookup givemetheflag.com 10.10.240.191
Server:		10.10.240.191
Address:	10.10.240.191#53

givemetheflag.com	text = "flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}"
givemetheflag.com	text = "flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}"
```

It's completely up to us, how we want to solve this task. In any case, both these commands are very useful, if we ever need to do some DNS enumeration and how to interact with DNS servers. Very insightful.
